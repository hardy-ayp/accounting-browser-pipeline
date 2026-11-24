from decimal import Decimal
from typing import Dict, Any, List, Tuple

def reconcile_records(
    subledger_records: Dict[str, Dict[str, Any]],
    general_ledger_records: Dict[str, Dict[str, Any]]
) -> Dict[str, List[Any]]:
    """
    Executes 5-pass reconciliation between subledger transactions and general ledger records.
    """
    matched = []
    discrepancies = []
    missing_in_gl = []
    missing_in_subledger = []

    gl_matched_keys = set()

    for ref_id, s_row in subledger_records.items():
        if ref_id in general_ledger_records:
            g_row = general_ledger_records[ref_id]
            gl_matched_keys.add(ref_id)

            delta_qty = Decimal(str(s_row.get("quantity", 0))) - Decimal(str(g_row.get("quantity", 0)))
            delta_amount = Decimal(str(s_row.get("amount", 0))) - Decimal(str(g_row.get("amount", 0)))

            if abs(delta_qty) < Decimal("0.0001") and abs(delta_amount) == Decimal("0"):
                if s_row.get("date") == g_row.get("date"):
                    matched.append((ref_id, s_row, g_row, "EXACT_MATCH"))
                else:
                    matched.append((ref_id, s_row, g_row, "TIMING_DIFFERENCE"))
            else:
                discrepancies.append((ref_id, s_row, g_row, delta_qty, delta_amount))
        else:
            missing_in_gl.append((ref_id, s_row))

    for ref_id, g_row in general_ledger_records.items():
        if ref_id not in gl_matched_keys:
            missing_in_subledger.append((ref_id, g_row))

    return {
        "matched": matched,
        "discrepancies": discrepancies,
        "missing_in_gl": missing_in_gl,
        "missing_in_subledger": missing_in_subledger
    }

def verify_balance_proof(
    beginning_balance: Decimal,
    total_inflows: Decimal,
    total_outflows: Decimal,
    actual_ending_balance: Decimal
) -> Dict[str, Any]:
    """
    Validates: Ending Balance = Beginning Balance + Inflows - Outflows
    """
    calculated_ending = beginning_balance + total_inflows - total_outflows
    variance = actual_ending_balance - calculated_ending
    return {
        "beginning": beginning_balance,
        "inflow": total_inflows,
        "outflow": total_outflows,
        "calculated_ending": calculated_ending,
        "actual_ending": actual_ending_balance,
        "variance": variance,
        "is_balanced": abs(variance) < Decimal("0.0001")
    }

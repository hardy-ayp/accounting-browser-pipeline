import unittest
from decimal import Decimal
import tempfile
import os
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.reconciler import reconcile_records, verify_balance_proof
from src.downloader import validate_magic_bytes, compute_checksums
from src.schema_builder import sanitize_identifier, generate_ddl

class TestAccountingPipeline(unittest.TestCase):

    def test_reconcile_records(self):
        subledger = {
            "TX-1": {"quantity": Decimal("10.5"), "amount": Decimal("1000"), "date": "2026-11-01"},
            "TX-2": {"quantity": Decimal("5.0"), "amount": Decimal("500"), "date": "2026-11-01"},
        }
        general_ledger = {
            "TX-1": {"quantity": Decimal("10.5"), "amount": Decimal("1000"), "date": "2026-11-01"},
            "TX-2": {"quantity": Decimal("5.0"), "amount": Decimal("480"), "date": "2026-11-01"},
            "TX-3": {"quantity": Decimal("2.0"), "amount": Decimal("200"), "date": "2026-11-01"},
        }

        res = reconcile_records(subledger, general_ledger)
        self.assertEqual(len(res["matched"]), 1)
        self.assertEqual(len(res["discrepancies"]), 1)
        self.assertEqual(len(res["missing_in_subledger"]), 1)
        self.assertEqual(len(res["missing_in_gl"]), 0)

    def test_balance_proof(self):
        proof = verify_balance_proof(
            beginning_balance=Decimal("100.00"),
            total_inflows=Decimal("50.00"),
            total_outflows=Decimal("30.00"),
            actual_ending_balance=Decimal("120.00")
        )
        self.assertTrue(proof["is_balanced"])
        self.assertEqual(proof["variance"], Decimal("0.00"))

    def test_sanitize_identifier(self):
        self.assertEqual(sanitize_identifier("Order Date"), "order_date")
        self.assertEqual(sanitize_identifier("Total (IDR)"), "total_idr")
        self.assertEqual(sanitize_identifier("select"), "select_val")

    def test_magic_bytes_and_checksums(self):
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
            tmp.write(b"PK\x03\x04sampledata")
            tmp_path = tmp.name

        try:
            self.assertTrue(validate_magic_bytes(tmp_path, "xlsx"))
            self.assertFalse(validate_magic_bytes(tmp_path, "pdf"))
            sums = compute_checksums(tmp_path)
            self.assertEqual(len(sums["md5"]), 32)
            self.assertEqual(len(sums["sha256"]), 64)
        finally:
            os.remove(tmp_path)

if __name__ == "__main__":
    unittest.main()

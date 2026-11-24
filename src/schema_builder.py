import re
from typing import List, Dict

RESERVED_SQL_WORDS = {
    "select", "from", "where", "order", "group", "by", "having",
    "insert", "update", "delete", "table", "index", "key", "desc", "asc"
}

def sanitize_identifier(raw_name: str) -> str:
    """
    Cleans raw column headers into safe SQL column identifiers.
    """
    cleaned = re.sub(r"[^\w\s]", "", str(raw_name).strip())
    cleaned = re.sub(r"\s+", "_", cleaned).lower()
    if not cleaned or cleaned[0].isdigit():
        cleaned = f"col_{cleaned}"
    if cleaned in RESERVED_SQL_WORDS:
        cleaned = f"{cleaned}_val"
    return cleaned

def generate_ddl(table_name: str, column_specs: Dict[str, str]) -> str:
    """
    Generates CREATE TABLE statement with DECIMAL(18,4) precision for financial quantities.
    """
    safe_table = sanitize_identifier(table_name)
    columns_ddl = []

    columns_ddl.append("id BIGINT AUTO_INCREMENT PRIMARY KEY")
    for raw_col, col_type in column_specs.items():
        safe_col = sanitize_identifier(raw_col)
        columns_ddl.append(f"{safe_col} {col_type}")

    columns_ddl.append("created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    body = ",\n    ".join(columns_ddl)
    return f"CREATE TABLE IF NOT EXISTS {safe_table} (\n    {body}\n);"

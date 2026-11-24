import hashlib
import os
from typing import Dict, Optional

MAGIC_SIGNATURES = {
    "xlsx": b"PK\x03\x04",
    "xls": b"\xd0\xcf\x11\xe0",
    "pdf": b"%PDF"
}

def validate_magic_bytes(file_path: str, expected_extension: str) -> bool:
    """
    Ensures downloaded report matches expected binary magic bytes and is not an error HTML page.
    """
    ext = expected_extension.lower().lstrip(".")
    if ext not in MAGIC_SIGNATURES:
        return True

    expected_magic = MAGIC_SIGNATURES[ext]
    if not os.path.exists(file_path):
        return False

    with open(file_path, "rb") as f:
        header = f.read(len(expected_magic))
        return header == expected_magic

def compute_checksums(file_path: str) -> Dict[str, str]:
    """
    Computes MD5 and SHA-256 hashes for cryptographic deduplication.
    """
    md5_hash = hashlib.md5()
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            md5_hash.update(chunk)
            sha256_hash.update(chunk)

    return {
        "md5": md5_hash.hexdigest(),
        "sha256": sha256_hash.hexdigest(),
        "size_bytes": os.path.getsize(file_path)
    }

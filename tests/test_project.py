import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance.db"


def test_customer_count():
    connection = sqlite3.connect(DB_PATH)
    count = connection.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]
    connection.close()

    assert count == 100


def test_policy_count():
    connection = sqlite3.connect(DB_PATH)
    count = connection.execute(
        "SELECT COUNT(*) FROM policies"
    ).fetchone()[0]
    connection.close()

    assert count == 2000


def test_claim_count():
    connection = sqlite3.connect(DB_PATH)
    count = connection.execute(
        "SELECT COUNT(*) FROM claims"
    ).fetchone()[0]
    connection.close()

    assert count == 1000


def test_document_count():
    connection = sqlite3.connect(DB_PATH)
    count = connection.execute(
        "SELECT COUNT(*) FROM documents"
    ).fetchone()[0]
    connection.close()

    assert count == 3000


def test_duplicate_claim_numbers():
    connection = sqlite3.connect(DB_PATH)

    duplicates = connection.execute("""
        SELECT claim_number
        FROM claims
        GROUP BY claim_number
        HAVING COUNT(*) > 1
    """).fetchall()

    connection.close()

    assert len(duplicates) == 0


def test_database_exists():
    assert DB_PATH.exists()
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance_test.db"

connection = sqlite3.connect(DB_PATH)

try:
    cursor = connection.cursor()

    print("RECORD COUNTS")

    for table in ["customers", "policies", "claims"]:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        print(f"{table}: {cursor.fetchone()[0]}")

    cursor.execute("""
        SELECT COUNT(*)
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        WHERE c.claim_date < p.start_date
           OR c.claim_date > p.end_date
    """)

    print("Claims outside policy dates:", cursor.fetchone()[0])

    cursor.execute("""
        SELECT COUNT(*)
        FROM claims c
        JOIN policies p ON c.policy_id = p.policy_id
        WHERE c.claim_amount > p.coverage_amount
    """)

    print("Claims above coverage:", cursor.fetchone()[0])

    cursor.execute("PRAGMA foreign_key_check")
    print("Foreign key errors:", len(cursor.fetchall()))

finally:
    connection.close()
import sqlite3
import hashlib
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance_test.db"


def get_data_hash():
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()
        digest = hashlib.sha256()

        queries = {
            "customers": """
                SELECT customer_id, full_name, email, phone
                FROM customers ORDER BY customer_id
            """,
            "policies": """
                SELECT policy_id, customer_id, policy_number,
                       policy_type, start_date, end_date,
                       coverage_amount, premium_amount, status
                FROM policies ORDER BY policy_id
            """,
            "claims": """
                SELECT claim_id, policy_id, claim_number,
                       claim_date, claim_amount, claim_status
                FROM claims ORDER BY claim_id
            """
        }

        for table, query in queries.items():
            cursor.execute(query)

            for row in cursor.fetchall():
                digest.update(
                    (table + repr(row)).encode("utf-8")
                )

        return digest.hexdigest()

    finally:
        connection.close()


if __name__ == "__main__":
    print("Dataset hash:")
    print(get_data_hash())
import sqlite3
import hashlib
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


def get_data_hash(db_path):
    connection = sqlite3.connect(db_path)

    try:
        digest = hashlib.sha256()

        for table, query in {
            "customers": "SELECT customer_id, full_name, email, phone FROM customers ORDER BY customer_id",
            "policies": "SELECT policy_id, customer_id, policy_number, policy_type, start_date, end_date, coverage_amount, premium_amount, status FROM policies ORDER BY policy_id",
            "claims": "SELECT claim_id, policy_id, claim_number, claim_date, claim_amount, claim_status FROM claims ORDER BY claim_id"
        }.items():
            for row in connection.execute(query):
                digest.update((table + repr(row)).encode("utf-8"))

        return digest.hexdigest()

    finally:
        connection.close()


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(BASE_DIR))

    from data.generate_data import main

    with tempfile.TemporaryDirectory() as temp_dir:
        test_db = Path(temp_dir) / "insurance_test.db"

        main(db_path=test_db)
        first_hash = get_data_hash(test_db)

        main(db_path=test_db)
        second_hash = get_data_hash(test_db)

        print("\nFirst hash:", first_hash)
        print("Second hash:", second_hash)

        if first_hash == second_hash:
            print("\nPASS: Dataset is reproducible!")
        else:
            print("\nFAIL: Dataset is not reproducible!")
            raise SystemExit(1)
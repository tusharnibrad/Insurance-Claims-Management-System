import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "insurance.db"


def calculate_settlements():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT claim_id, claim_amount, claim_status
            FROM claims
        """)

        claims = cursor.fetchall()

        total_reserve = 0
        total_settlement = 0

        for claim_id, amount, status in claims:

            if status == "Approved":
                reserve = amount * 0.10
                settlement = amount

            elif status == "Pending":
                reserve = amount
                settlement = 0

            else:
                reserve = 0
                settlement = 0

            total_reserve += reserve
            total_settlement += settlement

        print("Settlement Summary")
        print("------------------")
        print(f"Total claims: {len(claims)}")
        print(f"Total reserve: {total_reserve:.2f}")
        print(f"Total settlement: {total_settlement:.2f}")

    finally:
        connection.close()


if __name__ == "__main__":
    calculate_settlements()
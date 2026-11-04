import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "insurance.db"
EXPORT_DIR = BASE_DIR / "exports"


def export_data():
    EXPORT_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    tables = [
        "customers",
        "policies",
        "claims",
        "documents",
        "payments"
    ]

    try:
        for table in tables:
            df = pd.read_sql_query(
                f"SELECT * FROM {table}", connection
            )

            df.to_csv(
                EXPORT_DIR / f"{table}.csv",
                index=False
            )

            df.to_json(
                EXPORT_DIR / f"{table}.json",
                orient="records",
                indent=4
            )

            print(f"{table}: CSV and JSON exported")

    finally:
        connection.close()


if __name__ == "__main__":
    export_data()
    
def export_sql():
    connection = sqlite3.connect(DB_PATH)

    try:
        sql_data = "\n".join(
            connection.iterdump()
        )

        sql_path = EXPORT_DIR / "insurance_export.sql"
        sql_path.write_text(sql_data, encoding="utf-8")

        print("SQL export completed successfully!")

    finally:
        connection.close()
        
if __name__ == "__main__":
    export_data()
    export_sql()
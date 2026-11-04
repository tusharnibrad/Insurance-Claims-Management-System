import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).parent
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "insurance.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


# Create database
def create_database():
    DATABASE_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")

        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        connection.executescript(schema)
        connection.commit()

        print("Database created successfully!")

    finally:
        connection.close()


# Verify database tables
def verify_tables():
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )

        tables = cursor.fetchall()
        print("\nRecord counts:")

        for table_name in ["customers", "policies", "claims"]:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"{table_name}: {count}")

    finally:
        connection.close()


# Main execution
if __name__ == "__main__":
    create_database()
    verify_tables()
    


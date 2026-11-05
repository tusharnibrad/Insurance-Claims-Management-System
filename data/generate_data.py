
import sqlite3
import random
from pathlib import Path
from datetime import date, timedelta

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"

SEED = 42


def generate_customers(cursor):
    first_names = [
        "Amit", "Rahul", "Priya", "Sneha", "Rohan",
        "Neha", "Vikas", "Pooja", "Ankit", "Kavita"
    ]

    last_names = [
        "Sharma", "Patil", "Verma", "Gupta", "Joshi",
        "Deshmukh", "Khan", "Singh", "More"
    ]

    customers = []

    for customer_id in range(1, 101):
        name = (
            f"{random.choice(first_names)} "
            f"{random.choice(last_names)}"
        )
        email = f"customer{customer_id}@example.com"
        phone = f"9{random.randint(100000000, 999999999)}"

        customers.append((
            customer_id, name, email, phone
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO customers
        (customer_id, full_name, email, phone)
        VALUES (?, ?, ?, ?)
    """, customers)

    print("100 customers processed.")


def generate_policies(cursor):
    policies = []
    policy_types = ["Health", "Life", "Vehicle", "Property"]

    for policy_id in range(1, 2001):
        customer_id = random.randint(1, 100)
        policy_type = random.choice(policy_types)

        start_year = random.randint(2024, 2026)
        start_date = date(start_year, 1, 1)
        end_date = date(start_year + 1, 12, 31)

        coverage = random.randint(100000, 10000000)
        premium = round(
            coverage * random.uniform(0.01, 0.05), 2
        )

        status = random.choice(
            ["Active", "Expired", "Cancelled"]
        )

        policies.append((
            policy_id,
            customer_id,
            f"POL-{policy_id:05d}",
            policy_type,
            start_date.isoformat(),
            end_date.isoformat(),
            coverage,
            premium,
            status
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO policies
        (policy_id, customer_id, policy_number, policy_type,
         start_date, end_date, coverage_amount, premium_amount, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, policies)

    print("2000 policies processed.")


def generate_claims(cursor):
    cursor.execute("""
        SELECT policy_id, start_date, end_date, coverage_amount
        FROM policies
    """)

    policies = cursor.fetchall()
    claims = []

    for claim_id in range(1, 1001):
        policy_id, start_date, end_date, coverage = random.choice(
            policies
        )

        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)

        days = (end - start).days
        claim_date = start + timedelta(
            days=random.randint(0, days)
        )

        claim_amount = round(
            random.uniform(5000, float(coverage)), 2
        )

        claim_status = random.choice([
            "Submitted", "Approved", "Rejected", "Pending"
        ])

        claims.append((
            claim_id,
            policy_id,
            f"CLM-{claim_id:05d}",
            claim_date.isoformat(),
            claim_amount,
            claim_status
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO claims
        (claim_id, policy_id, claim_number, claim_date,
         claim_amount, claim_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, claims)

    print("1000 claims processed.")


def main():
    random.seed(SEED)

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        cursor = connection.cursor()

        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            schema = file.read()

        connection.executescript(schema)
                # Clear existing synthetic records before regeneration
        cursor.execute("DELETE FROM payments")
        cursor.execute("DELETE FROM documents")
        cursor.execute("DELETE FROM claims")
        cursor.execute("DELETE FROM policies")
        cursor.execute("DELETE FROM customers")

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
        """)
        print("Tables found:", cursor.fetchall())
        print("Database path:", DB_PATH)

        generate_customers(cursor)
        generate_policies(cursor)
        generate_claims(cursor)

        connection.commit()
        print("Data generation completed successfully!")

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()

import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance.db"

random.seed(42)


def generate_customers():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    first_names = ["Amit", "Rahul", "Priya", "Sneha", "Rohan",
                   "Neha", "Vikas", "Pooja", "Ankit", "Kavita"]

    last_names = ["Sharma", "Patil", "Verma", "Gupta", "Joshi",
                  "Deshmukh", "Nibrad", "Khan", "Singh", "More"]

    customers = []

    for customer_id in range(1, 101):
        name = random.choice(first_names) + " " + random.choice(last_names)
        email = f"customer{customer_id}@example.com"
        phone = f"9{random.randint(100000000, 999999999)}"

        customers.append((customer_id, name, email, phone))

    cursor.executemany(
        """
        INSERT OR IGNORE INTO customers
        (customer_id, full_name, email, phone)
        VALUES (?, ?, ?, ?)
        """,
        customers
    )

    connection.commit()
    connection.close()

    print("100 customers generated successfully!")


if __name__ == "__main__":
    generate_customers()
    
def generate_policies():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    policies = []

    policy_types = ["Health", "Life", "Vehicle", "Property"]

    for policy_id in range(1, 2001):
        customer_id = random.randint(1, 100)
        policy_type = random.choice(policy_types)

        start_year = random.randint(2024, 2026)
        start_date = f"{start_year}-01-01"
        end_date = f"{start_year + 1}-12-31"

        coverage = random.randint(100000, 10000000)
        premium = round(coverage * random.uniform(0.01, 0.05), 2)

        status = random.choice(["Active", "Expired", "Cancelled"])

        policies.append((
            policy_id,
            customer_id,
            f"POL-{policy_id:05d}",
            policy_type,
            start_date,
            end_date,
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

    connection.commit()
    connection.close()

    print("2000 policies generated successfully!")
    
if __name__ == "__main__":
    generate_customers()
    generate_policies()
    
def generate_claims():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    claims = []

    for claim_id in range(1, 1001):
        policy_id = random.randint(1, 2000)
        claim_date = (
            f"{random.randint(2024, 2026)}-"
            f"{random.randint(1, 12):02d}-"
            f"{random.randint(1, 28):02d}"
        )

        claim_amount = round(random.uniform(5000, 500000), 2)
        claim_status = random.choice(
            ["Submitted", "Approved", "Rejected", "Pending"]
        )

        claims.append((
            claim_id,
            policy_id,
            f"CLM-{claim_id:05d}",
            claim_date,
            claim_amount,
            claim_status
        ))

    cursor.executemany("""
        INSERT OR IGNORE INTO claims
        (claim_id, policy_id, claim_number, claim_date,
         claim_amount, claim_status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, claims)

    connection.commit()
    connection.close()

    print("1000 claims generated successfully!")
    
if __name__ == "__main__":
    generate_customers()
    generate_policies()
    generate_claims()
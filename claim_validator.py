import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "database" / "insurance.db"


def validate_claim(claim_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT
                c.claim_id,
                c.claim_date,
                c.claim_amount,
                p.policy_number,
                p.start_date,
                p.end_date,
                p.coverage_amount,
                p.status
            FROM claims c
            JOIN policies p ON c.policy_id = p.policy_id
            WHERE c.claim_id = ?
        """, (claim_id,))

        result = cursor.fetchone()

        if result is None:
            return "Invalid: Claim not found"

        (
            claim_id, claim_date, claim_amount,
            policy_number, start_date, end_date,
            coverage_amount, status
        ) = result

        if status != "Active":
            return "Ineligible: Policy is not active"

        if not start_date <= claim_date <= end_date:
            return "Ineligible: Claim date outside policy period"

        if claim_amount > coverage_amount:
            return "Ineligible: Claim exceeds coverage amount"

        return "Eligible: Claim passed validation"

    finally:
        connection.close()


if __name__ == "__main__":
    print(validate_claim(1))
    
def check_duplicate_claim(claim_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT policy_id, claim_date, claim_amount
            FROM claims
            WHERE claim_id = ?
        """, (claim_id,))

        claim = cursor.fetchone()

        if claim is None:
            return "Claim not found"

        cursor.execute("""
            SELECT COUNT(*)
            FROM claims
            WHERE policy_id = ?
              AND claim_date = ?
              AND claim_amount = ?
              AND claim_id != ?
        """, (*claim, claim_id))

        count = cursor.fetchone()[0]

        if count > 0:
            return "Duplicate claim detected"

        return "No duplicate claim found"

    finally:
        connection.close()
        
if __name__ == "__main__":
    print(validate_claim(1))
    print(check_duplicate_claim(1))
    
def check_missing_documents(claim_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    required_documents = [
        "Identity Proof",
        "Policy Copy",
        "Claim Form"
    ]

    try:
        cursor.execute("""
            SELECT document_type
            FROM documents
            WHERE claim_id = ?
              AND document_status = 'Submitted'
        """, (claim_id,))

        submitted = {row[0] for row in cursor.fetchall()}

        missing = [
            doc for doc in required_documents
            if doc not in submitted
        ]

        if missing:
            return "Missing documents: " + ", ".join(missing)

        return "All required documents submitted"

    finally:
        connection.close()
        

if __name__ == "__main__":
    print(validate_claim(1))
    print(check_duplicate_claim(1))
    print(check_missing_documents(1))
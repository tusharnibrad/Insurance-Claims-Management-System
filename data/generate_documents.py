import sqlite3
import random
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance.db"

random.seed(42)


def generate_documents():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    document_types = [
        "Identity Proof",
        "Policy Copy",
        "Claim Form"
    ]

    documents = []
    document_id = 1

    for claim_id in range(1, 1001):

        for document_type in document_types:

            status = random.choices(
                ["Submitted", "Missing"],
                weights=[80, 20]
            )[0]

            documents.append((
                document_id,
                claim_id,
                document_type,
                status
            ))

            document_id += 1

    cursor.executemany("""
        INSERT OR IGNORE INTO documents
        (document_id, claim_id, document_type, document_status)
        VALUES (?, ?, ?, ?)
    """, documents)

    connection.commit()

    print(f"{len(documents)} document records processed!")

    cursor.execute("""
        SELECT document_status, COUNT(*)
        FROM documents
        GROUP BY document_status
    """)

    print("\nDocument Status Summary:")

    for row in cursor.fetchall():
        print(f"{row[0]}: {row[1]}")

    connection.close()


if __name__ == "__main__":
    generate_documents()
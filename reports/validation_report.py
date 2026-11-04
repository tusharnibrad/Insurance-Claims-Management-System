import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "database" / "insurance.db"
EXPORT_DIR = BASE_DIR / "exports"


def generate_report():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    report = []

    try:
        report.append("INSURANCE CLAIMS MANAGEMENT SYSTEM")
        report.append("DATABASE VALIDATION REPORT")
        report.append("=" * 45)

        expected_counts = {
            "customers": 100,
            "policies": 2000,
            "claims": 1000
        }

        report.append("\nRECORD COUNTS")

        for table, expected in expected_counts.items():
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            actual = cursor.fetchone()[0]

            status = "PASS" if actual == expected else "FAIL"

            report.append(
                f"{table}: {actual} (Expected: {expected}) - {status}"
            )

        report.append("\nDUPLICATE CHECKS")

        cursor.execute("""
            SELECT COUNT(*) FROM (
                SELECT claim_number
                FROM claims
                GROUP BY claim_number
                HAVING COUNT(*) > 1
            )
        """)

        duplicates = cursor.fetchone()[0]

        report.append(
            f"Duplicate claim numbers: {duplicates}"
        )

        report.append("\nFOREIGN KEY CHECK")

        cursor.execute("PRAGMA foreign_key_check")
        fk_errors = cursor.fetchall()

        report.append(f"Foreign key errors: {len(fk_errors)}")

        report.append("\nDOCUMENT STATUS")

        cursor.execute("""
            SELECT document_status, COUNT(*)
            FROM documents
            GROUP BY document_status
        """)

        for status, count in cursor.fetchall():
            report.append(f"{status}: {count}")

        report.append("\nEXPORT FILE CHECK")

        for filename in [
            "customers.csv",
            "policies.csv",
            "claims.csv",
            "documents.csv",
            "payments.csv",
            "insurance_export.sql"
        ]:
            exists = (EXPORT_DIR / filename).exists()
            report.append(
                f"{filename}: {'PASS' if exists else 'FAIL'}"
            )

        report.append("\n" + "=" * 45)
        report.append("VALIDATION REPORT COMPLETED")

        report_text = "\n".join(report)

        report_path = BASE_DIR / "reports" / "validation_report.txt"
        report_path.write_text(report_text, encoding="utf-8")

        print(report_text)
        print("\nReport saved successfully!")

    finally:
        connection.close()


if __name__ == "__main__":
    generate_report()
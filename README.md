# Insurance Claims Management System

A Python and SQLite-based Insurance Claims Management System designed to manage insurance customers, policies, claims, documents, and settlement calculations.

## Project Overview

This project demonstrates a structured approach to insurance claim management using relational database design, synthetic data generation, claim validation, duplicate detection, document verification, and data exports.

## Key Features

- Relational database design using SQLite.
- Synthetic generation of 100 customers.
- Generation of 2,000 insurance policies.
- Generation of 1,000 insurance claims.
- Policy validation and claim eligibility checks.
- Duplicate claim detection.
- Missing document detection.
- Reserve and settlement calculations.
- CSV, JSON, and SQL exports.
- Database validation report.

## Technology Stack

- Python 3.13
- SQLite
- Pandas
- SQL
- CSV
- JSON
- Pytest

## Project Structure

Insurance-Claims-Management-System/
│
├── data/
│   ├── generate_data.py
│   ├── generate_documents.py
│   ├── verify_data.py
│   └── test_reproducibility.py
│
├── database/
│   └── schema.sql
│
├── reports/
│   └── validation_report.py
│
├── tests/
│   └── test_project.py
│
├── main.py
├── claim_validator.py
├── settlement_calculator.py
├── export_data.py
├── prompt_history.md
├── README.md
└── .gitignore

## Installation

Clone the repository:

    git clone https://github.com/tusharnibrad/Insurance-Claims-Management-System.git

Navigate to the project:

   cd Insurance-Claims-Management-System

Create a virtual environment:

    python -m venv venv

Activate on Windows:

    .\venv\Scripts\Activate.ps1

Install dependencies:

    pip install pandas pytest

## Running the Project

Create the database:

    python main.py

Generate customers, policies, and claims:

    python data/generate_data.py

Generate claim documents:

    python data/generate_documents.py

Validate claims:

    python claim_validator.py

Calculate settlements:

    python settlement_calculator.py

Export CSV, JSON, and SQL:

    python export_data.py

Generate validation report:

    python reports/validation_report.py

## Database Entities

1. Customers
2. Policies
3. Claims
4. Documents
5. Payments

## Synthetic Dataset

| Entity | Records |
|---|---:|
| Customers | 100 |
| Policies | 2,000 |
| Claims | 1,000 |
| Documents | 3,000 |

The synthetic document dataset contains:

- Submitted: 2,393
- Missing: 607

Random seed: 42

## Business Logic

### Claim Eligibility

Claims are checked against:

- Policy existence.
- Policy status.
- Policy validity dates.
- Coverage amount.

### Duplicate Detection

Claims are checked using policy ID, claim date, and claim amount.

### Document Verification

Required documents:

- Identity Proof
- Policy Copy
- Claim Form

### Reserve and Settlement

Current prototype assumptions:

- Approved claims: full claim amount as settlement and 10% reserve.
- Pending claims: full claim amount reserved.
- Rejected claims: zero reserve and zero settlement.

These are simplified demonstration rules, not actual insurance regulations.

## Validation Results

Latest local validation run:

- 100 customers: PASS
- 2,000 policies: PASS
- 1,000 claims: PASS
- Duplicate claim numbers: 0
- Foreign key errors: 0
- CSV exports: PASS
- SQL export: PASS

Run python reports/validation_report.py to generate the validation report.
## Limitations

- Synthetic data is used; no real customer information is included.
- Settlement rules are simplified assumptions.
- Six automated tests currently pass. Additional edge-case and integration test coverage can be added.
- Additional business rules and edge-case validation can be added.

## Future Improvements

- Automated unit and integration tests.
- Advanced claim fraud detection.
- Improved reserve estimation.
- More comprehensive policy eligibility rules.
- Interactive dashboard.
- Detailed audit logs.

## Disclaimer

This project is developed for educational and demonstration purposes.

It does not represent an actual insurance company's production system.
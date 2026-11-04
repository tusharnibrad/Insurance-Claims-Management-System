PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS policies (
    policy_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    policy_number TEXT UNIQUE NOT NULL,
    policy_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    coverage_amount REAL NOT NULL,
    premium_amount REAL NOT NULL,
    status TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE IF NOT EXISTS claims (
    claim_id INTEGER PRIMARY KEY,
    policy_id INTEGER NOT NULL,
    claim_number TEXT UNIQUE NOT NULL,
    claim_date TEXT NOT NULL,
    claim_amount REAL NOT NULL,
    claim_status TEXT NOT NULL,
    FOREIGN KEY (policy_id) REFERENCES policies(policy_id)
);

CREATE TABLE IF NOT EXISTS documents (
    document_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    document_type TEXT NOT NULL,
    document_status TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);

CREATE TABLE IF NOT EXISTS payments (
    payment_id INTEGER PRIMARY KEY,
    claim_id INTEGER NOT NULL,
    settlement_amount REAL NOT NULL,
    payment_date TEXT,
    payment_status TEXT NOT NULL,
    FOREIGN KEY (claim_id) REFERENCES claims(claim_id)
);
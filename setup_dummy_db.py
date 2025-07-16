import sqlite3

def setup_complex_dummy_db(db_path="dummy_financial.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop if exists
    cursor.execute("DROP TABLE IF EXISTS AdvisorTransaction")
    cursor.execute("DROP TABLE IF EXISTS FinancialAdvisor")

    # Create FinancialAdvisor table
    cursor.execute("""
        CREATE TABLE FinancialAdvisor (
            advisor_id INTEGER PRIMARY KEY,
            advisor_name TEXT NOT NULL,
            firm_name TEXT,
            advisor_status TEXT
        );
    """)

    # Create AdvisorTransaction table
    cursor.execute("""
        CREATE TABLE AdvisorTransaction (
            AdvisorTransaction_id INTEGER PRIMARY KEY,
            advisor_id INTEGER,
            date TEXT,
            sales_amt REAL,
            product_bought TEXT,
            FOREIGN KEY (advisor_id) REFERENCES FinancialAdvisor(advisor_id)
        );
    """)

    # Insert Financial Advisors
    advisors = [
        (1, "Alice Smith", "UBS", "Active"),
        (2, "Bob Johnson", "Wells Fargo", "Inactive"),
        (3, "Carol Patel", "LPL", "Active"),
        (4, "David Lee", "UBS", "Active"),
        (5, "Eva Martinez", "LPL", "Inactive")
    ]
    cursor.executemany("INSERT INTO FinancialAdvisor VALUES (?, ?, ?, ?);", advisors)

    # Insert AdvisorTransactions
    AdvisorTransactions = [
        (1001, 1, "2025-01-05", 150000.0, "ETF"),
        (1002, 1, "2025-03-10", 80000.0, "Mutual Fund"),
        (1003, 2, "2025-02-15", 50000.0, "ETF"),
        (1004, 3, "2025-01-25", 110000.0, "ETF"),
        (1005, 4, "2025-03-05", 95000.0, "Mutual Fund"),
        (1006, 4, "2025-01-18", 120000.0, "ETF"),
        (1007, 5, "2025-02-28", 43000.0, "ETF"),
        (1008, 3, "2025-03-15", 77000.0, "Mutual Fund"),
        (1009, 2, "2025-01-02", 61000.0, "ETF")
    ]
    cursor.executemany("INSERT INTO AdvisorTransaction VALUES (?, ?, ?, ?, ?);", AdvisorTransactions)

    conn.commit()
    conn.close()
    print("✅ Complex dummy database created.")

if __name__ == "__main__":
    setup_complex_dummy_db()

import csv
import zipfile
from datetime import datetime
from setup_dummy_db import setup_complex_dummy_db
from extract_metadata import extract_sqlite_metadata
from sql_generator import generate_sql
from sql_executor import execute_sql

TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = f"query_results_log_{TIMESTAMP}.csv"
ZIP_FILE = f"query_results_log_{TIMESTAMP}.zip"


TEST_QUERIES = [
    "What is the total ETF sales amount for each advisor in Q1 2025?",
    "How much total Mutual Fund was sold by advisors from UBS in February 2025?",
    "Show the total sales amount grouped by product type in Q1 2025.",
    "List the top 3 advisors by total sales amount in 2025.",
    "Which advisor had the highest ETF sales in January 2025?",
    "What is the total sales by each firm in 2025?",
    "Show the total Mutual Fund sales by active advisors only.",
    "How many transactions were made by inactive advisors?",
    "List the firms that have advisors with over ₹100,000 in ETF sales.",
    "Give me the total sales per firm for ETF products in March 2025.",
    "What are the total sales on each day in January 2025?",
    "How many transactions occurred in Q1 2025 per product?",
    "Show a breakdown of sales by month and product type.",
    "What is the average transaction size per advisor in February 2025?",
    "Which products were bought on or after March 1st, 2025?"
]

def run_pipeline(nl_query: str, writer):
    print(f"\n\U0001f9e0 Input Query: {nl_query}")

    # Step 3: Generate SQL using OpenAI
    sql = generate_sql(nl_query)
    print(f"\n\U0001f9fe Generated SQL:\n{sql}")

    # Step 4: Execute SQL and print result
    try:
        result = execute_sql(sql)
        print("\n📊 Result:")
        for row in result["rows"]:
            print(dict(zip(result["columns"], row)))

        # Log each row of result to CSV
        for row in result["rows"]:
            row_dict = dict(zip(result["columns"], row))
            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "query": nl_query,
                "generated_sql": sql,
                **row_dict
            })

    except Exception as e:
        print("\n❌ SQL Execution Error:", str(e))
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "query": nl_query,
            "generated_sql": sql,
            "error": str(e)
        })


if __name__ == "__main__":
    # Step 1: Create dummy DB
    setup_complex_dummy_db()

    # Step 2: Extract metadata JSON
    extract_sqlite_metadata()

    # Step 3: Run all test queries and log results
    with open(LOG_FILE, mode="w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["timestamp", "query", "generated_sql", "error", "advisor_id", "advisor_name", "firm_name", "advisor_status", "transaction_id", "date", "sales_amt", "product_bought"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for query in TEST_QUERIES:
            run_pipeline(query, writer)

    print(f"\n✅ All results logged to {LOG_FILE} and zipped as {ZIP_FILE}")
import sqlite3
import json

def extract_sqlite_metadata(db_path="dummy_financial.db", output_path="financial_metadata.json"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    metadata = {"tables": {}, "foreign_keys": []}

    for table in tables:
        if table.startswith("sqlite_"):
            continue

        cursor.execute(f"PRAGMA table_info({table});")
        columns_info = cursor.fetchall()
        metadata["tables"][table] = [
            {
                "column_name": col[1],
                "data_type": col[2],
                "primary_key": bool(col[5])
            }
            for col in columns_info
        ]

        cursor.execute(f"PRAGMA foreign_key_list({table});")
        for fk in cursor.fetchall():
            metadata["foreign_keys"].append({
                "from_table": table,
                "from_column": fk[3],
                "to_table": fk[2],
                "to_column": fk[4]
            })

    with open(output_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Metadata saved to {output_path}")
    conn.close()
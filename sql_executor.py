import sqlite3

def execute_sql(sql: str, db_path="dummy_financial.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()
    return {"columns": columns, "rows": rows}
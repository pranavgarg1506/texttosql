import json

def build_prompt(nl_query: str, metadata: dict) -> str:
    return f"""
You are an expert SQL assistant.

Given this SQLite database schema:

{json.dumps(metadata, indent=2)}

Write a syntactically correct SQLite SQL query for the following question:

{nl_query}

Only return the SQL query, no explanation.
"""
def clean_sql_query(query):
    """
    Removes Markdown code block syntax and other unwanted formatting from the SQL query.
    """
    query = query.strip()
    if query.startswith("```sql") or query.startswith("```"):
        query = query.replace("```sql", "").replace("```", "").strip()
    print(query)
    return query
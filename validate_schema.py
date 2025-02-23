import re

def extract_referenced_tables(query):
    """
    Extracts table names referenced in the SQL query.
    """
    pattern = r'\b(?:FROM|JOIN)\s+([a-zA-Z_][a-zA-Z0-9_]*)\b'
    matches = re.findall(pattern, query, re.IGNORECASE)
    return set(matches)

def extract_referenced_columns(query):
    """
    Extracts column references (e.g., table.column) from the SQL query.
    """
    # Regex pattern to match table.column references
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\b'
    matches = re.findall(pattern, query)
    return set(matches)

def extract_referenced_joins(query):
    """
    Extracts join conditions (e.g., table.column = foreign_table.foreign_column) from the SQL query.
    """
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)\b'
    matches = re.findall(pattern, query)
    return set(matches)

def normalize_join(join):
    """
    Normalizes a join tuple (table, column, foreign_table, foreign_column) for comparison.
    Ensures consistent ordering of tables and columns.
    """
    table, column, foreign_table, foreign_column = join
    # Ensure consistent ordering of tables (alphabetically)
    if table.lower() > foreign_table.lower():
        return (foreign_table.lower(), foreign_column.lower(), table.lower(), column.lower())
    return (table.lower(), column.lower(), foreign_table.lower(), foreign_column.lower())

def validate_table_names(schema_tables, referenced_tables):
    """
    Ensures all referenced table names in the query exist in the schema.
    """
    schema_tables_lower = {table.lower() for table in schema_tables}
    for table in referenced_tables:
        if table.lower() not in schema_tables_lower:
            print(f"Invalid table: {table}")
            return False
    return True


def extract_table_aliases(query):
    """
    Extracts table aliases from the SQL query and maps them to their actual table names.
    Handles both explicit (AS) and implicit aliases, including tables without aliases.
    """
    # Regex pattern to capture table and optional alias
    pattern = r'\b(?:FROM|JOIN)\s+(\w+)(?:\s+(?:AS\s+)?(\w+))?(\s|$)(?!ON)'
    matches = re.findall(pattern, query, flags=re.IGNORECASE)
    
    alias_mapping = {}
    for match in matches:
        table = match[0].lower()
        alias = match[1].lower() if match[1] else table
        alias_mapping[alias] = table
    
    return alias_mapping

def validate_column_names(schema_columns, referenced_columns, alias_mapping):
    """
    Validates columns using the alias mapping to resolve actual table names.
    """
    # Normalize schema columns for case-insensitive comparison
    normalized_schema_columns = {
        table.lower(): {col.lower() for col in cols}
        for table, cols in schema_columns.items()
    }
    
    # Validate each referenced column
    for alias, column in referenced_columns:
        # Resolve alias to actual table name
        actual_table = alias_mapping.get(alias.lower())
        if not actual_table:
            print(f"Invalid alias: {alias}")
            return False
            
        column_lower = column.lower()
        actual_table_lower = actual_table.lower()
        
        # Validate against schema
        if actual_table_lower not in normalized_schema_columns:
            print(f"Invalid table: {actual_table} (from alias {alias})")
            return False
            
        if column_lower not in normalized_schema_columns[actual_table_lower]:
            print(f"Invalid column: {alias}.{column} (resolved to {actual_table}.{column})")
            print(f"Available columns in {actual_table}: {normalized_schema_columns[actual_table_lower]}")
            return False
            
    return True

def validate_relationships(schema_relationships, referenced_joins, alias_mapping):
    """
    Ensures joins and relationships between tables are valid based on foreign keys.
    Handles both alias resolution and schema relationship format conversion.
    """
    converted_relationships = []
    for (table, column), (foreign_table, foreign_column) in schema_relationships.items():
        converted_relationships.append((table, column, foreign_table, foreign_column))

    # Normalize schema relationships
    schema_relationships_set = {
        normalize_join((table, column, foreign_table, foreign_column))
        for table, column, foreign_table, foreign_column in converted_relationships
    }

    # Resolve aliases in referenced joins
    resolved_joins = []
    for join in referenced_joins:
        table, col, foreign_table, foreign_col = join
        # Resolve aliases using alias_mapping
        resolved_table = alias_mapping.get(table.lower(), table)
        resolved_foreign_table = alias_mapping.get(foreign_table.lower(), foreign_table)
        resolved_joins.append((resolved_table, col, resolved_foreign_table, foreign_col))

    # Normalize referenced joins
    referenced_joins_set = {
        normalize_join((table, column, foreign_table, foreign_column))
        for table, column, foreign_table, foreign_column in resolved_joins
    }

    # Validate each referenced join
    for join in referenced_joins_set:
        if join not in schema_relationships_set:
            print(f"Invalid relationship: {join[0]}.{join[1]} = {join[2]}.{join[3]}")
            print(f"Allowed relationships: {schema_relationships_set}")
            return False

    return True



def validate_query(cleaned_query, schema_metadata):
    """
    Validates the SQL query against the schema metadata.
    """
    # Step 1: Extract referenced tables
    referenced_tables = extract_referenced_tables(cleaned_query)

    # Step 2: Validate table names
    if not validate_table_names(schema_metadata["tables"], referenced_tables):
        return "Error: Invalid table names in query."

    alias_mapping = extract_table_aliases(cleaned_query)
    referenced_columns = extract_referenced_columns(cleaned_query)
    
    # Validate column names with alias resolution
    if not validate_column_names(schema_metadata["columns"], referenced_columns, alias_mapping):
        return "Error: Invalid column names in query."
    
    referenced_joins = extract_referenced_joins(cleaned_query)
    
    # Step 4: Validate relationships
    if not validate_relationships(schema_metadata["relationships"], referenced_joins, alias_mapping):
        return "Error: Invalid table relationships in query."

    # If all validations pass, return the cleaned query
    return cleaned_query
import psycopg2

def get_schema_metadata():
    """
    Extracts schema metadata (tables, columns, relationships) from the Pagila database.
    """
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123456",
            host="localhost",  # Use "host.docker.internal" on Windows/macOS if needed
            port="5432"
        )
        cursor = conn.cursor()

        # Get all tables in the public schema
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public' and table_name NOT LIKE 'packages_%'; 
        """)
        tables = [row[0] for row in cursor.fetchall()]

        # Get all columns for each table
        cursor.execute("""
            SELECT table_name, column_name
            FROM information_schema.columns
            WHERE table_schema = 'public';
        """)
        columns_data = cursor.fetchall()

        columns = {}
        for table, column in columns_data:
            if table not in columns:
                columns[table] = []
            columns[table].append(column)

        # Get foreign key relationships
        cursor.execute("""
            SELECT
                tc.table_name,
                kcu.column_name,
                ccu.table_name AS foreign_table_name,
                ccu.column_name AS foreign_column_name
            FROM
                information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
            WHERE constraint_type = 'FOREIGN KEY';
        """)
        relationships = cursor.fetchall()

        # Convert relationships to a dictionary for easier lookup
        relationships_dict = {
            (table, column): (foreign_table, foreign_column)
            for table, column, foreign_table, foreign_column in relationships
        }

        # Validate metadata
        if not tables:
            print("No tables found in the schema.")
            return None

        if not all(columns.values()):
            print("Some tables have no columns. Check the schema metadata.")
            return None

        if not relationships:
            print("No foreign key relationships found. Check the schema metadata.")
            return None

        return {
            "tables": tables,
            "columns": columns,
            "relationships": relationships_dict
        }

    except Exception as e:
        print(f"Error retrieving schema metadata: {e}")
        return None

    finally:
        if conn:
            conn.close()
import psycopg2
from psycopg2 import OperationalError
from smolagents import Tool

class SQLTool(Tool):
    """
    A tool that executes SQL queries on the database.

    Args:
        query (str): A SQL query to execute.

    Returns:
        string: Query results as a string.
    """

    def __init__(self, db, user, password=None, port=5432, host="localhost",table_name=None, name=None, description=None, inputs=None, output_type=None):
        super().__init__()
        self.pg_conn_dict = {
            'dbname': db,
            'user': user,
            'password': password,
            'port': port,
            'host': host
        }
        self.name = name
        self.description = f"{description}\n{self.get_db_schema(table_name)}"
        self.inputs = inputs
        self.output_type = output_type

    def get_db_schema(self, table_name) -> str:
        try:
            conn = psycopg2.connect(**self.pg_conn_dict)
            cursor = conn.cursor()
        except OperationalError as e:
            print("Failed to connect to database")
            print(f"Error: {e}")
            return None

        query = f"""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = '{table_name}';
                """
        try:
            cursor.execute(query)
            columns = cursor.fetchall()
            conn.commit()
        except Exception as e:
            # TODO Implement logging for error handling
            columns = f"SQL Execution Error: {e}"
            return ""
        finally:
            conn.close()
        schema_lines = [f" - column name: {col[0]}, data type: {col[1]}, is nullable: {col[2]}" for col in columns]
        return f"Database Schema for '{table_name}':\n" + "\n".join(schema_lines)

    def is_safe_sql(self, sql: str) -> bool:
        """Only allow SELECT queries (basic safeguard)."""
        safe_keywords = ["select", "with"]  # Add CTE support
        sql_lower = sql.strip().lower()
        return any(sql_lower.startswith(kw) for kw in safe_keywords)
    
    def forward(self, query: str):
        if not self.is_safe_sql(query):
            return "❌ Unsafe SQL query detected. Only SELECT queries are allowed."
        
        conn = psycopg2.connect(**self.pg_conn_dict)
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            conn.commit()
        except Exception as e:
            results = f"SQL Execution Error: {e}"
        finally:
            conn.close()
        return str(results)
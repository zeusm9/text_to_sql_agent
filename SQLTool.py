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

    def __init__(self, db, user, password=None, port=5432, host="localhost",table_name=None, name=None, description=None, inputs=None, output_type=None, logger=None):
        super().__init__()
        self.pg_conn_dict = {
            'dbname': db,
            'user': user,
            'password': password,
            'port': port,
            'host': host
        }
        self.name = name
        self.logger = logger
        self.description = f"{description}\n{self.get_db_schema(table_name)}"
        self.inputs = inputs
        self.output_type = output_type

    def get_db_schema(self, table_name) -> str:
        try:
            conn = psycopg2.connect(**self.pg_conn_dict)
            cursor = conn.cursor()
        except OperationalError as e:
            self.logger.error("Failed to connect to database", exc_info=True)
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
            schema_lines = [f" - column name: {col[0]}, data type: {col[1]}, is nullable: {col[2]}" for col in columns]
            return f"Database Schema for '{table_name}':\n" + "\n".join(schema_lines)
        except Exception as e:
            self.logger.error("SQL Execution Error", exc_info=True)
            return None
        finally:
            if conn:
                conn.close()
        

    def is_safe_sql(self, sql: str) -> bool:
        """Only allow SELECT queries (basic safeguard)."""
        safe_keywords = ["select", "with"] 
        sql_lower = sql.strip().lower()
        return any(sql_lower.startswith(kw) for kw in safe_keywords)
    
    def forward(self, query: str):
        if not self.is_safe_sql(query):
            self.logger.error("❌ Unsafe SQL query detected. Only SELECT queries are allowed.")
            return None
        try:
            conn = psycopg2.connect(**self.pg_conn_dict)
            cursor = conn.cursor()
        except OperationalError as e:
            self.logger.error("Failed to connect to database", exc_info=True)
            return None
        try:
            cursor.execute(query)
            results = cursor.fetchall()
            conn.commit()
        except Exception as e:
            self.logger.error("SQL Execution Error", exc_info=True)
            return None
        finally:
            if conn:
                conn.close()
        return str(results)
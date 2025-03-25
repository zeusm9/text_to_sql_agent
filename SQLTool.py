import psycopg2
from smolagents import Tool

class SQLTool(Tool):
    """
    A tool that executes SQL queries on the 'certs' database.

    Args:
        query (str): A SQL query to execute.

    Returns:
        string: Query results as a string.
    """
    name = "sql_executor"
    description = (
        f"""
        This is an efficient and user-friendly tool designed to gather information about certificates contained in a SQL database.
        This tool can find the information of the certificates in the SQL database and return it in a readable format. 
        Rephrase the response in a human readable format without inserting the sql query or other dirty tokens.
        Considering the name of the table of the database is 'certs'. Use the sql_executor tool to run SQL
        queries on the certs table
        
        Few-Shot Example:
        Query:
        - show me the status of the certificate of the edge nodegraf.edge.panel.
        Action:
        - considering the name of the table  is "certs" and the node name is in the column "common_name", call tool with fist paremeter 'action' equal to 'execute_query' and second parameter 'query' equal to 'select status from certs where common_name = 'nodegraf.edge.panel''
        """
    )
    inputs = {
        "query": {
            "type": "string",
            "description": "A valid SQL query string."
        }
    }
    output_type = "string"

    def __init__(self, db, user, password, port, host):
        super().__init__()
        self.pg_conn_dict = {
            'dbname': db,
            'user': user,
            'password': password,
            'port': port,
            'host': host
        }

    def get_db_schema(self) -> str:
        conn = psycopg2.connect(**self.pg_conn_dict)
        cursor = conn.cursor()
        query = """
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_name = 'certs';
                """
        cursor.execute(query)
        columns = cursor.fetchall()
        conn.close()

        schema_lines = [f" - {col[1]} ({col[2]})" for col in columns]
        return f"SQLite Database Schema for 'certs':\n" + "\n".join(schema_lines)


    def forward(self, query: str):
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
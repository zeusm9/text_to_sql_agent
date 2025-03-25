import os
import yaml
from SQLTool import SQLTool
from dotenv import load_dotenv
from smolagents import ToolCallingAgent, LiteLLMModel, GradioUI

if __name__ == "__main__":
    load_dotenv()

model = LiteLLMModel(
    model_id="sambanova/Meta-Llama-3.3-70B-Instruct",
    api_base="https://api.sambanova.ai/v1",
    api_key=os.getenv("SAMBANOVA_API_KEY"),
    max_tokens=500
)

sql_tool = SQLTool(
    db=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT"),
    host=os.getenv("POSTGRES_HOST")
)

schema_description = sql_tool.get_db_schema()

agent = ToolCallingAgent(
    tools=[sql_tool],
    model=model,
    description=f"""
        This is an efficient and user-friendly tool designed to gather information about certificates contained in a SQL database.
        This tool can find the information of the certificates in the SQL database and return it in a readable format. 
        Rephrase the response in a human readable format without inserting the sql query or other dirty tokens.
        Considering the name of the table of the database is 'certs' and the table has
        the following schema: {schema_description}\nUse the sql_executor tool to run SQL
        queries on the certs table
        
        Few-Shot Example:
        Query:
        - show me the status of the certificate of the edge nodegraf.edge.panel.
        Action:
        - considering the name of the table  is "certs" and the node name is in the column "common_name", call tool with fist paremeter 'action' equal to 'execute_query' and second parameter 'query' equal to 'select status from certs where common_name = "nodegraf.edge.panel"'
        """
)

GradioUI(agent).launch()
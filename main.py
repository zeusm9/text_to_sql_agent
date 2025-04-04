import os
import logging
import sys
from SQLTool import SQLTool
from dotenv import load_dotenv
from smolagents import LiteLLMModel, GradioUI, CodeAgent

if __name__ == "__main__":
    logger = logging.getLogger("agent_logger")
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    load_dotenv()

    model = LiteLLMModel(
        model_id="sambanova/Meta-Llama-3.3-70B-Instruct",
        api_base="https://api.sambanova.ai/v1",
        api_key=os.getenv("SAMBANOVA_API_KEY"),
        temperature = 0,
        max_tokens=6000
    )

    tool_description =  f"""A tool designed to execute SQL queries on a structured database and return the results as a string. 
    It supports SELECT queries for data retrieval, including filtering, aggregation, and joins. 
    The tool processes queries efficiently and returns results in a human-readable string format. 
    Ensure queries are well-formed to prevent errors. Avoid SQL injection by properly handling input parameters.
    """

    tool_inputs = {
            "query": {
                "type": "string",
                "description": "A valid SQL query string."
            }
        }

    tool_output_type = "string"

    sql_tool = SQLTool(
        db=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT"),
        host=os.getenv("POSTGRES_HOST"),
        table_name= os.getenv("POSTGRES_TABLE_NAME"),
        name="sql_executor",
        description=tool_description,
        inputs=tool_inputs,
        output_type=tool_output_type,
        logger=logger
    )

    logger.info(f"The description of the toolw is the following:\n{sql_tool.description}")

    agent = CodeAgent(
        tools=[sql_tool],
        model=model
    )

    GradioUI(agent).launch()
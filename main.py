import os
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
    model=model
)

GradioUI(agent).launch()
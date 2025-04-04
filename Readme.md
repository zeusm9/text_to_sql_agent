# Text to SQL with SmolAgents

This project uses SmolAgents, a lightweight autonomous agent framework, to query a PostgreSQL database. The agent processes natural language queries and translates them into SQL queries to retrieve relevant data from the database.

Features
AI-powered querying: Users can ask questions in plain English, and the agent generates optimized SQL queries.

PostgreSQL integration: Connects to a Postgres database to retrieve structured information.

SmolAgents framework: Utilizes autonomous AI agents for query generation and data retrieval.

LLM deployment: Uses Sambanova Cloud for deploying a language model seamlessly.


## Usage
1. Set up a PostgreSQL database with certificate data.

2. Configure the database connection settings in your .env file.

3. Run the main.py to try your agent in GradioUI.

4. Receive structured responses with relevant information.

## Requirements

- Python 3.11.8
- smolagents
- psycopg2
- python-dotenv

## Install Requirements
```console
pip install -r requirements.txt
```
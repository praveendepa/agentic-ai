import sys
sys.path.append("src/")

from dotenv import load_dotenv

import agentic_ai.config as config

from agentic_ai.models.memory import Memory
from agentic_ai.functions.agent_orchestrator import agent_orchestrator
from agentic_ai.functions.sqldb_fn import setup_db


memory = Memory()
load_dotenv(".env")

# Setup database
setup_db(csv_file=config.csv_file, table_name=config.table_name, database=config.database)

def main():
    print("Welcome to the OpenAI Agent. Type 'exit' to quit.")
    while True:
        user_input = input("[User Prompt]: ")
        if user_input.lower() == 'exit':
            break
        response = agent_orchestrator(user_input)
        print(f"[Agent]: {response}")


if __name__ == "__main__":
    main()

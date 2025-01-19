import json

import agentic_ai.config as config

from agentic_ai.functions.sqldb_fn import get_conn, get_table_schema, get_db_schema



class PromptData:
    def __init__(self):
        self.test_var = []

        self.EXP_QUERY_TEMPLATE = json.dumps(
            {   'question': '[question]',
                'explanation': '[explain how the query is generated]',
                'query': '```[sql query]```'
            }, indent=4
        )
        
        self.FINAL_OUTPUT_TEMPLATE = json.dumps(
            {
                'question': '[question]',
                'explanation': '[explain how the query is generated]',
                'query': '```[sql query]```',
                'result': '[result]',
            }, indent=4
        )

        #self.table_name = "data_fct"
        #self.csv_file = "./data/superstore/superstore.csv"
        #self.database = "./data/database.db"
        conn = get_conn(db_file=config.database)

        # self.schema = get_table_schema(conn=conn, table_name=config.table_name)
        self.schema = get_db_schema(conn=conn)
        #self.schema = setup(self.csv_file, self.table_name, self.database)
        
    def get_table_prompt(self) -> str:
    # def get_table_prompt(self, self.schema: str, self.table_name: str) -> str:
        """ Writes a prompt to show information about the table """
        self.prompt = 'Your job is to write SQL queries on the following table.\n'
        self.prompt += f'Table name: {config.table_name}\n'
        self.prompt += f'Table schema:\n{self.schema}\n\n'
        self.prompt += '\n------------------------------------------------------\n'
        return self.prompt
    
    def get_db_prompt(self) -> str:
        """ Writes a prompt to show information about the tables in the database """
        self.prompt = 'Your job is to write SQL queries on the tables as described below.\n'
        self.prompt += f'\n{self.schema}\n\n'
        self.prompt += '\n------------------------------------------------------\n'
        return self.prompt
    
    def get_user_agent_prompt(self) -> str:
        self.prompt = self.get_db_prompt()
        self.prompt += 'You are SQL query writer for tables mentioned above. Below is a question input from a user. '
        self.prompt += 'Generate the query that pulls the necessary data to answer the question.\n\n'
        self.prompt += 'Return your answer by filling out the following template:\n'
        self.prompt += self.EXP_QUERY_TEMPLATE

        return self.prompt
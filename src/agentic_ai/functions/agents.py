import json
import pandas as pd
import requests

import agentic_ai.config as config

from agentic_ai.functions.ui_fn import converse
from agentic_ai.functions.sqldb_fn import get_conn
from agentic_ai.functions.llm_fn import parse_response_for_query

def get_current_weather(weather_key,location, unit="celsius"):
    # in this example, we will ignore the units parameter
    """Get the current weather in a given location"""
    # if "tokyo" in location.lower():
    #     return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    # elif "rome" in location.lower():
    #     return json.dumps({"location": "rome", "temperature": "72", "unit": unit})
    # elif "paris" in location.lower():
    #     return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    # else:
    #     return json.dumps({"location": location, "temperature": "unknown"})

    api_url = "http://api.weatherapi.com/v1/current.json?key={}&q={}".format(weather_key,location)
    response = requests.get(api_url)
    return json.dumps({"location": location, "temperature": response.json()['current']['temp_c']})


def get_vacation(user):
    if "john" in user.lower():
        return json.dumps({"vacation": "5 days"})
    if "mary" in user.lower():
        return json.dumps({"vacation": "10 days"})
    if "bob" in user.lower():
        return json.dumps({"vacation": "20 days"})
    else:
        return json.dumps({"vacation": "first tell me your name?"})
    
def get_price(name):
    if "milk" in name.lower():
        return json.dumps({"price": "1 usd"})
    if "beer" in name.lower():
        return json.dumps({"price": "10 usd"})
    if "eggs" in name.lower():
        return json.dumps({"price": "2 usd"})
    else:
        return json.dumps({"price": "first tell me the product?"})
    
def get_sales(question):
    #response = converse(question, memory.history)
    response = converse(question)

    question, explanation, query = parse_response_for_query(response.choices[0].message.content)

    query = query.strip().rstrip().replace('\n', ' ').replace('sql', ' ')

    print(question)
    print(query)
    result = pd.read_sql_query(query, get_conn(db_file=config.database))
    print(result)
    return json.dumps({"result": result.to_json()})
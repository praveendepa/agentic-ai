from openai import OpenAI
import json
import os

import agentic_ai.config as config

from agentic_ai.functions.agents import get_current_weather, get_price, get_sales, get_vacation


def agent_orchestrator(prompt):

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    messages = [{"role": "user", "content": prompt}]

    tools_list = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "get current weather for a city. City name is required",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "The city and state, e.g. San Francisco, CA",
                            },
                            "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                        },
                        "required": ["location"],
                    },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_vacation",
                "description": "get vacation in days for a user. User name is required",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user": {
                                "type": "string",
                                "description": "name of the user",
                            }
                        },
                        "required": ["user"],
                    },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_price",
                "description": "get price of a product. Product name is required",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "name of the product",
                            }
                        },
                        "required": ["name"],
                    },
            },
        },

        {
            "type": "function",
            "function": {
                "name": "get_sales",
                "description": "Call this when you detect the question is a query about sales data. Return the same user question ",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "question": {
                                "type": "string",
                                "description": "user question",
                            }
                        },
                        "required": ["question"],
                    },
            },
        }
    ]

    response = client.chat.completions.create(
        model=config.MODEL_NAME, messages=messages, tools=tools_list, tool_choice='auto')
    response_message = response.choices[0].message

    print(response_message)
    print(response_message.tool_calls)
    
    tool_calls = response_message.tool_calls
    # check if the model wants to call a function
    if tool_calls:
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_vacation": get_vacation,
            "get_price": get_price,
            "get_sales": get_sales,
        }  # you can have multiple functions here

        # extend conversation with assistant's reply
        messages.append(response_message)

        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            if function_name == 'get_vacation':
                function_response = function_to_call(
                    user=function_args.get("user"),
                )
            elif function_name == 'get_current_weather':
                function_response = function_to_call(
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
            elif function_name == 'get_price':
                function_response = function_to_call(
                    name=function_args.get("name"),
                )
            else: 
                function_response = function_to_call(
                    question=function_args.get("question"),
                )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function responsete

            print(messages)

            second_response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
            )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
    else:
        return response_message.content

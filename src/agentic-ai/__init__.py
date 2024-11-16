from openai import OpenAI
import openai
import requests
import json
import config

# Create an OpenAI client
#MODEL_NAME = "gpt-4o-2024-05-13"
MODEL_NAME = "gpt-3.5-turbo"
client = OpenAI(
    # this is also the default, it can be omitted
    api_key=config.OPENAI_API_KEY,
)


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


def agent_orchestrator(prompt):
    messages = [{"role": "user", "content": prompt}]

    weather_key = config.WEATHER_API_KEY

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
        }
    ]
    response = client.chat.completions.create(
        model=MODEL_NAME, messages=messages, tools=tools_list, tool_choice='auto')
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
                    weather_key,
                    location=function_args.get("location"),
                    unit=function_args.get("unit"),
                )
            else:
                function_response = function_to_call(
                    name=function_args.get("name"),
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
                model=MODEL_NAME,
                messages=messages,
            )  # get a new response from the model where it can see the function response
        return second_response.choices[0].message.content
    else:
        return response_message.content


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

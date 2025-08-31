import getpass
import os
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt import create_react_agent
    

load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

@tool
def add_numbers(a: int, b: int) -> int:
    """
    Adds two numbers.
    """
    return a + b

@tool
def multiply_numbers(a: int, b: int) -> int:
    """
    Multiplies two numbers.
    """
    return a * b

# Initialize the Anthropic chat model
model = ChatAnthropic(model='claude-sonnet-4-20250514')

agent = create_react_agent(model, tools=[add_numbers, multiply_numbers])

query = 'what is (9+9) multiplied by 9?'

response = agent.invoke({'messages':[('human', query)]})

print(response['messages'][-1].content)
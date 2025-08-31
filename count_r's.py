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
def count_r_in_word(word: str) -> int:
    """
    Counts the number of occurrences of the letter 'r' in a given word.
    """
    return word.lower().count('r')

# Initialize the Anthropic chat model
model = ChatAnthropic(model='claude-sonnet-4-20250514')
# Create the agent
app = create_react_agent(model=model, tools=[count_r_in_word])

# Create a query
query = "How many r's are in the word 'Terrarium'?"

# Invoke the agent and store the response
response = app.invoke({"messages": [("human", query)]})

# Print the agent's response
print(response['messages'][-1].content)
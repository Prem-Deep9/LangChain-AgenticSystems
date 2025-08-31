from langgraph.graph import START,END,StateGraph
from langgraph.graph.message import add_messages
from langchain_anthropic import ChatAnthropic
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
import getpass
import os
from IPython.display import display, Image
import IPython

load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

llm = ChatAnthropic(model='claude-sonnet-4-20250514')

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

def chatbot(State: State):
    return {'messages': [llm.invoke(State['messages'])]}

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({'messages': [("user", user_input)]}):
        for value in event.values():
            print('Agent', value['messages'])

user_query = 'Who is Lionel Messi?'
stream_graph_updates(user_query)

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except:
    print('Additional dependencies are required to display the graph.')

if IPython.get_ipython():
    display(Image(graph.get_graph().draw_mermaid_png()))
else:
    img_data = graph.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    print("Graph image saved as graph.png")
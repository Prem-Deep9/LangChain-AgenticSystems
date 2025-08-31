from langgraph.graph import START,END,StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_anthropic import ChatAnthropic
from typing import Annotated
from typing_extensions import TypedDict
from dotenv import load_dotenv
import getpass
import os
from IPython.display import display, Image
import IPython
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

llm = ChatAnthropic(model='claude-sonnet-4-20250514')

class State(TypedDict):
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

api_wrapper = WikipediaAPIWrapper(top_k_results=1)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
tools = [wikipedia_tool]
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    return {'messages': [llm_with_tools.invoke(state['messages'])]}

tool_node = ToolNode(tools=[wikipedia_tool])
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
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
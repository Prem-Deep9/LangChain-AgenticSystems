from getpass import getpass
import os
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun
from langgraph.graph import START,END,StateGraph, MessagesState
from IPython.display import display, Image
import IPython
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import AIMessage, HumanMessage


load_dotenv()

if "ANTHROPIC_API_KEY" not in os.environ:
    os.environ["ANTHROPIC_API_KEY"] = getpass.getpass("Enter your Anthropic API key: ")

llm = ChatAnthropic(model='claude-sonnet-4-20250514')

@tool
def date_checker(date: str) -> str:
    """Provide a list of important historical events that occurred on a date give in any format."""
    try:
        answer = llm.invoke(f"List important historical events that occurred on {date}.")
        return answer.content
    except Exception as e:
        return f"error retrieving events for date {date}: {str(e)}"
    
@tool
def check_palindrome(text: str):
    """Check if the given word or phrase is a palindrome."""
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    if cleaned == cleaned[::-1]:
        return f"The phrase or word {text} is a palindrome."
    else:
        return f"The phrase or word {text} is not a palindrome."
    
api_wrapper = WikipediaAPIWrapper(top_k_results=1)
wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    
#list of tools 
tools = [date_checker, check_palindrome, wikipedia_tool]
tool_node = ToolNode(tools)
model_with_tools = llm.bind_tools(tools)

def should_continue(state: MessagesState):
    last_message = state['messages'][-1]
    if last_message.tool_calls:
        return 'tools'
    return END

def call_model(state: MessagesState):
    last_message = state['messages'][-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return {'messages': [AIMessage(content=last_message.tool_calls[0]['response'])]}
    return {'messages': [model_with_tools.invoke(state['messages'])]}

workflow = StateGraph(MessagesState)
workflow.add_node('chatbot', call_model)
workflow.add_node('tools', tool_node)

workflow.add_edge(START, 'chatbot')

workflow.add_conditional_edges('chatbot', should_continue, ['tools', END])
workflow.add_edge('tools', 'chatbot')

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

if IPython.get_ipython():
    display(Image(app.get_graph().draw_mermaid_png()))
else:
    img_data = app.get_graph().draw_mermaid_png()
    with open("graph.png", "wb") as f:
        f.write(img_data)
    print("Graph image saved as graph.png")

config = {"configurable": { "thread_id": "1"}}
# Create input message with the user's query
def multi_tool_output(query):
    inputs = {"messages": [HumanMessage(content=query)]}
    # Stream messages and metadata from the chatbot application
    for msg, metadata in app.stream(inputs, config, stream_mode="messages"):
        if msg.content and not isinstance(msg, HumanMessage):
            print(msg.content, end='', flush=True)
    print("\n")

multi_tool_output("Is `may a moody baby doom a yam` a palindrome?")
multi_tool_output("What happened on 20th July, 1969?")
multi_tool_output("What happened on July 20th, 1995?")
multi_tool_output("Is 'A man, a plan, a canal, Panama' a palindrome?")

# def user_agent_multiturn(queries):
#     for query in queries:
#         print(f"User: {query}")
#         # Stream through messages corresponding to queries, excluding metadata
#         print("Agent: " + "".join(msg.content for msg, metadata in app.stream(
#                 {"messages": [HumanMessage(content=query)]}, config, stream_mode="messages") 
            
#             # Filter out the human messages to print agent messages
#             if msg.content and not isinstance(msg, HumanMessage)) + "\n")

# queries = ["Is `stressed desserts?` a palindrome?", "What about the word `kayak`?",
#     "What happened on the May 8th, 1945?", "What about 9 November 1989?"]
# user_agent_multiturn(queries) 
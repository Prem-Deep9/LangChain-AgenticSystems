# Langchain Agents Collection

A set of example agents and chatbots built using LangChain, LangGraph, and Anthropic Claude models. This repository demonstrates how to build custom tools, chatbots, and graph-based conversational flows with Python.

## Features

- **ReAct Math Agent**: Performs math operations (addition, multiplication) using custom tools and Anthropic Claude.
- **Multitool Agent**: Includes tools for checking historical events by date and palindrome detection.
- **Langgraph Chatbot**: Graph-based chatbot using LangGraph and Anthropic Claude.
- **Count R's Agent**: Counts the number of 'r' letters in a word.
- **Wikipedia Tool Chatbot**: Integrates Wikipedia search as a tool for answering questions.

## Setup

1. **Clone the repository**

2. **Create a virtual environment**
	uv venv

3. **Install dependencies**
	uv sync

4. **Set up your `.env` file**
	```
	ANTHROPIC_API_KEY=your_actual_api_key_here
	```

## Usage

Each script is self-contained. Run any agent script directly:

```sh
python ReAct-math-agent.py
python multitool-agent.py
python Langgraph-chatbot.py
python count_r's.py
python chatbot_wikipedia_tool.py
```

## Example Agents

### ReAct Math Agent

Performs math queries using custom tools.

### Multitool Agent

Provides historical events for a date and checks palindromes.

### Langgraph Chatbot

Graph-based conversational agent.

### Count R's Agent

Counts occurrences of 'r' in a word.

### Wikipedia Tool Chatbot

Answers questions using Wikipedia search.
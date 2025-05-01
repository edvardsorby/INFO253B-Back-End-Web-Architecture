from importlib import resources
from typing import Annotated

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.mongodb import AsyncMongoDBSaver
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from pymongo import AsyncMongoClient
from typing_extensions import TypedDict

from search.config import settings
from search.services.course_search import retrieve_courses_tool

#############
# Define graph components
#############

_llm = ChatOpenAI(model="gpt-4.1")
_tools = [retrieve_courses_tool]
_llm_with_tools = _llm.bind_tools(_tools)

with resources.files("search.services").joinpath("system_prompt.md").open() as f:
    _system_prompt = SystemMessage(f.read())


class State(TypedDict):
    messages: Annotated[list, add_messages]


tool_node = ToolNode(tools=_tools)


def chat_node(state: State):
    return {"messages": [_llm_with_tools.invoke([_system_prompt] + state["messages"])]}


async_mongodb_client = AsyncMongoClient(settings.mongo_uri_chat)
checkpointer = AsyncMongoDBSaver(async_mongodb_client)

#############
# Construct graph
#############

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chat_node)
graph_builder.add_node("tools", tool_node)

graph_builder.set_entry_point("chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

course_agent = graph_builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":
    with open("graph.png", "wb") as f:
        f.write(course_agent.get_graph().draw_mermaid_png())

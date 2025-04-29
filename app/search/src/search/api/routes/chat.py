from uuid import uuid4

from fastapi import APIRouter

from search.models import MessagesIn, MessagesOut
from search.services import course_agent

router = APIRouter(tags=["chat"])


@router.post("/chat")
async def agent(msg_in: MessagesIn) -> MessagesOut:
    conv_id = msg_in.conv_id
    if conv_id is None:
        conv_id = uuid4()

    config = {"configurable": {"thread_id": conv_id}}
    response = await course_agent.ainvoke(
        {"messages": [{"role": "user", "content": msg_in.query}]}, config
    )
    assistant_message = response["messages"][-1].content

    return {"response": assistant_message, "conv_id": conv_id}

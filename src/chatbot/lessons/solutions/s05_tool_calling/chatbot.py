import uuid
import requests
from enum import Enum
import datetime
from zoneinfo import ZoneInfo
from typing import override
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.services.llm import LLM


# a tool is a function exposed the LLM
# the model can request it to be called and the answer is returned as the reply
class TimeZone(Enum):
    America_NewYork = "America/New_York"
    Europe_London = "Europe/London"
    Europe_Warsaw = "Europe/Warsaw"
    Europe_Oslo = "Europe/Oslo"


@tool
def convert_time(
    time_24h: datetime.time, from_time_zone: TimeZone, to_time_zone: TimeZone
) -> str:
    """Converts today's time from one time zone to another.
    time: 'HH:MM[:SS]' (no timezone, no 'Z')
    Example: 10:00
    Returns ISO-8601 with offset, plus target time zone in brackets.
    """
    from_tz = ZoneInfo(from_time_zone.value)
    to_tz = ZoneInfo(to_time_zone.value)
    today = datetime.datetime.now(from_tz).date()
    date_time_24h = datetime.datetime.combine(today, time_24h, tzinfo=from_tz)
    return f"{date_time_24h.astimezone(to_tz).isoformat()} [{to_time_zone.value}]"


class Currency(Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    NOK = "NOK"


@tool
def convert_currency(
    amount: float, from_currency: Currency, to_currency: Currency
) -> float:
    """Converts money between currencies at today's rate."""
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency.value}&to={to_currency.value}"
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    data = response.json()
    answer = data["rates"][to_currency.value]
    return answer


# Chat bot implementation
class ChatBot(BaseChatBot):
    """Uses an LLM with tools"""

    def __init__(self):
        # vanilla language model
        llm = LLM()
        # list of tools at the model's disposal - they need to be decorated with @tool
        tools = [convert_time, convert_currency]
        # predefined tool calling agent in LangGraph
        # it resolves tool calls in a loop until none are requested
        # MemorySaver checkpointer automatically manages conversation history
        self._agent: CompiledStateGraph = create_agent(
            model=llm, tools=tools, checkpointer=MemorySaver()
        )
        self._thread_id = str(uuid.uuid4())

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        # Generate new thread ID to start fresh conversation
        self._thread_id = str(uuid.uuid4())

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")
        # Call the agent with new message
        # Checkpointer automatically loads previous messages and saves new ones
        # also pass ctx so that the agent can publish status updates on tool calls to the UI
        response = self._agent.invoke(
            {"messages": [HumanMessage(content=question)]},
            config={
                **self.get_config(ctx),
                "configurable": {"thread_id": self._thread_id},
            },
        )
        # extract the answer
        # multiple messages may have been generated, the last one is the final response
        answer = str(response["messages"][-1].content)

        return answer

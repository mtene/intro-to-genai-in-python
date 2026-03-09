import requests
import datetime
from enum import Enum
from zoneinfo import ZoneInfo
from typing import override
from langchain_core.tools import tool
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.chat_history import ChatHistory, assistant_message, user_message
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
        # TODO: study langchain.agents.create_agent
        # https://reference.langchain.com/python/langchain/agents/factory/create_agent
        # TODO: create an agent with tools (convert_time, convert_currency)
        self._agent = LLM()
        # Bonus TODO: replace with in-memory checkpointer
        self._chat_history = ChatHistory()

    @override
    def reset(self) -> None:
        """Reset chatbot to initial state"""
        # Bonus TODO: replace with changing thread_id for in-memory checkpointer
        self._chat_history.clear()

    @override
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        ctx.update_status("🧠 Thinking...")

        # record question in chat history
        # Bonus TODO: remove in favor of in-memory checkpointer
        self._chat_history.add_message(user_message(question))
        # call the agent with all historic messages
        response = self._agent.invoke(
            self._chat_history.messages, config=self.get_config(ctx)
        )
        # TODO: extract the answer from the response
        # Hint: the agent will return {"messages": [...]} - get the last message's content
        answer = str(response.content)
        # record answer in chat history
        # Bonus TODO: remove in favor of in-memory checkpointer
        self._chat_history.add_message(assistant_message(answer))

        return answer

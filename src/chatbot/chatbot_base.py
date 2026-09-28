import importlib
import inspect
from abc import ABC, abstractmethod
from pathlib import Path
from types import ModuleType
from langchain_core.runnables import RunnableConfig
from chatbot.chat_context import ChatContext


class BaseChatBot(ABC):
    """
    Chatbot base class serving as blueprint for all implementations.
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns the name of the directory holding the implementation, e.g. exercises.00_intro"""
        chatbot_path = Path(inspect.getfile(cls))
        lessons_path = Path(__file__).parent / "lessons"
        relative_path = chatbot_path.parent.relative_to(lessons_path)
        return ".".join(relative_path.parts)

    @classmethod
    def get_description(cls) -> str:
        """Returns the description of the implementation, extracted from the doc-comments"""
        return inspect.getdoc(cls) or ""

    @classmethod
    def get_config(cls, ctx: ChatContext, thread_id: str | None = None):
        if thread_id is None:
            thread_id = cls.get_name()
        return RunnableConfig(
            configurable={"thread_id": thread_id},
            callbacks=[ctx],
            recursion_limit=100,
        )

    def reset(self) -> None:
        """
        Reset chatbot to initial state.
        Subclasses must implement this to clear any stateful components.
        """
        pass

    @classmethod
    def get_test_module(cls) -> ModuleType | None:
        """Automatically discover and load tests.py in the same directory."""
        module_name = f"chatbot.lessons.{cls.get_name()}.tests"
        try:
            return importlib.import_module(module_name)
        except Exception:
            return None

    @abstractmethod
    def get_answer(self, question: str, ctx: ChatContext) -> str:
        """
        Produce the assistant's reply to the provided user question.
        Can use ctx to emit status updates, which will be displayed in the UI.
        """
        raise NotImplementedError

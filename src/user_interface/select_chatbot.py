import logging
from pathlib import Path
from chatbot.chatbot_base import BaseChatBot
import importlib
from typing import List

logger = logging.getLogger(__name__)


def list_chatbot_names() -> List[str]:
    """
    Discover chatbot implementations by scanning folders under chatbot/lessons
    Returns: a list of folder names
    """
    chatbot_names: List[str] = []
    root_path = Path(__file__).parent.parent / "chatbot" / "lessons"
    for subdir in root_path.rglob("*"):
        if subdir.is_dir() and (subdir / "chatbot.py").is_file():
            relative_path = subdir.relative_to(root_path)
            chatbot_name = ".".join(relative_path.parts)
            chatbot_names.append(chatbot_name)
    return chatbot_names


def load_chatbot(name: str) -> BaseChatBot | None:
    """Returns the given chatbot implementation"""
    module_name = f"chatbot.lessons.{name}.chatbot"
    try:
        # import the chatbot instance from the lessons' __main__.py
        module = importlib.import_module(module_name)
        chatbot_type = getattr(module, "ChatBot")
        chatbot = chatbot_type()
        logger.info(f"Successfully loaded chatbot from {module_name}")
        return chatbot
    except Exception:
        logger.exception(f"Unable to load chatbot implementation from {module_name}")
        return None

import logging
from typing import Type
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.start_chat import start_chat_services, stop_chat_services

logger = logging.getLogger(__name__)


def console(chatbot_type: Type[BaseChatBot]):
    start_chat_services()
    chatbot = chatbot_type()
    rich_console = Console()
    rich_console.print(
        f"\n[bold cyan]{chatbot.get_name()}[/bold cyan] console (type /quit to exit)"
    )
    try:
        while True:
            # user prompt with no newline
            rich_console.print(Text(">>> ", style="bold green"), end="")
            # read input
            question = input("")
            # stop if requested
            if question.strip() in {"/quit", "/exit"}:
                break
            # retrieve assistant answer
            ctx = ChatContext(
                status_update_func=lambda msg: rich_console.print(Text(msg))
            )
            answer = chatbot.get_answer(question, ctx)
            # assistant prompt
            rich_console.print(Panel(Markdown(answer)))
    except (KeyboardInterrupt, EOFError):
        print()
        logger.warning("Interrupted by user. Shutting down...")
    except Exception:
        logger.exception("Unhandled exception")
    finally:
        stop_chat_services()

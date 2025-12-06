import logging
from typing import Type
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from chatbot.chatbot_base import BaseChatBot
from chatbot.chat_context import ChatContext
from chatbot.testing.evaluator import ChatbotEvaluator
from chatbot.start_chat import start_chat_services, stop_chat_services

logger = logging.getLogger(__name__)


def handle_test_command(chatbot: BaseChatBot, rich_console: Console):
    """Run the test suite for the current chatbot."""
    test_suite = chatbot.get_test_suite()
    if test_suite is None:
        rich_console.print("[yellow]No test suite defined for this chatbot.[/yellow]")
        return

    evaluator = ChatbotEvaluator(chatbot)
    evaluator.run_test_suite(test_suite, rich_console)

    rich_console.print("[dim]Resetting chatbot state[/dim]")
    chatbot.reset()


def console(chatbot_type: Type[BaseChatBot]):
    start_chat_services()
    chatbot = chatbot_type()
    rich_console = Console()
    rich_console.print(
        f"\n[bold cyan]{chatbot.get_name()}[/bold cyan] console: type /quit to exit, /test to run tests"
    )
    try:
        while True:
            # user prompt with no newline
            rich_console.print(Text(">>> ", style="bold green"), end="")
            # read input
            question = input("")
            # evaluate command
            match question.strip():
                case "/quit" | "/exit":
                    break
                case "/test":
                    handle_test_command(chatbot, rich_console)
                    continue
            # retrieve assistant answer
            ctx = ChatContext(
                status_update_func=lambda msg: rich_console.print(Text(msg))
            )
            try:
                answer = chatbot.get_answer(question, ctx)
            except Exception as e:
                answer = repr(e)
                logger.exception(answer)
            # assistant prompt
            rich_console.print(Panel(Markdown(answer)))
    except (KeyboardInterrupt, EOFError):
        print()
        logger.warning("Interrupted by user. Shutting down...")
    except Exception:
        logger.exception("Unhandled exception")
    finally:
        stop_chat_services()

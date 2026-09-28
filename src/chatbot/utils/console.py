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
    """Run DeepEval suites declared in the chatbot's tests.py module."""
    module = chatbot.get_test_module()
    if module is None or not hasattr(module, "EVAL_SUITES"):
        rich_console.print("[yellow]No test suite defined for this chatbot.[/yellow]")
        return

    evaluator = ChatbotEvaluator(chatbot)
    evaluator.run(
        module.EVAL_SUITES,
        rich_console,
        repetitions=getattr(module, "EVAL_REPETITIONS", 1),
        min_pass_rate=getattr(module, "EVAL_MIN_PASS_RATE", 0.8),
    )


def console(chatbot_type: Type[BaseChatBot]):
    start_chat_services()
    chatbot = chatbot_type()
    rich_console = Console()
    rich_console.print(
        f"\n[bold cyan]{chatbot.get_name()}[/bold cyan] console: type /quit to exit, /test to run evaluations"
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
                case "/test" | "/eval":
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

from chatbot.utils.console import console
from .chatbot import ChatBot
from chatbot.utils.logging import configure_logging


def main():
    configure_logging()
    console(ChatBot)


if __name__ == "__main__":
    main()

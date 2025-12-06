from chatbot.utils.console import console
from chatbot.utils.logging import configure_logging
from .chatbot import ChatBot


def main():
    configure_logging()
    console(ChatBot)


if __name__ == "__main__":
    main()

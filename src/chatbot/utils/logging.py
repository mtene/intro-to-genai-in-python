import logging
from typing import List
from rich.logging import RichHandler
from chatbot.config import config


def configure_logging() -> None:
    errors: List[str] = []

    # get logging level from config
    config_log_level = config.get_log_level()
    log_level = logging.getLevelNamesMapping().get(config_log_level.upper())
    if log_level is None:
        log_level = logging.INFO
        errors.append(
            f"Invalid logging level '{config_log_level}', using '{logging.getLevelName(log_level).lower()}'"
        )

    # setup console log coloring handler
    handler = RichHandler(
        rich_tracebacks=True,  # Enable rich tracebacks
        show_time=False,  # Disable timestamps
        show_level=True,  # Show log levels
        show_path=False,  # Disable file path display
    )

    # configure logging
    logging.basicConfig(level=log_level, format="%(message)s", handlers=[handler])

    # suppress some the 3rd party packages INFO logging, to reduce clutter
    if log_level > logging.DEBUG:
        for logger_name in ["httpx", "mcp"]:
            logging.getLogger(logger_name).setLevel(logging.WARNING)

    # now that logging is setup, report any errors encountered
    if errors:
        logger = logging.getLogger(__name__)
        for error in errors:
            logger.error(error)

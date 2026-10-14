import logging
import sys
from pathlib import Path
from typing import List
from chatbot.utils.logging import configure_logging
from chatbot.utils.processes import run_on_this_process

logger = logging.getLogger(__name__)


def start_streamlit(argv: List[str] | None = None) -> int:
    streamlit_app_path = Path(__file__).parent / "app.py"
    streamlit_cmd = [
        "streamlit",
        "run",
        str(streamlit_app_path.resolve()),
        "--server.address",
        "127.0.0.1",
    ]
    if argv:
        streamlit_cmd += ["--"] + argv
    return run_on_this_process(cmd=streamlit_cmd)


def main() -> int:
    configure_logging()
    try:
        return start_streamlit()
    except Exception:
        logger.exception("Unhandled exception")
        return 1


if __name__ == "__main__":
    sys.exit(main())

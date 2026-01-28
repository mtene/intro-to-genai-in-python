import logging
import os
import subprocess
from urllib.parse import urlparse
from http.client import HTTPConnection
from typing import List, Dict

logger = logging.getLogger(__name__)


def is_endpoint_reachable(endpoint: str, timeout: float = 1.0) -> bool:
    conn = None
    try:
        parsed = urlparse(endpoint)
        host = parsed.hostname or "127.0.0.1"
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        path = parsed.path or ""
        conn = HTTPConnection(host=host, port=port, timeout=timeout)
        conn.request("HEAD", path)
        resp = conn.getresponse()
        # Any response code implies the server answered; 200..499 is enough to treat as reachable.
        return resp is not None
    except Exception:
        return False
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception:
                pass


def run_on_this_process(cmd: List[str], env: Dict[str, str] = os.environ.copy()) -> int:
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Shutting down...")
        return 130

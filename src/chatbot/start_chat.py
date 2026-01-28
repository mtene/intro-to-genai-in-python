import logging
import requests
from chatbot.config import config, ServiceType
from chatbot.utils.processes import run_on_this_process

logger = logging.getLogger(__name__)


def stop_chat_services():
    # stop any processes we spawned
    pass


def start_chat_services():
    # preload local services to avoid latency on first prompt
    service_configs = [config.get_llm_config(), config.get_embeddings_config()]
    service_endpoint_paths = ["api/generate", "api/embeddings"]
    service_endpoint_host = "127.0.0.1"
    service_endpoint_port = 11434
    service_test_payloads = [
        {"messages": [{"role": "user", "content": "Hi"}], "stream": False},
        {"input": "Hi"},
    ]
    for service_config, service_endpoint_path, service_test_payload in zip(
        service_configs, service_endpoint_paths, service_test_payloads
    ):
        if service_config["type"] == ServiceType.LOCAL:
            # download the model, if not present
            model = service_config["model"]
            cmd = ["ollama", "pull", model]
            exit_code = run_on_this_process(cmd=cmd)
            if exit_code != 0:
                logger.error(f"Failed to fetch model `{model}`: exit code {exit_code}")
            else:
                # send a dummy test query
                url = f"http://{service_endpoint_host}:{service_endpoint_port}/{service_endpoint_path}"
                payload = {"model": model, **service_test_payload}
                response = requests.post(url=url, json=payload, timeout=360)
                response.raise_for_status()

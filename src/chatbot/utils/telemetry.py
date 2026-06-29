import base64
import logging
import json
import os
from chatbot.config import config
from chatbot.utils.processes import is_endpoint_reachable
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor
from opentelemetry.instrumentation.chromadb import ChromaInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor


logger = logging.getLogger(__name__)


class Telemetry:
    """
    OpenTelemetry bootstrap
    """

    def __init__(self, service_name: str):
        self._service_name = service_name
        self._processor: BatchSpanProcessor | None = None
        self._started = False

    @staticmethod
    def _dump_object_to_span(span, obj, prefix):
        """Dump all public attributes of an object to span attributes"""
        try:
            for attr_name in dir(obj):
                if attr_name.startswith("_"):
                    continue
                try:
                    attr_value = getattr(obj, attr_name)
                    if callable(attr_value):
                        continue
                    # Serialize value
                    if isinstance(attr_value, (str, int, float, bool)):
                        value = attr_value
                    elif isinstance(attr_value, bytes):
                        try:
                            value = attr_value.decode("utf-8")
                        except Exception:
                            value = f"<bytes: {len(attr_value)} bytes>"
                    elif isinstance(attr_value, (dict, list, tuple)):
                        value = json.dumps(attr_value, indent=2)
                    else:
                        value = str(attr_value)

                    span.set_attribute(f"{prefix}.{attr_name}", value)
                except Exception:
                    pass
        except Exception as e:
            logger.debug(f"Failed to dump {prefix}: {e}")

    def start(self) -> None:
        if self._started:
            return
        obs_cfg = config.get_observability_config()
        endpoint = obs_cfg.get("endpoint")

        if not endpoint:
            logger.debug("No observability endpoint configured; traces disabled")
            return

        if not is_endpoint_reachable(endpoint):
            logger.debug(
                f"Could not reach observability endpoint {endpoint}, traces disabled"
            )
            return

        os.environ.setdefault(
            "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "true"
        )

        pub_env = obs_cfg.get("langfuse_public_key_env_var")
        sec_env = obs_cfg.get("langfuse_secret_key_env_var")
        pub_env = (
            pub_env.strip() if isinstance(pub_env, str) and pub_env.strip() else None
        )
        sec_env = (
            sec_env.strip() if isinstance(sec_env, str) and sec_env.strip() else None
        )
        if not pub_env or not sec_env:
            logger.error(
                "Langfuse telemetry auth is not configured in config.yaml. Traces disabled."
            )
            return

        pub = os.environ.get(pub_env)
        sec = os.environ.get(sec_env)
        if not pub or not sec:
            missing = [
                name for name, val in [(pub_env, pub), (sec_env, sec)] if not val
            ]
            logger.error(
                "Langfuse telemetry auth env vars are not set: "
                + ", ".join(missing)
                + ". Traces disabled."
            )
            return

        token = base64.b64encode(f"{pub}:{sec}".encode("utf-8")).decode("ascii")
        headers: dict[str, str] = {"Authorization": f"Basic {token}"}
        logger.info(
            f"Streaming traces to observability endpoint {endpoint} for service {self._service_name}"
        )

        provider = TracerProvider(
            resource=Resource.create({"service.name": self._service_name})
        )
        self._processor = BatchSpanProcessor(
            OTLPSpanExporter(endpoint=endpoint, headers=headers)
        )
        provider.add_span_processor(self._processor)
        trace.set_tracer_provider(provider)
        LangchainInstrumentor().instrument()
        OpenAIInstrumentor().instrument()
        ChromaInstrumentor().instrument()
        RequestsInstrumentor().instrument(
            request_hook=lambda span, request: self._dump_object_to_span(
                span, request, "http.request"
            ),
            response_hook=lambda span, request, response: self._dump_object_to_span(
                span, response, "http.response"
            ),
        )
        HTTPXClientInstrumentor().instrument(
            request_hook=lambda span, request: self._dump_object_to_span(
                span, request, "http.request"
            ),
            response_hook=lambda span, request, response: self._dump_object_to_span(
                span, response, "http.response"
            ),
        )
        self._started = True

    def stop(self) -> None:
        if not self._started:
            return
        if self._processor is not None:
            try:
                self._processor.force_flush()
            except Exception:
                pass
            try:
                self._processor.shutdown()
            except Exception:
                pass
        self._started = False

    def __enter__(self) -> "Telemetry":
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.stop()

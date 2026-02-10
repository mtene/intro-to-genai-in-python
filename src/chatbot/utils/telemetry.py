import logging
import json
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
                if attr_name.startswith('_'):
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
        endpoint = config.get_observability_endpoint()
        if not is_endpoint_reachable(endpoint):
            logger.debug(
                f"Could not reach observability endpoint {endpoint}, traces disabled"
            )
            return
        logger.info(
            f"Streaming traces to observability endpoint {endpoint} for service {self._service_name}"
        )

        provider = TracerProvider(
            resource=Resource.create({"service.name": self._service_name})
        )
        self._processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        provider.add_span_processor(self._processor)
        trace.set_tracer_provider(provider)
        LangchainInstrumentor().instrument()
        OpenAIInstrumentor().instrument()
        ChromaInstrumentor().instrument()
        RequestsInstrumentor().instrument(
            request_hook=lambda span, request: self._dump_object_to_span(span, request, "http.request"),
            response_hook=lambda span, request, response: self._dump_object_to_span(span, response, "http.response"),
        )
        HTTPXClientInstrumentor().instrument(
            request_hook=lambda span, request: self._dump_object_to_span(span, request, "http.request"),
            response_hook=lambda span, request, response: self._dump_object_to_span(span, response, "http.response"),
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

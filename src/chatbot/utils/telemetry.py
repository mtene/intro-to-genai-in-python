import logging
from chatbot.config import config
from chatbot.utils.processes import is_endpoint_reachable
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.langchain import LangchainInstrumentor
from opentelemetry.instrumentation.openai_v2 import OpenAIInstrumentor


logger = logging.getLogger(__name__)


class Telemetry:
    """
    OpenTelemetry bootstrap
    """

    def __init__(self, service_name: str):
        self._service_name = service_name
        self._processor: BatchSpanProcessor | None = None
        self._started = False

    def start(self) -> None:
        if self._started:
            return
        endpoint = config.get_observability_endpoint()
        if not is_endpoint_reachable(endpoint):
            logger.debug(
                f"Could not reach observability endpoint {endpoint}, traces disabled"
            )
            return
        logger.info(f"Streaming traces to observability endpoint {endpoint} for service {self._service_name}")

        provider = TracerProvider(
            resource=Resource.create({"service.name": self._service_name})
        )
        self._processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        provider.add_span_processor(self._processor)
        trace.set_tracer_provider(provider)
        LangchainInstrumentor().instrument()
        OpenAIInstrumentor().instrument()
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

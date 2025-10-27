import os
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader


from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
import logging

SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "react-agent")
OTLP_ENDPOINT = os.getenv("OTLP_EXPORTER_OTLP_ENDPOINT","http://localhost:4317")

resource = Resource.create({
    "service.name": SERVICE_NAME,
    "service.version": os.getenv("OTEL_SERVCIE_VERSION","0.1.0"),
    "deployment.environment": os.getenv("ENV","dev")

})


tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint=OTLP_ENDPOINT, insecure=True))
)
trace.set_tracer_provider(tracer_provider)

metrics_reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint=OTLP_ENDPOINT, insecure=True)
)

meter_provider = MeterProvider(resource=resource, metric_readers=[metrics_reader])
metrics.set_meter_provider(meter_provider)


logger_provider = LoggerProvider(resource=resource)
logger_provider.add_log_record_processor(
    BatchLogRecordProcessor(OTLPLogExporter(endpoint=OTLP_ENDPOINT, insecure=True))

)

otel_handler = LoggingHandler(level = logging.INFO, logger_provider = logger_provider)
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(otel_handler)


def instrument_requests():
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    RequestsInstrumentor().instrument()

def instrument_logginfg_context():

    from opentelemetry.instrumentation.logging import LoggingInstrumentor
    LoggingInstrumentor().instrument(set_logging_format=True)

def init_telemetry():
    instrument_requests()
    instrument_logginfg_context()
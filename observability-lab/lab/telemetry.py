import os
from typing import Callable

import httpx
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace.sampling import TraceIdRatioBased
from opentelemetry.semconv.resource import ResourceAttributes


def _endpoint() -> str:
    host = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "otel-collector:4318")
    if not host.startswith("http"):
        host = f"http://{host}"
    return host.rstrip("/")


def init_telemetry(service_name: str) -> Callable[[], None]:
    endpoint = _endpoint()
    resource = Resource.create({ResourceAttributes.SERVICE_NAME: service_name})

    trace_exporter = OTLPSpanExporter(endpoint=f"{endpoint}/v1/traces")
    tracer_provider = TracerProvider(
        resource=resource,
        sampler=TraceIdRatioBased(0.1),
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(trace_exporter))
    trace.set_tracer_provider(tracer_provider)

    metric_exporter = OTLPMetricExporter(endpoint=f"{endpoint}/v1/metrics")
    reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=15_000)
    meter_provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meter_provider)

    HTTPXClientInstrumentor().instrument()

    def shutdown() -> None:
        tracer_provider.shutdown()
        meter_provider.shutdown()

    return shutdown


def http_client(timeout: float = 30.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=timeout)

from opentelemetry import trace
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def run_jaeger(app):
    # Настройка провайдера трассировок и экспортера
    resource = Resource(attributes={SERVICE_NAME: "second_app"})
    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    # Настройка экспортера Jaeger
    jaeger_exporter = OTLPSpanExporter(
        endpoint="http://host.docker.internal:4318/v1/traces"
    )

    # Настройка обработчика спанов
    span_processor = BatchSpanProcessor(jaeger_exporter)
    provider.add_span_processor(span_processor)

    # Настройка пропагаторов для передачи контекста трассировок
    LoggingInstrumentor().instrument(set_logging_format=True)
    FastAPIInstrumentor.instrument_app(app, tracer_provider=provider)
    HTTPXClientInstrumentor().instrument()

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import Status, StatusCode, SpanKind

# TracerProvider is a factory for Tracers. Tracer Provider is initialized once and its lifecycle matches the application’s lifecycle.
# Tracer Provider initialization also includes Resource and Exporter initialization.
provider = TracerProvider()

# Trace Exporters send traces to a consumer e.g Otel Collector.
console_exporter = ConsoleSpanExporter()

# The BatchSpanProcessor processes spans in batches before they are exported. This is usually the right processor to use for an application.
# In contrast, the SimpleSpanProcessor processes spans as they are created.
# This means that if you create 5 spans, each will be processed and exported before the next span is created in code.
# This can be helpful in scenarios where you do not want to risk losing a batch, or if you’re experimenting with OpenTelemetry in development
processor = BatchSpanProcessor(console_exporter)
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# A Tracer creates spans containing more information about what is happening for a given operation, such as a request in a service.
# Tracers are created from Tracer Providers.
# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")


def sum(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def main():
    with tracer.start_as_current_span("main-sum", kind=SpanKind.INTERNAL) as span:
        # do some work that 'span' will track
        val_a = 10
        val_b = 15
        # Attributes are key-value pairs that contain metadata that you can use to
        # annotate a Span to carry information about the operation it is tracking.
        span.set_attributes({"method.name": "main", SpanAttributes.CODE_FUNCTION: "main"})

        # A Span Event can be thought of as a structured log message (or annotation) on a Span,
        # typically used to denote a meaningful, singular point in time during the Span’s duration.
        # An event is a human-readable message on a span that represents “something happening” during its lifetime.
        # Think of it as a primitive log.
        span.add_event("Summing values", {"log.level": "DEBUG", "val.a": val_a, "val.b": val_b})

        r = sum(val_a, val_b)
        span.add_event("Sum result", {"log.level": "DEBUG", "result": r})
        # When the 'with' block goes out of scope, 'span' is closed

    with tracer.start_as_current_span("main-div", kind=SpanKind.INTERNAL) as span:
        val_a = 10
        val_b = 0
        span.set_attributes({"method.name": "main", SpanAttributes.CODE_FUNCTION: "main"})
        span.add_event("Dividing values", {"log.level": "DEBUG", "val.a": val_a, "val.b": val_b})
        try:
            r = sum(val_a, val_b)
        except ZeroDivisionError as e:
            span.set_status(Status(StatusCode.ERROR))
            span.record_exception(e)
            span.add_event(
                str(e),
                {
                    "log.level": "DEBUG",

                },
            )


if __name__ == "__main__":
    main()

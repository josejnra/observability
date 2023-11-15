from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.sdk.resources import Resource

resource = Resource.create(attributes={"service.name": "metric-service-example"})

otlp_exporter = OTLPMetricExporter(endpoint="127.0.0.1:4317", insecure=True)
otlp_metric_reader = PeriodicExportingMetricReader(otlp_exporter)
console_metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[console_metric_reader, otlp_metric_reader], resource=resource)

# Sets the global default meter provider
metrics.set_meter_provider(provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter("my.meter.name")


def sum(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def main():
    work_counter = meter.create_counter(name="add_counter", unit="1", description="Counts the amount of work done")
    exception_counter = meter.create_counter(
        name="divide_exceptions", unit="1", description="number of exceptions caught"
    )

    sum(10, 15)
    work_counter.add(1)

    try:
        divide(10, 0)
    except ZeroDivisionError:
        exception_counter.add(1)


if __name__ == "__main__":
    main()

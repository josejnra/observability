import logging

from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource

resource = Resource.create(attributes={"service.name": "log-service-example"})
provider = LoggerProvider(resource=resource)

console_exporter = ConsoleLogExporter()
otlp_exporter = OTLPLogExporter(endpoint="127.0.0.1:4317", insecure=True)

set_logger_provider(provider)

provider.add_log_record_processor(BatchLogRecordProcessor(console_exporter))
provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
handler = LoggingHandler(logger_provider=provider)

# Attach OTLP handler to root logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def sum(a: int, b: int):
    return a + b


def divide(a: int, b: int):
    return a / b


def main():
    logging.info("Summing two values")
    r = sum(10, 15)
    logging.debug("Summing result: %s", r)

    try:
        logging.info("Dividing")
        r = divide(10, 0)
        logging.debug("Dividing result: %s", r)
    except ZeroDivisionError as e:
        logging.error("Division by zero: %s", e)


if __name__ == "__main__":
    main()
    provider.shutdown()

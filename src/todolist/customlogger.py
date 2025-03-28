import logging
from prometheus_client import Counter

# Define Prometheus counters for different log levels
log_counters = {
    'INFO': Counter('django_log_info_total', 'Total number of INFO logs'),
    'WARNING': Counter('django_log_warning_total', 'Total number of WARNING logs'),
    'ERROR': Counter('django_log_error_total', 'Total number of ERROR logs'),
}

class PrometheusLogHandler(logging.Handler):  # Custom log handler
    def emit(self, record):
        log_level = record.levelname  # Get the log level (INFO, WARNING, ERROR)
        if log_level in log_counters:  # Check if we have a counter for this level
            log_counters[log_level].inc()  # Increment the counter

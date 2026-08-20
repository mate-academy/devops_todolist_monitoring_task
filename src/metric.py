from prometheus_client import Counter, Histogram, Gauge
import time

# Лічильник запитів
request_count = Counter(
    'todoapp_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status']
)

# Час виконання запиту
request_duration = Histogram(
    'todoapp_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

# Активні подання
active_tasks = Gauge(
    'todoapp_active_tasks',
    'Number of active tasks'
)

# Помилки
errors = Counter(
    'todoapp_errors_total',
    'Total number of errors',
    ['error_type']
)
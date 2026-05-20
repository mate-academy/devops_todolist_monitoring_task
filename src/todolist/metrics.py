from prometheus_client import Counter

GET_REQUESTS = Counter(
    'django_get_requests_total',
    'Total number of GET requests'
)

POST_REQUESTS = Counter(
    'django_post_requests_total',
    'Total number of POST requests'
)
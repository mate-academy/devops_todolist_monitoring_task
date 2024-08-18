from prometheus_client import Counter

# Create counters for GET and POST requests
get_request_counter = Counter('django_custom_get_requests_total', 'Total number of GET requests')
post_request_counter = Counter('django_custom_post_requests_total', 'Total number of POST requests')

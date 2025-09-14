#!/bin/bash

# Test script to verify TodoApp metrics endpoint
# This script tests the /metrics endpoint and generates some sample data

set -e

echo "🧪 Testing TodoApp metrics endpoint..."

# Function to test metrics endpoint
test_metrics() {
    local url=$1
    local description=$2
    
    echo "Testing: $description"
    echo "URL: $url"
    
    # Test if endpoint is accessible
    if curl -s -f "$url" > /dev/null; then
        echo "✅ $description - Endpoint accessible"
        
        # Get metrics and check for our custom metrics
        metrics=$(curl -s "$url")
        
        if echo "$metrics" | grep -q "http_requests_total"; then
            echo "✅ Custom metrics found: http_requests_total"
        else
            echo "❌ Custom metrics not found: http_requests_total"
        fi
        
        if echo "$metrics" | grep -q "http_request_duration_seconds"; then
            echo "✅ Custom metrics found: http_request_duration_seconds"
        else
            echo "❌ Custom metrics not found: http_request_duration_seconds"
        fi
        
        # Show sample metrics
        echo "📊 Sample metrics:"
        echo "$metrics" | grep -E "(http_requests_total|http_request_duration_seconds)" | head -5
        echo ""
        
    else
        echo "❌ $description - Endpoint not accessible"
        return 1
    fi
}

# Function to generate test traffic
generate_traffic() {
    local base_url=$1
    local count=${2:-10}
    
    echo "🚀 Generating $count test requests..."
    
    for i in $(seq 1 $count); do
        # GET request
        curl -s "$base_url/" > /dev/null
        
        # POST request
        curl -s -X POST "$base_url/" -d "description=test-todo-$i" > /dev/null
        
        # API request
        curl -s "$base_url/api/" > /dev/null
        
        if [ $((i % 5)) -eq 0 ]; then
            echo "  Generated $i requests..."
        fi
    done
    
    echo "✅ Generated $count requests"
}

# Main execution
echo "Starting metrics testing..."

# Test different scenarios
if [ "$1" = "local" ]; then
    # Test local development server
    echo "Testing local development server..."
    test_metrics "http://localhost:8000/metrics" "Local Development Server"
    
elif [ "$1" = "k8s" ]; then
    # Test Kubernetes deployment
    echo "Testing Kubernetes deployment..."
    
    # Check if port-forward is running
    if ! pgrep -f "kubectl port-forward.*todoapp" > /dev/null; then
        echo "Starting port-forward for todoapp service..."
        kubectl port-forward svc/todoapp-service 8080:80 -n todoapp &
        PORT_FORWARD_PID=$!
        sleep 5
    fi
    
    test_metrics "http://localhost:8080/metrics" "Kubernetes Deployment"
    
    # Generate some traffic
    generate_traffic "http://localhost:8080" 20
    
    # Test again after traffic
    echo "Testing after generating traffic..."
    test_metrics "http://localhost:8080/metrics" "Kubernetes Deployment (After Traffic)"
    
    # Cleanup port-forward
    if [ ! -z "$PORT_FORWARD_PID" ]; then
        kill $PORT_FORWARD_PID 2>/dev/null || true
    fi
    
else
    echo "Usage: $0 [local|k8s]"
    echo ""
    echo "Examples:"
    echo "  $0 local    # Test local development server"
    echo "  $0 k8s      # Test Kubernetes deployment"
    echo ""
    echo "Prerequisites:"
    echo "  - For 'local': Run 'python manage.py runserver' in src/ directory"
    echo "  - For 'k8s':  Deploy to Kubernetes and ensure port-forward is available"
    exit 1
fi

echo ""
echo "🎉 Metrics testing completed!"
echo ""
echo "Next steps:"
echo "1. Check Prometheus targets: http://localhost:9090/targets"
echo "2. Import Grafana dashboard: grafana-dashboard.json"
echo "3. View metrics in Grafana: http://localhost:3000"

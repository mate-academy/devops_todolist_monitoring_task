#!/usr/bin/env python3
"""
Demo script to showcase TodoApp Prometheus metrics
This script demonstrates the metrics endpoint and generates sample data
"""

import requests
import time
import json
import sys
from urllib.parse import urljoin

def test_metrics_endpoint(base_url):
    """Test the metrics endpoint and display results"""
    metrics_url = urljoin(base_url, '/metrics')
    
    print(f"🔍 Testing metrics endpoint: {metrics_url}")
    
    try:
        response = requests.get(metrics_url, timeout=10)
        response.raise_for_status()
        
        print(f"✅ Status Code: {response.status_code}")
        print(f"✅ Content-Type: {response.headers.get('Content-Type', 'Not set')}")
        
        # Parse metrics
        metrics_text = response.text
        lines = metrics_text.split('\n')
        
        # Count different types of metrics
        http_metrics = [line for line in lines if 'http_requests_total' in line and not line.startswith('#')]
        duration_metrics = [line for line in lines if 'http_request_duration_seconds' in line and not line.startswith('#')]
        created_metrics = [line for line in lines if 'http_requests_created' in line and not line.startswith('#')]
        
        print(f"\n📊 Metrics Summary:")
        print(f"   HTTP Request Counters: {len(http_metrics)}")
        print(f"   Duration Histograms: {len(duration_metrics)}")
        print(f"   Creation Timestamps: {len(created_metrics)}")
        
        # Show sample metrics
        print(f"\n📈 Sample HTTP Request Metrics:")
        for metric in http_metrics[:5]:
            print(f"   {metric}")
        
        if len(http_metrics) > 5:
            print(f"   ... and {len(http_metrics) - 5} more")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Error accessing metrics endpoint: {e}")
        return False

def generate_traffic(base_url, num_requests=20):
    """Generate sample traffic to create metrics"""
    print(f"\n🚀 Generating {num_requests} sample requests...")
    
    endpoints = [
        ('/', 'GET'),
        ('/api/', 'GET'),
        ('/', 'POST'),
        ('/api/health', 'GET'),
        ('/api/ready', 'GET'),
    ]
    
    for i in range(num_requests):
        endpoint, method = endpoints[i % len(endpoints)]
        url = urljoin(base_url, endpoint)
        
        try:
            if method == 'GET':
                response = requests.get(url, timeout=5)
            else:  # POST
                response = requests.post(url, data={'description': f'test-todo-{i}'}, timeout=5)
            
            if i % 5 == 0:
                print(f"   Generated {i+1} requests...")
                
        except requests.exceptions.RequestException as e:
            print(f"   Warning: Request {i+1} failed: {e}")
    
    print(f"✅ Generated {num_requests} requests")

def show_prometheus_queries():
    """Display useful Prometheus queries for the metrics"""
    print(f"\n🔍 Useful Prometheus Queries:")
    print(f"   # Total request rate")
    print(f"   sum(rate(http_requests_total[5m]))")
    print(f"")
    print(f"   # Request rate by method")
    print(f"   sum(rate(http_requests_total[5m])) by (method)")
    print(f"")
    print(f"   # 95th percentile response time")
    print(f"   histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))")
    print(f"")
    print(f"   # Request rate by endpoint")
    print(f"   sum(rate(http_requests_total[5m])) by (endpoint, method)")

def main():
    if len(sys.argv) != 2:
        print("Usage: python demo-metrics.py <base_url>")
        print("Examples:")
        print("  python demo-metrics.py http://localhost:8000")
        print("  python demo-metrics.py http://localhost:30007")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    print("🎯 TodoApp Prometheus Metrics Demo")
    print("=" * 50)
    
    # Test initial metrics
    if not test_metrics_endpoint(base_url):
        print("❌ Cannot access metrics endpoint. Make sure the application is running.")
        sys.exit(1)
    
    # Generate traffic
    generate_traffic(base_url, 30)
    
    # Wait a moment for metrics to update
    print("\n⏳ Waiting for metrics to update...")
    time.sleep(2)
    
    # Test metrics again
    print("\n" + "=" * 50)
    print("📊 Metrics after generating traffic:")
    test_metrics_endpoint(base_url)
    
    # Show Prometheus queries
    show_prometheus_queries()
    
    print(f"\n🎉 Demo completed!")
    print(f"💡 Next steps:")
    print(f"   1. Import grafana-dashboard.json into Grafana")
    print(f"   2. Set up Prometheus to scrape {base_url}/metrics")
    print(f"   3. Create alerts based on the metrics")

if __name__ == "__main__":
    main()

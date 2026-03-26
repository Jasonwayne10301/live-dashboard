from prometheus_client import Gauge

# Prometheus metrics
cpu_gauge = Gauge('system_cpu_percent', 'CPU usage percentage', ['server'])
memory_gauge = Gauge('system_memory_percent', 'Memory usage percentage', ['server'])
disk_gauge = Gauge('system_disk_percent', 'Disk usage percentage', ['server'])
network_in_gauge = Gauge('system_network_in_mbps', 'Network in Mbps', ['server'])
network_out_gauge = Gauge('system_network_out_mbps', 'Network out Mbps', ['server'])
request_rate_gauge = Gauge('system_request_rate', 'Request rate per second', ['server'])
response_time_gauge = Gauge('system_response_time_ms', 'Response time in ms', ['server'])
active_connections_gauge = Gauge('system_active_connections', 'Active connections', ['server'])

import time
import collections
import psutil

# Data structure to keep track of network stats over time
network_stats = {
    'time': [],
    'bytes_sent': [],
    'bytes_recv': []
}

def bytes_to_mb_and_gb(bytes_value):
    mb = bytes_value / (1024 ** 2)
    gb = bytes_value / (1024 ** 3)
    return f"{mb:.3f} MB ({gb:.3f} GB)"

# Function to get the current network stats
def get_network_stats():
    net_io = psutil.net_io_counters()
    return {
        'bytes_sent': net_io.bytes_sent,
        'bytes_recv': net_io.bytes_recv 
    }

def fetch_network_metrics():
    # Network I/O Counters
    net_io_counters = psutil.net_io_counters(pernic=True)
    net_io_metrics = {}
    for nic, metrics in net_io_counters.items():
        net_io_metrics[nic] = {
            'bytes_sent': bytes_to_mb_and_gb(metrics.bytes_sent),
            'bytes_recv': bytes_to_mb_and_gb(metrics.bytes_recv),
            'packets_sent': metrics.packets_sent,
            'packets_recv': metrics.packets_recv,
            'errin': metrics.errin,
            'errout': metrics.errout,
            'dropin': metrics.dropin,
            'dropout': metrics.dropout,
        }

    # Network Interface Addresses
    net_if_addrs = psutil.net_if_addrs()
    net_if_addrs_metrics = {}
    for nic, addrs in net_if_addrs.items():
        net_if_addrs_metrics[nic] = [
            {
                'family': addr.family,
                'address': addr.address,
                'netmask': addr.netmask,
                'broadcast': addr.broadcast,
                'ptp': addr.ptp
            }
            for addr in addrs
        ]

    # Network Interface Statistics
    net_if_stats = psutil.net_if_stats()
    net_if_stats_metrics = {
        nic: {
            'isup': stats.isup,
            'duplex': stats.duplex,
            'speed': stats.speed,
            'mtu': stats.mtu
        }
        for nic, stats in net_if_stats.items()
    }

    return {
        'Network I/O Counters': net_io_metrics,
        'Network Interface Addresses': net_if_addrs_metrics,
        'Network Interface Statistics': net_if_stats_metrics
    }

# Function to count private and non-private connections and used ports
def analyze_connections():
    connections = psutil.net_connections()
    private_connections = 0
    non_private_connections = 0
    used_ports = collections.defaultdict(int)

    for conn in connections:
        if conn.raddr:
            used_ports[conn.laddr.port] += 1
            if conn.raddr.ip.startswith("192.168.") or conn.raddr.ip.startswith("10.") or conn.raddr.ip.startswith("172.16."):
                private_connections += 1
            else:
                non_private_connections += 1
    
    return private_connections, non_private_connections, used_ports

# Function to calculate bandwidth speed
def calculate_bandwidth_speed(duration_seconds=1):
    stats_start = get_network_stats()
    time.sleep(duration_seconds)
    stats_end = get_network_stats()

    bytes_sent_diff = stats_end['bytes_sent'] - stats_start['bytes_sent']
    bytes_recv_diff = stats_end['bytes_recv'] - stats_start['bytes_recv']

    sent_speed = bytes_sent_diff / duration_seconds
    recv_speed = bytes_recv_diff / duration_seconds
    
    return {
        'current_sent_speed': bytes_to_mb_and_gb(sent_speed),
        'current_recv_speed': bytes_to_mb_and_gb(recv_speed) 
    }

# Function to print network metrics
def get_network_metrics():

    response = "\nNETWORK Metrics:\n\n"

    network_metrics = fetch_network_metrics()
    for key, value in network_metrics.items():
        response += f"{key}:\n"
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                response += f"  {subkey}:\n"
                if isinstance(subvalue, dict):
                    for k, v in subvalue.items():
                        response += f"    {k}: {v}\n"
                elif isinstance(subvalue, list):
                    for item in subvalue:
                        response += "    Address Info:\n"
                        for k, v in item.items():
                            response += f"      {k}: {v}\n"
        response += "\n"
    response += "Network connections count:\n"
    private_connections, non_private_connections, used_ports = analyze_connections()
    response += f"  Private Connections: {private_connections}\n"
    response += f"  Non-private Connections: {non_private_connections}\n"
    response += f"  Used Ports:\n"
    for k, v in sorted(dict(used_ports).items()):
        response += f"    port {k}:  {v} connections\n"

    current_bandwidth_speed = calculate_bandwidth_speed()
    response += "\nNetwork Current Bandwidth Speed:\n"
    response += f"  Current Sent Speed: {current_bandwidth_speed['current_sent_speed']}\n"
    response += f"  Current Received Speed: {current_bandwidth_speed['current_recv_speed']}\n"
    response += "\n"
    
    return response
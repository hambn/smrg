import psutil

def fetch_network_connections():
    # Network Connections
    connections = psutil.net_connections()
    connections_metrics = []
    for conn in connections:
        laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else "N/A"
        raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
        connection_info = {
            'fd': conn.fd,
            'family': conn.family,
            'type': conn.type,
            'local_address': laddr,
            'remote_address': raddr,
            'status': conn.status,
            'pid': conn.pid
        }
        connections_metrics.append(connection_info)

    return connections_metrics

def get_network_connections():
    response = "\nNetwork Connections Details:\n\n"
    network_connections = fetch_network_connections()
    response += "Network Connections:\n"
    for connection in network_connections:
        for k, v in connection.items():
            response += f"  {k}: {v}\n"
        response += "\n"
    return response
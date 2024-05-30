import psutil

def bytes_to_mb_and_gb(bytes_value):
    gb = bytes_value / (1024 ** 3)
    mb = bytes_value / (1024 ** 2)
    return f"({gb:.3f} GB  {mb:.3f} MB)"

def fetch_disk_metrics():
    # Disk Partitions
    partitions = psutil.disk_partitions()
    partitions_metrics = [
        {
            'Device': p.device,
            'Mountpoint': p.mountpoint,
            'File System Type': p.fstype,
            'Options': p.opts
        }
        for p in partitions
    ]
    
    # Disk Usage
    disk_usage = {p.mountpoint: psutil.disk_usage(p.mountpoint)._asdict() for p in partitions}
    for mountpoint, usage in disk_usage.items():
        for key, value in usage.items():
            if key != 'percent':
                usage[key] = bytes_to_mb_and_gb(value)  # Convert bytes to MB
            else:
                usage[key] = f"{value:.2f}%"  # Format percentage

    # Disk I/O
    disk_io = psutil.disk_io_counters(perdisk=True)
    disk_io_metrics = {}
    for disk, metrics in disk_io.items():
        disk_io_metrics[disk] = {
            key: bytes_to_mb_and_gb(value) if 'bytes' in key else value
            for key, value in metrics._asdict().items()
        }

    return {
        'Disk Partitions': partitions_metrics,
        'Disk Usage': disk_usage,
        'Disk I/O': disk_io_metrics
    }

def get_disk_metrics():
    response = "\nDISK Metrics:\n\n"
    disk_metrics = fetch_disk_metrics()
    for key, value in disk_metrics.items():
        response += f"{key}:\n"
        if isinstance(value, list):
            for item in value:
                response += f"  Device: {item['Device']}\n"
                response += f"    Mountpoint: {item['Mountpoint']}\n"
                response += f"    File System Type: {item['File System Type']}\n"
                response += f"    Options: {item['Options']}\n"
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                response += f"  {subkey}:\n"
                for k, v in subvalue.items():
                    response += f"    {k}: {v}\n"
        response += "\n"
    return response
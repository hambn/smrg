import psutil

def get_all_ram_metrics_mb():
    # Convert bytes to megabytes with 2 decimal places
    def bytes_to_mb(bytes_value):
        return f"{bytes_value / (1024 * 1024):.2f} MB"

    # Virtual Memory Metrics
    virtual_memory = psutil.virtual_memory()
    virtual_memory_metrics = {
        'Total': bytes_to_mb(virtual_memory.total),
        'Available': bytes_to_mb(virtual_memory.available),
        'Used': bytes_to_mb(virtual_memory.used),
        'Free': bytes_to_mb(virtual_memory.free),
        'Active': bytes_to_mb(getattr(virtual_memory, 'active', 0)),
        'Inactive': bytes_to_mb(getattr(virtual_memory, 'inactive', 0)),
        'Buffers': bytes_to_mb(getattr(virtual_memory, 'buffers', 0)),
        'Cached': bytes_to_mb(getattr(virtual_memory, 'cached', 0)),
        'Shared': bytes_to_mb(getattr(virtual_memory, 'shared', 0)),
        'Slab': bytes_to_mb(getattr(virtual_memory, 'slab', 0)),
        'Wired': bytes_to_mb(getattr(virtual_memory, 'wired', 0)),  # Only on BSD
        'Percent': f"{virtual_memory.percent:.2f}%"
    }

    # Swap Memory Metrics
    swap_memory = psutil.swap_memory()
    swap_memory_metrics = {
        'Total': bytes_to_mb(swap_memory.total),
        'Used': bytes_to_mb(swap_memory.used),
        'Free': bytes_to_mb(swap_memory.free),
        'Percent': f"{swap_memory.percent:.2f}%",
        'Sin': bytes_to_mb(swap_memory.sin),  # Swap in
        'Sout': bytes_to_mb(swap_memory.sout)  # Swap out
    }

    return {
        'Virtual Memory': virtual_memory_metrics,
        'Swap Memory': swap_memory_metrics
    }

def get_ram_metrics():
    
    metrics = get_all_ram_metrics_mb()
    response = "\nRAM Details:\n\n"
    
    for key, value in metrics.items():
        response += f"{key}:\n"
        if isinstance(value, dict):
            for subkey, subvalue in value.items():
                response += f"  {subkey}: {subvalue}\n"
        response += "\n"

    return response
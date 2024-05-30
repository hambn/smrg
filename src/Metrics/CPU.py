import psutil

def get_all_cpu_metrics():
    # General CPU Metrics
    cpu_times = psutil.cpu_times()
    cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_stats = psutil.cpu_stats()
    cpu_freq = psutil.cpu_freq()
    load_avg = psutil.getloadavg()

    # Per-CPU Times
    per_cpu_times = psutil.cpu_times(percpu=True)
    per_cpu_times_metrics = [
        {
            'CPU': i,
            'User Time (seconds)': cpu_time.user,
            'System Time (seconds)': cpu_time.system,
            'Idle Time (seconds)': cpu_time.idle,
            'Nice Time (seconds)': getattr(cpu_time, 'nice', None),
            'I/O Wait Time (seconds)': getattr(cpu_time, 'iowait', None),
            'IRQ Time (seconds)': getattr(cpu_time, 'irq', None),
            'Soft IRQ Time (seconds)': getattr(cpu_time, 'softirq', None),
            'Steal Time (seconds)': getattr(cpu_time, 'steal', None),
            'Guest Time (seconds)': getattr(cpu_time, 'guest', None),
            'Guest Nice Time (seconds)': getattr(cpu_time, 'guest_nice', None)
        }
        for i, cpu_time in enumerate(per_cpu_times)
    ]

    # Per-CPU Frequency
    per_cpu_freq = psutil.cpu_freq(percpu=True)
    per_cpu_freq_metrics = [
        {
            'CPU': i,
            'Current Frequency (MHz)': freq.current,
            'Min Frequency (MHz)': freq.min,
            'Max Frequency (MHz)': freq.max
        }
        for i, freq in enumerate(per_cpu_freq)
    ]

    return {
        'CPU Times': {
            'User Time (seconds)': cpu_times.user,
            'System Time (seconds)': cpu_times.system,
            'Idle Time (seconds)': cpu_times.idle,
            'Nice Time (seconds)': getattr(cpu_times, 'nice', None),
            'I/O Wait Time (seconds)': getattr(cpu_times, 'iowait', None),
            'IRQ Time (seconds)': getattr(cpu_times, 'irq', None),
            'Soft IRQ Time (seconds)': getattr(cpu_times, 'softirq', None),
            'Steal Time (seconds)': getattr(cpu_times, 'steal', None),
            'Guest Time (seconds)': getattr(cpu_times, 'guest', None),
            'Guest Nice Time (seconds)': getattr(cpu_times, 'guest_nice', None)
        },
        'CPU Percent': cpu_percent,
        'CPU Count (Logical)': cpu_count_logical,
        'CPU Count (Physical)': cpu_count_physical,
        'CPU Stats': {
            'Context Switches': cpu_stats.ctx_switches,
            'Interrupts': cpu_stats.interrupts,
            'Soft Interrupts': cpu_stats.soft_interrupts,
            'Syscalls': cpu_stats.syscalls
        },
        'CPU Frequency': {
            'Current Frequency (MHz)': cpu_freq.current,
            'Min Frequency (MHz)': cpu_freq.min,
            'Max Frequency (MHz)': cpu_freq.max
        },
        'Load Average': {
            'Load Average (1 minute)': load_avg[0],
            'Load Average (5 minutes)': load_avg[1],
            'Load Average (15 minutes)': load_avg[2]
        },
        'Per-CPU Times': per_cpu_times_metrics,
        'Per-CPU Frequency': per_cpu_freq_metrics
    }

def get_cpu_metrics():

    metrics = get_all_cpu_metrics()
    response = "\nCPU Details:\n\n"

    for key, value in metrics.items():
        response += f"{key}:\n"
        if isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    for subkey, subvalue in item.items():
                        response += f"  {subkey}: {subvalue}\n"
                    response += "\n"
                else:
                    response += f"  CPU {i}: {item}%\n"
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                response += f"  {subkey}: {subvalue}\n"
        else:
            response += f"  {value}\n"
        response += "\n"

    return response
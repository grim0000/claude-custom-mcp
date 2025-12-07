import psutil
import logging

logger = logging.getLogger("resource-tools")

async def get_system_stats() -> str:
    """Gets current system statistics (CPU, Memory, Disk)."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return (
        f"CPU Usage: {cpu_percent}%\n"
        f"Memory Usage: {memory.percent}% (Used: {memory.used // (1024**3)}GB / Total: {memory.total // (1024**3)}GB)\n"
        f"Disk Usage: {disk.percent}% (Free: {disk.free // (1024**3)}GB)"
    )

async def list_processes(limit: int = 10) -> str:
    """Lists top running processes by memory usage."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Sort by memory usage
    processes.sort(key=lambda p: p['memory_percent'] or 0, reverse=True)
    
    top_procs = processes[:limit]
    output = ["Top Processes by Memory:"]
    for p in top_procs:
        mem = f"{p['memory_percent']:.1f}%" if p['memory_percent'] else "N/A"
        output.append(f"PID: {p['pid']:<6} | Name: {p['name']:<25} | Mem: {mem}")
        
    return "\n".join(output)

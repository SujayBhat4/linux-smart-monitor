import psutil
import time
from datetime import datetime
import os

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "system_log.txt")


def ensure_log_dir():
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)


def get_stats():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    net = psutil.net_io_counters()
    net_usage = net.bytes_sent + net.bytes_recv

    return cpu, ram, disk, net_usage


def log_stats():
    cpu, ram, disk, net = get_stats()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"{timestamp}, CPU={cpu}%, RAM={ram}%, Disk={disk}%, Net={net}\n"

    with open(LOG_FILE, "a") as f:
        f.write(line)

    print(line)


def main():
    ensure_log_dir()

    print("🚀 Linux Smart Monitor Started...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            log_stats()
            time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
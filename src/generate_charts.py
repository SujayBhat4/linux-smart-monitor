import pandas as pd
import matplotlib.pyplot as plt
import os

LOG_FILE = "logs/system_log.txt"
CHART_DIR = "charts"


def ensure_chart_dir():
    if not os.path.exists(CHART_DIR):
        os.makedirs(CHART_DIR)


def parse_log():
    data = {
        "time": [],
        "cpu": [],
        "ram": [],
        "disk": []
    }

    with open(LOG_FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")

            time = parts[0]
            cpu = float(parts[1].split("=")[1].replace("%", ""))
            ram = float(parts[2].split("=")[1].replace("%", ""))
            disk = float(parts[3].split("=")[1].replace("%", ""))

            data["time"].append(time)
            data["cpu"].append(cpu)
            data["ram"].append(ram)
            data["disk"].append(disk)

    return pd.DataFrame(data)


def generate_charts(df):
    ensure_chart_dir()

    # CPU
    plt.figure()
    plt.plot(df["time"], df["cpu"])
    plt.xticks(rotation=45)
    plt.title("CPU Usage")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/cpu.png")
    plt.close()

    # RAM
    plt.figure()
    plt.plot(df["time"], df["ram"])
    plt.xticks(rotation=45)
    plt.title("RAM Usage")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/ram.png")
    plt.close()

    # Disk
    plt.figure()
    plt.plot(df["time"], df["disk"])
    plt.xticks(rotation=45)
    plt.title("Disk Usage")
    plt.tight_layout()
    plt.savefig(f"{CHART_DIR}/disk.png")
    plt.close()


def main():
    df = parse_log()
    generate_charts(df)
    print("Charts generated in charts/ folder.")


if __name__ == "__main__":
    main()
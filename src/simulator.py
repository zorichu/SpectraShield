import pandas as pd
import numpy as np
from datetime import datetime
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)

start = datetime.now()

normal_n = 500

normal = pd.DataFrame({
        "timestamp": pd.date_range(start=start, periods=normal_n, freq="s"),
        "source_ip": ["10.0.0." + str(x) for x in np.random.randint(1, 20, normal_n)],
        "destination_ip": ["10.0.1." + str(x) for x in np.random.randint(1, 20, normal_n)],
        "source_port": np.random.randint(1024, 65535, normal_n),
        "destination_port": np.random.choice([80, 443, 22, 53], normal_n),
        "protocol": np.random.choice(["TCP", "UDP"], normal_n),
        "packet_count": np.random.randint(20, 150, normal_n),
        "bytes": np.random.randint(1000, 70000, normal_n),
        "duration": np.round(np.random.uniform(0.5, 5, normal_n), 2),
        "attack_type": "Normal"
})

ddos_n = 50

ddos = pd.DataFrame({
    "timestamp": pd.date_range(start=start, periods=ddos_n, freq="s"),
    "source_ip": ["192.168.1." + str(x) for x in np.random.randint(1, 255, ddos_n)],
    "destination_ip": ["10.0.1.5"] * ddos_n,
    "source_port": np.random.randint(1024, 65535, ddos_n),
    "destination_port": [80] * ddos_n,
    "protocol": ["TCP"] * ddos_n,
    "packet_count": np.random.randint(2000, 5000, ddos_n),
    "bytes": np.random.randint(500000, 2000000, ddos_n),
    "duration": np.round(np.random.uniform(0.1, 1, ddos_n), 2),
    "attack_type": "Possible DDoS"
})

scan_n = 50

scan = pd.DataFrame({
    "timestamp": pd.date_range(start=start, periods=scan_n, freq="s"),
    "source_ip": ["172.16.0.10"] * scan_n,
    "destination_ip": ["10.0.1.10"] * scan_n,
    "source_port": np.random.randint(1024, 65535, scan_n),
    "destination_port": np.random.randint(1, 10000, scan_n),
    "protocol": ["TCP"] * scan_n,
    "packet_count": np.random.randint(100, 400, scan_n),
    "bytes": np.random.randint(5000, 30000, scan_n),
    "duration": np.round(np.random.uniform(0.1, 2, scan_n), 2),
    "attack_type": "Possible Port Scan"
})

df = pd.concat([normal, ddos, scan], ignore_index=True)

df.to_csv("data/traffic.csv", index=False)

print("Traffic simulation complete!")
print("Generated", len(df), "traffic records.")
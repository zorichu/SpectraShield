import pandas as pd
import time
from detector import detect_threat


traffic = pd.read_csv("data/traffic.csv")

print("SpectraShield Live Monitoring Started")
print("-------------------------------------")

for i in range(len(traffic)):
    record = traffic.iloc[[i]]

    result = detect_threat(record).iloc[0]

    print(
        f"Source: {result['source_ip']} | "
        f"Destination: {result['destination_ip']} | "
        f"Threat: {result['threat']} | "
        f"Severity: {result['severity']} | "
        f"Score: {result['detection_score']}"
    )

    time.sleep(0.2)
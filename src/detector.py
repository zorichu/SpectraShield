import pandas as pd
import joblib
from src.processor import process_data

model = joblib.load("models/detector.pkl")

FEATURES = [
    "packet_count",
    "bytes",
    "duration",
    "packets_per_second",
    "bytes_per_second",
    "destination_port"
]


def detect_threat(df):
        df = process_data(df)

        X = df[FEATURES]

        predictions = model.predict(X)
        scores = model.decision_function(X)

        results = []

        for i in range(len(df)):
            if predictions[i] == 1:
                threat = "Normal"
                severity = "Low"
                reason = "Traffic pattern matches normal behaviour."

            else:
                packets = df.iloc[i]["packets_per_second"]
                bytes_rate = df.iloc[i]["bytes_per_second"]
                port = df.iloc[i]["destination_port"]
                packet_count = df.iloc[i]["packet_count"]
                
                if packets > 1000:
                    threat = "Possible DDoS"
                    severity = "Critical"
                    reason = "Very high packet rate detected."

                elif port > 1000 and packet_count > 100:
                    threat = "Possible Port Scan"
                    severity = "High"
                    reason = "Unusual port activity and packet behaviour detected."

                elif bytes_rate > 500000:
                                                                    
                    threat = "Possible Data Exfiltration"
                    severity = "High"
                    reason = "Unusually high outbound data rate detected."

                else:
                    threat = "Suspicious Anomaly"
                    severity = "Medium"
                    reason = "Traffic behaviour differs from learned normal patterns." 

            results.append({
                "threat": threat,
                "severity": severity,
                "detection_score": round(float(scores[i]), 4),
                "reason": reason
            })

        result_df = pd.DataFrame(results)

        return pd.concat(
            [df.reset_index(drop=True), result_df],
            axis=1
        )


if __name__ == "__main__":
    traffic = pd.read_csv("data/traffic.csv")
    detected = detect_threat(traffic)

    print(detected[
        ["source_ip", "destination_ip", "threat", "severity", "detection_score"]
    ].head(20).to_string(index=False))
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest
from src.processor import process_data

df = pd.read_csv("data/traffic.csv")

df = process_data(df)

normal_data = df[df["attack_type"] == "Normal"]

features = [
    "packet_count",
    "bytes",
    "duration",
    "packets_per_second",
    "bytes_per_second",
    "destination_port"
]

X = normal_data[features]

model = IsolationForest(
    n_estimators=150,
    contamination=0.15,
    random_state=42
)

model.fit(X)

joblib.dump(model, "models/detector.pkl")

print("AI model training complete!")
print("Normal traffic used:", len(X))
print("Model saved to: models/detector.pkl")
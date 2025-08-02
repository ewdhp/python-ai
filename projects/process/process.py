
"""
process.py
This script analyzes process logs to detect anomalous processes 
based on CPU and thread usage.

It performs the following steps:
- Loads process data from a CSV file.
- Sanitizes and normalizes numeric fields (CPU, Threads).
- Trains an Isolation Forest model for anomaly detection.
- Flags trusted process paths as normal (whitelisting).
- Outputs suspicious (anomalous) processes to a separate CSV file.
Intended for use in monitoring and identifying potentially suspicious 
or abnormal processes on a Windows system.

The Isolation Forest algorithm is used here for anomaly detection. 
Its purpose is to identify processes whose CPU and Threads usage 
patterns differ significantly from the majority, which may indicate 
suspicious or abnormal behavior.

Explanation:

Isolation Forest is an unsupervised machine learning algorithm designed 
to detect anomalies (outliers) in data.It works by randomly partitioning 
the data and isolating observations. Anomalies are isolated faster because 
they are few and different.In this code, the model is trained on normalized 
CPU and Threads metrics for each process.Processes that the model predicts 
as outliers are labeled as "anomaly", while the rest are labeled as "normal".
This helps automatically flag unusual processes for further investigation.
You can add this as a comment above the model training section:
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
import os

# Load data using relative path
csv_path = os.path.join(os.path.dirname(__file__), "proc_log.csv")
df = pd.read_csv(csv_path)

# Sanitize numeric fields
df["CPU"] = pd.to_numeric(df["CPU"], errors="coerce")
df["Threads"] = pd.to_numeric(df["Threads"], errors="coerce")
df.dropna(subset=["CPU", "Threads", "Path"], inplace=True)

# Bail out if nothing usable
if df[["CPU", "Threads"]].shape[0] == 0:
    print("No valid rows with numeric CPU and Threads values. Exiting.")
    exit(1)

# Normalize metrics
scaler = StandardScaler()
df[["CPU", "Threads"]] = scaler.fit_transform(df[["CPU", "Threads"]])

# Train anomaly detection model
model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
model.fit(df[["CPU", "Threads"]])
df["anomaly"] = model.predict(df[["CPU", "Threads"]])
df["anomaly"] = df["anomaly"].map({1: "normal", -1: "anomaly"})

# Whitelist trusted paths
trusted_paths = [
    r"C:\Windows\Explorer.EXE",
    r"C:\Users\ewdhp\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    r"C:\Program Files\WindowsApps\Microsoft.Copilot_1.25071.125.0_x64__8wekyb3d8bbwe\Copilot.exe"
]
df["anomaly"] = df.apply(
    lambda row: "normal" if row["Path"] in trusted_paths else row["anomaly"],
    axis=1
)

# Segment suspicious processes
anomalies = df[df["anomaly"] == "anomaly"]
output_path = os.path.join(os.path.dirname(__file__), "suspicious_processes.csv")
anomalies.to_csv(output_path, index=False)

# Optional: Print summary
print(f"✅ Process scan complete: {len(anomalies)} anomalies logged.")
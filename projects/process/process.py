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
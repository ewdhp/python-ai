import pandas as pd
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("proc_log.csv")
df.dropna(inplace=True)

scaler = StandardScaler()
df[["CPU", "Threads"]] = scaler.fit_transform(df[["CPU", "Threads"]])
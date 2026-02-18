"""
import pandas as pd

#load dataset
df = pd.read_csv("smart_logistics_dataset.csv")

print("\nColumns:\n")
print(df.columns)

print("\nShape:\n")
print(df.shape)

print("\nFirst 5 rows:\n")
print(df.head())

"""

import pandas as pd

#load dataset
df = pd.read_csv("smart_logistics_dataset.csv")


#Fix Column names
df.columns = df.columns.str.strip()
print(df.columns)

print("\nInitial Shape:", df.shape)

#----1.Remove duplicates-----
df = df.drop_duplicates()


#----2.Check Null Vlaues-----
print("\nNull Valiues: \n")
print(df.isnull().sum())


#----3.Fix data types----

df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce')


#----4.Drop rows with bad Timestamp-----

df = df.dropna(subset=['Timestamp'])


#-----5.Create Useful Fields-----

df['Year'] = df['Timestamp'].dt.year
df['Month'] = df['Timestamp'].dt.month
df['Day'] = df['Timestamp'].dt.day


#-----6. Standardize Text Columns-----

text_cols = ['Shipment_Status', 'Traffic_Status', 'Logistics_Delay_Reason']
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()


#----7. Final Shape-----

print("\nCleaned Shape:", df.shape)


#----8. Export Cleaned Data-----

df.to_csv("clean_logistics_data.csv", index=False)

print("\nClean dataset saved as: clean_logistics_data.csv")



print("\n===== BASIC EDA =====")

# 1) Shipment Status count
print("\nShipment Status Distribution:")
print(df['Shipment_Status'].value_counts())

# 2) Delay rate
print("\nDelay Percentage:")
delay_rate = df['Logistics_Delay'].mean() * 100
print(f"Overall Delay Rate: {delay_rate:.2f}%")

# 3) Top delay reasons
print("\nTop Delay Reasons:")
print(df['Logistics_Delay_Reason'].value_counts().head(10))

# 4) Traffic impact
print("\nDelay by Traffic Condition:")
print(pd.crosstab(df['Traffic_Status'], df['Logistics_Delay']))

# 5) Waiting time impact
print("\nAverage Waiting Time by Delay:")
print(df.groupby('Logistics_Delay')['Waiting_Time'].mean())

# 6) Asset utilization impact
print("\nAsset Utilization vs Delay:")
print(df.groupby('Logistics_Delay')['Asset_Utilization'].mean())



print("\n===== DATA TYPES CHECK =====")
print(df.dtypes)

print("\nUnique values check:")
print("Logistics_Delay unique:", df["Logistics_Delay"].unique())
print("Shipment_Status unique:", df["Shipment_Status"].unique()[:10])
print("Traffic_Status unique:", df["Traffic_Status"].unique()[:10])


print("\n===== DELAY TREND ANALYSIS =====")

# Delay rate by Month
delay_by_month = df.groupby(['Year','Month'])['Logistics_Delay'].mean().reset_index()
delay_by_month['Delay_Percent'] = delay_by_month['Logistics_Delay'] * 100

print(delay_by_month.head())



print("\n===== KPI SUMMARY =====")

total_shipments = len(df)
delay_percent = df['Logistics_Delay'].mean() * 100
avg_waiting = df['Waiting_Time'].mean()
avg_utilization = df['Asset_Utilization'].mean()

print(f"Total Shipments: {total_shipments}")
print(f"Delay %: {delay_percent:.2f}")
print(f"Avg Waiting Time: {avg_waiting:.2f}")
print(f"Avg Asset Utilization: {avg_utilization:.2f}")


import pandas as pd

# 1) KPI summary (single row)
kpi = pd.DataFrame([{
    "Total_Shipments": len(df),
    "Delay_Percent": df["Logistics_Delay"].mean() * 100,
    "Avg_Waiting_Time": df["Waiting_Time"].mean(),
    "Avg_Asset_Utilization": df["Asset_Utilization"].mean()
}])
kpi.to_csv("tbl_kpi.csv", index=False)

# 2) Delay trend by month
delay_trend = (df.groupby(["Year","Month"], as_index=False)["Logistics_Delay"].mean())
delay_trend["Delay_Percent"] = delay_trend["Logistics_Delay"] * 100
delay_trend.to_csv("tbl_delay_trend.csv", index=False)

# 3) Delay % by traffic
delay_by_traffic = (df.groupby("Traffic_Status", as_index=False)["Logistics_Delay"].mean())
delay_by_traffic["Delay_Percent"] = delay_by_traffic["Logistics_Delay"] * 100
delay_by_traffic.to_csv("tbl_delay_by_traffic.csv", index=False)

# 4) Delay % by shipment status
delay_by_status = (df.groupby("Shipment_Status", as_index=False)["Logistics_Delay"].mean())
delay_by_status["Delay_Percent"] = delay_by_status["Logistics_Delay"] * 100
delay_by_status.to_csv("tbl_delay_by_status.csv", index=False)

# 5) Top delay reasons (counts)
delay_reasons = df["Logistics_Delay_Reason"].value_counts().reset_index()
delay_reasons.columns = ["Logistics_Delay_Reason", "Count"]
delay_reasons.to_csv("tbl_delay_reasons.csv", index=False)

print("Exported: tbl_kpi.csv, tbl_delay_trend.csv, tbl_delay_by_traffic.csv, tbl_delay_by_status.csv, tbl_delay_reasons.csv")
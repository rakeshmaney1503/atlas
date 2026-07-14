import pandas as pd

df = pd.read_csv("data/samples/zerodha/holdings-2.csv")

print(df.info())
print()
print(df.columns.tolist())
print()
print(df.head())

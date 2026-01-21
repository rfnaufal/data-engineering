import sys
import os
import pandas as pd
print("arguments", sys.argv)
month = int(sys.argv[1])

df = pd.DataFrame({"Day": [1, 2], "Num_passengers": [3, 4]})
df['month'] = month
print(df.head())
#df.to_parquet(f"output_day_{sys.argv[1]}.parquet")
df.to_parquet(f"{month}.parquet")
print(f"Running pipeline for month {month}")
print("cwd:", os.getcwd())
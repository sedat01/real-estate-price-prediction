import pandas as pd
import glob
import os

path = r'C:\Users\sedat\source\repos\real-estate-price-prediction\csv files by provinces\all' # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))

li = []

for filename in all_files:
    df = pd.read_csv(filename,low_memory=False, index_col=None, header=0)
    li.append(df)

df = pd.concat((pd.read_csv(f,low_memory=False) for f in all_files), ignore_index=True)
df.to_csv("collected_all.csv")
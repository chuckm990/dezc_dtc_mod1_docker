import sys
import pandas as pd

month = int(sys.argv[1]) #sys.argv[0] is always the name of the script

df = pd.DataFrame({"day": [1, 2], "num_passengers": [3, 4]})
df['month'] = month
print(df.head())

df.to_parquet(f"output_day_{sys.argv[1]}.parquet")

print('CLI arguments: ', sys.argv)

print('Hello first docker pipeline!', f'Current month is: month={month}') #because month moves from 1 to 12, we say that it is parametrized
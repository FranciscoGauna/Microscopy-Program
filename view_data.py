import pandas as pd

df = pd.read_csv("output/run_1.csv")[["Lockin_amplitude", "Fungen 1_frequency"]]

print(df.columns)
print(df)
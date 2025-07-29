import pandas as pd

# Load the CSV file
df = pd.read_csv("data/videos.csv")

# Show the first 5 rows
print("First 5 rows:")
print(df.head(), "\n")

# Show column names
print("Columns:")
print(df.columns.tolist(), "\n")

# Show basic info
print("Info:")
print(df.info(), "\n")

# Show summary statistics for numeric columns
print("Summary statistics:")
print(df.describe(include='all'))
import os
import pandas as pd

# Example file path to check on your local system
file_path = "/Users/matthewlary/Desktop/sensorData/MINTS_001e0636e547_APDS9002_2023_07_30.csv"
print(f"Attempting to access: {file_path}")
print("Does the file exist?", os.path.exists(file_path))

# Print the current working directory
print("Current working directory:", os.getcwd())

# Ensure the file path is for the local environment
# Adjust the file path according to where the script is being executed
# Here we use the file_path from the initial check which we know exists
try:
    # Load the provided sample file
    df = pd.read_csv(file_path)

    # Display the first few rows of the dataframe
    print(df.head())
except Exception as e:
    print(f"Failed to load the file: {e}")


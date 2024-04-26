import pandas as pd
import matplotlib.pyplot as plt
from functions import process_csv_files  # Ensure this import statement is correct

# Usage
yaml_file = '/Users/matthewlary/Desktop/General/Programming/Repos/sensor_calibration/SensorDataV2.yaml'

# Process the CSV files and get the combined dataframe
combined_dataframe = process_csv_files(yaml_file)
print(combined_dataframe)

# Plotting
if not combined_dataframe.empty and {'temperature_BME280', 'temperature_BME680'}.issubset(combined_dataframe.columns):
    plt.figure(figsize=(10, 6))
    plt.plot(combined_dataframe.index, combined_dataframe['temperature_BME280'], label='Temperature BME280', color='blue')
    plt.plot(combined_dataframe.index, combined_dataframe['temperature_BME680'], label='Temperature BME680', color='red')
    plt.xlabel('DateTime')
    plt.ylabel('Temperature')
    plt.title('Temperature Data Resampled')
    plt.legend()
    plt.show()
else:
    print("Data is empty or required temperature columns are missing.")

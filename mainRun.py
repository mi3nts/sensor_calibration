
import pandas as pd
import yaml
import os
import re
import matplotlib.pyplot as plt
import functions as f

# Usage
yaml_file     = '/Users/matthewlary/Desktop/General/Programming/Repos/sensor_calibration/SensorDataV2.yaml'  # Update with the correct path
# Process the CSV files and get the combined dataframe
combined_dataframe= f.process_csv_files(yaml_file)


print(combined_dataframe)


# Plotting
plt.figure(figsize=(10, 6))
plt.plot(combined_dataframe.index, combined_dataframe['temperature_BME280'], label='Temperature BME280', color='blue')
plt.plot(combined_dataframe.index, combined_dataframe['temperature_BME680'], label='Temperature BME680', color='red')
plt.xlabel('DateTime')
plt.ylabel('Temperature')
plt.title('Temperature Data Resampled')
plt.legend()
plt.show()


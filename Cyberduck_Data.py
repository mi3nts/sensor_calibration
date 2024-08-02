import pandas as pd
import matplotlib.pyplot as plt
import yaml
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def process_csv_files(yaml_file, base_folder):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    node_ids = yaml_data['node_ids']
    sensor_ids = yaml_data['sensor_ids']

    combined_dataframes = []

    for root, dirs, files in os.walk(base_folder):
        for file in files:
            if file.endswith(".csv"):
                for node_id in node_ids:
                    for sensor_id in sensor_ids:
                        if f"MINTS_{node_id}_{sensor_id}_" in file:
                            file_path = os.path.join(root, file)

                            df = pd.read_csv(file_path)
                            df['dateTime'] = pd.to_datetime(df['dateTime'], errors='coerce')
                            df.set_index('dateTime', inplace=True)
                            numerical_cols = df.select_dtypes(include=['number']).columns
                            df_numerical = df[numerical_cols].rename(columns=lambda x: f"{x}_{sensor_id}")
                            df_resampled = df_numerical.resample('min').mean()  # Downsample to 1 minute intervals

                            # Filter temperature, PM2.5, pressure, and humidity columns
                            relevant_cols = [col for col in df_resampled.columns if 'temperature' in col.lower() or 'pm2_5' in col.lower() or 'pressure' in col.lower() or 'humidity' in col.lower()]
                            if relevant_cols:
                                df_relevant = df_resampled[relevant_cols]
                                combined_dataframes.append(df_relevant)

    if not combined_dataframes:
        return pd.DataFrame()

    combined_dataframe = pd.concat(combined_dataframes, axis=0).sort_index()
    combined_dataframe.ffill(inplace=True)

    return combined_dataframe

# Usage
yaml_file = '/Users/matthewlary/Desktop/Programming/Repos/sensor_calibration/SensorDataV2.yaml'
base_folder = '/Users/matthewlary/Desktop/sensorData'

# Process the CSV files and get the combined dataframe
combined_dataframe = process_csv_files(yaml_file, base_folder)

# Display the first 20 rows of the combined dataframe
pd.set_option('display.max_columns', None)  # Display all columns
print("First 20 rows of the combined dataframe:")
print(combined_dataframe.head(20))

# Filter relevant columns for the BME280 sensor
bme280_pressure_cols = [col for col in combined_dataframe.columns if 'pressure' in col.lower() and 'BME280' in col]
bme280_humidity_cols = [col for col in combined_dataframe.columns if 'humidity' in col.lower() and 'BME280' in col]
bme280_temp_cols = [col for col in combined_dataframe.columns if 'temperature' in col.lower() and 'BME280' in col]

if not bme280_pressure_cols or not bme280_humidity_cols or not bme280_temp_cols:
    print("BME280 sensor data not found.")
else:
    # Prepare the data for machine learning
    combined_dataframe['BME280_pressure'] = combined_dataframe[bme280_pressure_cols].mean(axis=1)
    combined_dataframe['BME280_humidity'] = combined_dataframe[bme280_humidity_cols].mean(axis=1)
    combined_dataframe['BME280_temperature'] = combined_dataframe[bme280_temp_cols].mean(axis=1)
    
    # Drop rows with missing values
    combined_dataframe.dropna(subset=['BME280_pressure', 'BME280_humidity', 'BME280_temperature'], inplace=True)
    
    # Define features and target
    X = combined_dataframe[['BME280_pressure', 'BME280_humidity']]
    y = combined_dataframe['BME280_temperature']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train a linear regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error: {mse}")
    
    # Plot the true vs predicted values with a 45-degree line
    plt.figure(figsize=(15, 8))
    plt.scatter(y_test, y_pred, alpha=0.5, label='Predicted vs True')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', label='45-degree line')
    plt.xlabel('True Temperature')
    plt.ylabel('Predicted Temperature')
    plt.title('True vs Predicted Temperature for BME280')
    plt.legend()
    plt.show()

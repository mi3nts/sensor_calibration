import pandas as pd
import yaml
import os

def process_csv_files(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    node_ids = yaml_data['node_ids']
    sensor_ids = yaml_data['sensor_ids']

    base_path = "/Users/matthewlary/Desktop/sensorData/MINTS_"
    date_suffix = "2023_07_30.csv"
    all_dataframes = []

    for node_id in node_ids:
        for sensor_id in sensor_ids:
            file_path = f"{base_path}{node_id}_{sensor_id}_{date_suffix}"
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                continue

            df = pd.read_csv(file_path)
            df['dateTime'] = pd.to_datetime(df['dateTime'])
            df.set_index('dateTime', inplace=True)
            numerical_cols = df.select_dtypes(include=['number']).columns
            df_numerical = df[numerical_cols].rename(columns=lambda x: f"{x}_{sensor_id}")
            df_numerical.dropna(inplace=True)
            df_resampled = df_numerical.resample('10S').mean()
            all_dataframes.append(df_resampled)

    if not all_dataframes:
        print("No dataframes to concatenate")
        return pd.DataFrame()

    combined_dataframe = pd.concat(all_dataframes, axis=1)
    return combined_dataframe

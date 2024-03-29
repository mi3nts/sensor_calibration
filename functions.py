
import pandas as pd
import yaml
import os
import re
import matplotlib.pyplot as plt


def process_csv_files_v0(yaml_file):
    # Load the YAML file
    with open(yaml_file, 'r') as file:
        csv_file_paths = yaml.safe_load(file)['csv_files']

    all_dataframes = []

    for file_info in csv_file_paths:
        file_path = file_info['name']

        # Extract the name from the file path
        filename = os.path.basename(file_path)
        name_match = re.search(r"_([A-Za-z0-9]+)_\d{4}_\d{2}_\d{2}\.csv", filename)
        if name_match:
            name_suffix = name_match.group(1)
        else:
            name_suffix = 'Unknown'

        # Load CSV file
        df = pd.read_csv(file_path)

        # Convert 'dateTime' to datetime and set as index
        df['dateTime'] = pd.to_datetime(df['dateTime'])
        df.set_index('dateTime', inplace=True)

        # Keep only numerical columns
        numerical_cols = df.select_dtypes(include=['number']).columns

        # Rename numerical columns by appending the extracted name
        df_numerical = df[numerical_cols].rename(columns=lambda x: f"{x}_{name_suffix}")

        # Drop rows with NaN values in numerical columns
        df_numerical.dropna(inplace=True)

        # Resample and average each DataFrame at 10-second intervals
        df_resampled = df_numerical.resample('10S').mean()

        # Collect all resampled dataframes
        all_dataframes.append(df_resampled)

    # Concatenate all dataframes along columns
    combined_dataframe = pd.concat(all_dataframes, axis=1)

    return combined_dataframe


def process_csv_files(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    node_ids = yaml_data['node_ids']
    sensor_ids = yaml_data['sensor_ids']

    base_path = "/Users/mlary/Desktop/sensorData/MINTS_"
    date_suffix = "2023_07_30.csv"  # Change this if the dates vary
    all_dataframes = []

    for node_id in node_ids:
        for sensor_id in sensor_ids:
            file_path = f"{base_path}{node_id}_{sensor_id}_{date_suffix}"
            print(f"Checking file: {file_path}")  # Debugging line

            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")  # Debugging line
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
        print("No dataframes to concatenate")  # Debugging line
        return pd.DataFrame()

    combined_dataframe = pd.concat(all_dataframes, axis=1)
    return combined_dataframe



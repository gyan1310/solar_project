import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

st.set_option('deprecation.showPyplotGlobalUse', False)

# Function for data cleaning
def data_cleaning(df):
    # Extract the date from the location column and create a new column 'Date'
    df['Date'] = df['coo: 25.4924552_81.8638651'].str.split('\t').str[0]

    # Create columns for solar elevation and azimuth for each timestamp
    for col in df.columns[1:]:  # Skip the location column
        if col.startswith('E'):
            df['Elevation_' + col[2:]] = df[col]
        elif col.startswith('A'):
            df['Azimuth_' + col[2:]] = df[col]

    # Drop the original location column and the timestamp columns
    df = df.drop(columns=['coo: 25.4924552_81.8638651'])
    # Delete columns 1 to 32 (0-based index) from the DataFrame
    df = df.iloc[:, 32:]  # Keep columns from index 32 onwards

    return df

# Function to calculate solar zenith angle
def calculate_solar_zenith_angle(df):
    # Assuming the latitude is fixed for your location
    latitude = 25.4924552  # Replace with your actual latitude

    # Create a new column for solar zenith angle
    for col in df.columns:
        if col.startswith('Elevation_'):
            # Convert the elevation values to numeric, replacing non-numeric values with NaN
            df['Elevation_' + col[10:]] = pd.to_numeric(df[col], errors='coerce')
            # Calculate the solar zenith angle for each timestamp
            df['Zenith_' + col[10:]] = 90 - df['Elevation_' + col[10:]].astype(float)

    return df

# Function to calculate optimal tilt angle
def calculate_optimal_tilt_angle(df):
    # Create a new column for optimal tilt angle
    for col in df.columns:
        if col.startswith('Zenith_'):
            # Calculate the optimal tilt angle based on the solar zenith angle
            df['Optimal_Tilt_' + col[7:]] = df[col].astype(float)

    return df

# Function to calculate optimal azimuth angle
def calculate_optimal_azimuth_angle(df):
    # Create a new column for optimal azimuth angle
    for col in df.columns:
        if col.startswith('Azimuth_'):
            # Replace '--' with NaN in the column
            df[col] = df[col].replace('--', np.nan)
            
            # Convert the column to float, handling NaN values
            df['Optimal_Azimuth_' + col[8:]] = df[col].astype(float)

    return df

# Streamlit app
def main():
    st.title("Solar Tracking Data Analysis")

    # File upload
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        # Read the uploaded CSV file into a DataFrame
        df = pd.read_csv(uploaded_file)

        # Data cleaning
        df = data_cleaning(df)

        # Calculate solar zenith angle
        df = calculate_solar_zenith_angle(df)

        # Calculate optimal tilt angle
        df = calculate_optimal_tilt_angle(df)

        # Calculate optimal azimuth angle
        df = calculate_optimal_azimuth_angle(df)

        # Display the processed DataFrame as a table
        st.subheader("Processed Data")
        st.write(df)

        # Extract timestamps (assuming they are column names with 'Zenith_' prefix)
        timestamps = [col for col in df.columns if col.startswith('Zenith_')]

        # # Plot solar zenith angle
        # st.subheader("Solar Zenith Angle Over Time")
        # plt.figure(figsize=(12, 6))
        # for timestamp in timestamps:
        #     plt.plot(df['Date'], df[timestamp], label=f'Solar Zenith Angle ({timestamp[7:]})')

        # plt.xlabel('Date', color='white')
        # plt.ylabel('Solar Zenith Angle (degrees)', color='white')
        # plt.title('Solar Zenith Angle Over Time', color='white')
        # # plt.legend()
        # plt.legend(fontsize=10, edgecolor='white', labels=[f'Solar Zenith Angle ({timestamp[7:]})' for timestamp in timestamps])
        # plt.grid(False)
        # plt.xticks(rotation=45)
        # # st.pyplot()
        # # Set the background of the plot to be transparent
        # plt.savefig("solar_zenith_angle_plot.png", transparent=True)

        # # Display the transparent plot using Streamlit
        # st.image("solar_zenith_angle_plot.png")
        
        # Plot solar zenith angle
        st.subheader("Solar Zenith Angle Over Time")
        plt.figure(figsize=(12, 6))
        for timestamp in timestamps:
            plt.plot(df['Date'], df[timestamp])#, label=f'Solar Zenith Angle ({timestamp[7:]})')

        plt.xlabel('Date')
        plt.ylabel('Solar Zenith Angle (degrees)')
        plt.title('Solar Zenith Angle Over Time')
        plt.legend()
        plt.grid(False)
        plt.xticks(rotation=45)
        st.pyplot()

        # Plot optimal tilt angle
        st.subheader("Optimal Tilt Angle Over Time")
        plt.figure(figsize=(12, 6))
        for timestamp in timestamps:
            plt.plot(df['Date'], df[f'Optimal_Tilt_{timestamp[7:]}'], label=f'Optimal Tilt Angle ({timestamp[7:]})')

        plt.xlabel('Date')
        plt.ylabel('Optimal Tilt Angle (degrees)')
        plt.title('Optimal Tilt Angle Over Time')
        plt.legend()
        plt.grid(False)
        plt.xticks(rotation=45)
        st.pyplot()

        # Plot optimal azimuth angle
        st.subheader("Optimal Azimuth Angle Over Time")
        plt.figure(figsize=(12, 6))
        for timestamp in timestamps:
            plt.plot(df['Date'], df[f'Optimal_Azimuth_{timestamp[7:]}'], label=f'Optimal Azimuth Angle ({timestamp[7:]})')

        plt.xlabel('Date')
        plt.ylabel('Optimal Azimuth Angle (degrees)')
        plt.title('Optimal Azimuth Angle Over Time')
        plt.legend()
        plt.grid(False)
        plt.grid(axis='y', linestyle='--', alpha=0.6) 
        plt.xticks(rotation=45)
        st.pyplot()
        st.markdown("developed by gyan")

if __name__ == "__main__":
    main()

import pandas as pd

def data_cleaning():
    file_path = 'data.csv'

    # Read the csv file into a pandas DataFrame
    df = pd.read_csv(file_path)
    # df = df.dropna(axis=1)

    # Print the first few rows of the DataFrame to verify the data
    # print(df.head())

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

    # Print the modified DataFrame
    print(df.head())
    df.to_csv("data_cleaned.csv", index = False)


    return df

data = data_cleaning()

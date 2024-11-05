import pandas as pd


def import_sba_csv(file_path):
    """
    Imports the SBA CSV file as a pandas DataFrame.

    Args:
        file_path (str): Path to the SBA CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the SBA data.
    """
    return pd.read_csv(file_path)


def import_gl_csv(file_path):
    """
    Imports the GL CSV file as a pandas DataFrame.

    Args:
        file_path (str): Path to the GL CSV file.

    Returns:
        pd.DataFrame: DataFrame containing the GL data.
    """
    return pd.read_csv(file_path)


def main():
    """
    Main function that specifies paths to CSV files, imports them, and prints
    the head of each DataFrame to verify import success.
    """
    # Specify the paths to the CSV files
    sba_csv_path = "path/to/sba.csv"
    gl_csv_path = "path/to/gl.csv"

    # Import the CSV files as DataFrames
    sba_df = import_sba_csv(sba_csv_path)
    gl_df = import_gl_csv(gl_csv_path)

    # Print the DataFrames to verify the import
    print("SBA DataFrame:")
    print(sba_df.head())

    print("\nGL DataFrame:")
    print(gl_df.head())


if __name__ == "__main__":
    main()

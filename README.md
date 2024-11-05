## Project Setup and Data Import

This project requires importing data from two main CSV files: `SBA.csv` and `GL.csv`. These files contain essential fields for client and general ledger data processing. Below are the steps to import these CSV files into the project, including column renaming to ensure a consistent format.

### Step 1: Importing the SBA CSV

The SBA CSV file contains essential fields for client data processing:

- **Fields**:
  - `JOBID`: Unique identifier for each job
  - `CLNTNAME`: Client name
  - `CLNTKEY`: Unique client key
  - `CLACCOUNTID`: Client account ID

1. Ensure the CSV file is accessible within the working directory or specify its path.
2. Use the `import_sba_csv` function to load the SBA CSV as a DataFrame, returning a structured data frame of client data.

```python
import pandas as pd

def import_sba_csv(file_path):
    return pd.read_csv(file_path)
```

### Step 2: Importing the GL CSV

The GL CSV file contains detailed general ledger information. The `DESC` fields are especially relevant, as they may contain strings that match or partially match with data from the SBA CSV.

- **Fields**:
  - `GL ACCOUNT NBR`: General Ledger Account Number
  - `GL AU NBR`: General Ledger Authorization Number
  - `ENTERED AMOUNT DR/(CR)`: Debit or Credit amount
  - `DR/CR CODE`: Debit/Credit indicator
  - `EFFECTIVE DATE`: Date of transaction effectiveness
  - `ENT DATE`: Entry date
  - `DESC 1`, `DESC 2`, `DESC 3`, `DESC 4`, `DESC 7`: Description fields (used for matching to SBA data)
  - `EXTERNAL REFERENCE`: External reference ID
  - `ORACLE GL CATEGORY NAME`: Oracle GL category name
  - `OUTPUT CYCLE`, `OUTPUT RUN ID`: Output cycle and run identifiers
  - `EAGLE BATCH ID`, `JOURNAL ID NBR`, `JOURNAL LINE NBR`: Journal and batch identifiers
  - `PK`: Primary key
  - `GL_NBR`: General Ledger number
  - `7Y_FLG`: 7-Year flag indicator

To load this CSV:

1. Place the GL CSV file in the working directory or specify its path.
2. Use the `import_gl_csv` function to load the GL CSV as a DataFrame, enabling further analysis.

```python
def import_gl_csv(file_path):
    return pd.read_csv(file_path)
```

### Step 3: Standardizing Column Names

The project standardizes column names to follow a consistent naming convention: lowercase letters with underscores instead of spaces, removing non-alphanumeric characters (except underscores). This ensures easier handling and alignment across all datasets.

**Column Renaming Function**

```python
def rename_columns(dataframe):
    dataframe.columns = (
        dataframe.columns
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(r'[^a-zA-Z0-9_]', "", regex=True)
        .str.replace(r'__+', '_', regex=True)
    )
    return dataframe
```

### Example Usage

Use the following code to specify paths, import the CSV files, and verify the data:

```python
def main():
    sba_csv_path = "path/to/sba.csv"
    gl_csv_path = "path/to/gl.csv"

    sba_df = rename_columns(import_sba_csv(sba_csv_path))
    gl_df = rename_columns(import_gl_csv(gl_csv_path))

    print("SBA DataFrame:")
    print(sba_df.head())

    print("\nGL DataFrame:")
    print(gl_df.head())

if __name__ == "__main__":
    main()
```

By following these steps, you’ll have a structured import process for both the SBA and GL datasets, ready for subsequent matching and analysis.

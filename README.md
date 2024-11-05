# Project Setup and Data Import

## Overview

This project requires importing and processing data from two main CSV files: `SBA.csv` and `GL.csv`. We use a custom `CSVImporter` class to handle CSV imports with error handling and column standardization. The importer ensures that all columns are converted to lowercase, spaces are replaced with underscores, non-alphanumeric characters are removed, and multiple underscores are collapsed to a single underscore for consistency across datasets.

The main code is located in `src/app.py`, which demonstrates the usage of the `CSVImporter` class to load both CSV files and standardize column names.

## Synthetic Sample Data

To assist with testing and verification, the project includes synthetic sample data files:

- **`data/sba.csv`**: Contains sample data with key fields for client processing:
  - `JOBID`: Unique identifier for each job
  - `CLNTNAME`: Client name
  - `CLNTKEY`: Unique client key
  - `CLACCOUNTID`: Client account ID

- **`data/gl.csv`**: Contains sample data with general ledger details. Special attention should be given to the `DESC` fields, which may contain text that partially or fully matches entries in `SBA.csv`. Key fields include:
  - `GL ACCOUNT NBR`: General Ledger Account Number
  - `GL AU NBR`: General Ledger Authorization Number
  - `ENTERED AMOUNT DR/(CR)`: Debit or Credit amount
  - `DR/CR CODE`: Debit/Credit indicator
  - `DESC 1`, `DESC 2`, `DESC 3`, `DESC 4`, `DESC 7`: Description fields for matching with SBA data
  - Other fields, such as `EXTERNAL REFERENCE`, `ORACLE GL CATEGORY NAME`, and `OUTPUT CYCLE`

## Usage

### Importing Data

The `CSVImporter` class is used to import both `SBA.csv` and `GL.csv` files. When importing, the class automatically standardizes column names. Error handling ensures that file paths are validated and logs provide informative output for each import operation. 

### Running the Import Process

The main entry point for data import and validation is `src/app.py`. This script initializes the `CSVImporter` and imports the `SBA.csv` and `GL.csv` files located in the `data` directory.

Simply execute `src/app.py` to:

1. Import `SBA.csv` and `GL.csv`.
2. Standardize all column names in each DataFrame.
3. Print a preview of the data, including the shape and first few rows of each DataFrame.

This setup allows for flexible updates and easy testing of the data import process. For further analysis, the imported DataFrames can be used to perform matching, filtering, and other data processing tasks.

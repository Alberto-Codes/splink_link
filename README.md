# Project Setup and Data Import

## Overview

This project requires importing and processing data from two main CSV files: `SBA.csv` and `GL.csv`. We use a custom `CSVImporter` class to handle CSV imports with error handling and column standardization. The importer ensures that all columns are converted to lowercase, spaces are replaced with underscores, non-alphanumeric characters are removed, and multiple underscores are collapsed to a single underscore for consistency across datasets.

The main code is located in `src/app.py`, which demonstrates the usage of the `CSVImporter` class to load both CSV files, standardize column names, and generate hybrid fields for comparisons.

## Synthetic Sample Data

To assist with testing and verification, the project includes synthetic sample data files:

- **`data/sba.csv`**: Contains sample data with key fields for client processing:
  - `JOBID`: Unique identifier for each job
  - `CLNTNAME`: Client name
  - `CLNTKEY`: Unique client key
  - `CLACCOUNTID`: Client account ID

- **`data/gl.csv`**: Contains sample data with general ledger details. Special attention is given to the `DESC` fields, which may contain text that partially or fully matches entries in `SBA.csv`. Key fields include:
  - `GL ACCOUNT NBR`: General Ledger Account Number
  - `GL AU NBR`: General Ledger Authorization Number
  - `ENTERED AMOUNT DR/(CR)`: Debit or Credit amount
  - `DR/CR CODE`: Debit/Credit indicator
  - `DESC 1`, `DESC 2`, `DESC 3`, `DESC 4`, `DESC 7`: Description fields for matching with SBA data
  - Additional fields, such as `EXTERNAL REFERENCE`, `ORACLE GL CATEGORY NAME`, and `OUTPUT CYCLE`

## Usage

### Importing Data and Creating Hybrid Fields

The `CSVImporter` class is used to import both `SBA.csv` and `GL.csv` files. When importing, the class automatically standardizes column names. Additionally, each DataFrame is assigned a `unique_id` column, which is required for compatibility with Splink, a record linkage tool used in this project.

After importing, hybrid fields are generated to facilitate comparisons between SBA and GL records. Hybrid fields are combinations of SBA and GL columns in a format that allows Splink to compare possible matches across multiple fields.

### Hybrid Fields Creation

For comparison, the project generates hybrid fields by pairing each specified field in the SBA dataset (e.g., `clntname`, `clntkey`, `claccountid`) with each `DESC` field in the GL dataset. For example:
- `clntname-desc_1` in the SBA dataset will contain `clntname`, and in the GL dataset, it will contain data from `desc_1`.
- These combinations extend to each SBA field paired with every `DESC` field in GL, such as `clntkey-desc_2`, `claccountid-desc_3`, etc.

These hybrid fields allow Splink to detect potential matches across various descriptive fields even when exact matches might not occur directly in the original columns.

### Running the Import and Comparison Process

The main entry point for data import and hybrid field generation is `src/app.py`. This script performs the following:

1. Imports `SBA.csv` and `GL.csv` as DataFrames.
2. Standardizes column names in each DataFrame.
3. Adds a `unique_id` column for each DataFrame, which is required for Splink compatibility.
4. Generates comparison DataFrames with hybrid fields, preparing the data for linkage analysis.

To run the import and hybrid field generation process:

1. Update the paths in `src/app.py` to point to your `SBA.csv` and `GL.csv` files in the `data` directory.
2. Execute `src/app.py` to print previews of the imported DataFrames with `unique_id` and hybrid comparison fields.

**Example Command:**
```bash
python src/app.py
```

---

This setup provides a comprehensive foundation for importing, standardizing, and generating comparison-ready DataFrames for further analysis with Splink. For additional details on linking records with Splink, consult the [Splink documentation](https://moj-analytical-services.github.io/splink/).
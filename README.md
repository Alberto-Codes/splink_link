## Project Setup and Data Import

### Step 1: Import the SBA CSV as a DataFrame

This project requires loading an SBA CSV file that contains essential fields for client data processing. The CSV should include the following columns:

- `JOBID`: Unique identifier for each job
- `CLNTNAME`: Name of the client
- `CLNTKEY`: Unique client key
- `CLACCOUNTID`: Client account ID

To import this CSV into the project, follow these steps:

1. Ensure the CSV file is accessible within the working directory or specify its path.
2. Import the CSV as a DataFrame using `pandas`.

### Step 2: Import the GL CSV as a DataFrame

In addition to the SBA CSV, this project requires importing a GL CSV file that contains extensive details. The key focus will be on the `DESC` fields, which include data strings that may align in full or partially with information from the SBA CSV file.

#### GL CSV Fields

The GL CSV contains the following fields (some of which will be central to data processing):

- `GL ACCOUNT NBR`: General Ledger Account Number
- `GL AU NBR`: General Ledger Authorization Number
- `ENTERED AMOUNT DR/(CR)`: Debit or Credit amount
- `DR/CR CODE`: Debit/Credit indicator
- `EFFECTIVE DATE`: Date of transaction effectiveness
- `ENT DATE`: Entry date
- `DESC 1`, `DESC 2`, `DESC 3`, `DESC 4`, `DESC 7`: Description fields (important for matching to SBA data)
- `EXTERNAL REFERENCE`: External reference ID
- `ORACLE GL CATEGORY NAME`: Category name from Oracle GL
- `OUTPUT CYCLE`, `OUTPUT RUN ID`: Cycle and run identifiers
- `EAGLE BATCH ID`, `JOURNAL ID NBR`, `JOURNAL LINE NBR`: IDs associated with journal and batch entries
- `PK`: Primary key
- `GL_NBR`: General Ledger number
- `7Y_FLG`: 7-Year flag indicator

#### Importing the GL CSV

To import this GL CSV file, follow the steps below:

1. Make sure the GL CSV file is accessible in your working directory or specify the appropriate path.
2. Load the file as a DataFrame in `pandas`, enabling further analysis, particularly for the `DESC` fields that will match with the SBA data.
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
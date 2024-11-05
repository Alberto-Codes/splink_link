import logging
from pathlib import Path
from typing import Optional, Union

import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CSVImporter:
    """A class to handle CSV file imports and column standardization."""

    def __init__(self, encoding: str = "utf-8"):
        """
        Initializes the CSVImporter.

        Args:
            encoding (str): Character encoding to use when reading files.
                Defaults to 'utf-8'.
        """
        self.encoding = encoding

    def import_csv(
        self, file_path: Union[str, Path], standardize_columns: bool = True, **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Imports a CSV file as a pandas DataFrame with error handling.

        Args:
            file_path (Union[str, Path]): Path to the CSV file.
            standardize_columns (bool): Whether to standardize column names.
                Defaults to True.
            **kwargs: Additional arguments to pass to `pd.read_csv`.

        Returns:
            Optional[pd.DataFrame]: DataFrame if successful; None if import fails.

        Raises:
            FileNotFoundError: If the specified file doesn't exist.
            Exception: For any other error during import.
        """
        file_path = Path(file_path)

        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            logger.info(f"Importing CSV file: {file_path}")
            df = pd.read_csv(file_path, encoding=self.encoding, **kwargs)

            if standardize_columns:
                df = self._standardize_column_names(df)

            df["unique_id"] = range(1, len(df) + 1)

            logger.info(f"Successfully imported {len(df)} rows from {file_path}")
            return df

        except Exception as e:
            logger.error(f"Error importing {file_path}: {str(e)}")
            raise

    @staticmethod
    def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes DataFrame column names to a consistent format.

        Transforms column names to:
        - Lowercase
        - Replaces spaces with underscores
        - Removes non-alphanumeric characters (except underscores)
        - Collapses multiple underscores

        Args:
            df (pd.DataFrame): Input DataFrame.

        Returns:
            pd.DataFrame: DataFrame with standardized column names.
        """
        df.columns = (
            df.columns.str.lower()
            .str.replace(" ", "_")
            .str.replace(r"[^a-zA-Z0-9_]", "", regex=True)
            .str.replace(r"__+", "_", regex=True)
        )
        return df


def main():
    """
    Main function to demonstrate the usage of the CSVImporter class.

    Demonstrates importing and standardizing column names for two example CSV files.
    """
    try:
        importer = CSVImporter()

        # Example file paths - replace with actual paths
        sba_path = "data/sba.csv"
        gl_path = "data/gl.csv"

        # Import CSV files
        sba_df = importer.import_csv(sba_path)
        gl_df = importer.import_csv(gl_path)

        # Display sample data
        for name, df in [("SBA", sba_df), ("GL", gl_df)]:
            print(f"\n{name} DataFrame Preview:")
            print(f"Shape: {df.shape}")
            print(f"Columns: {', '.join(df.columns)}")
            print("\nFirst few rows:")
            print(df.head())

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()

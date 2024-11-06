import logging
from pathlib import Path
from typing import Optional, Tuple, Union

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
                Defaults to "utf-8".
        """
        self.encoding = encoding

    def import_csv(
        self, file_path: Union[str, Path], standardize_columns: bool = True, **kwargs
    ) -> Optional[pd.DataFrame]:
        """
        Imports a CSV file as a pandas DataFrame with optional column standardization
        and adds a unique identifier column.

        Args:
            file_path (Union[str, Path]): Path to the CSV file.
            standardize_columns (bool): Whether to standardize column names.
                Defaults to True.
            **kwargs: Additional arguments to pass to `pd.read_csv`.

        Returns:
            Optional[pd.DataFrame]: DataFrame with an added `unique_id` column if
            import is successful; None if import fails.

        Raises:
            FileNotFoundError: If the specified file does not exist.
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

            # Add a unique_id for Splink compatibility
            df["unique_id"] = range(1, len(df) + 1)

            logger.info(f"Successfully imported {len(df)} rows from {file_path}")
            return df

        except Exception as e:
            logger.error(f"Error importing {file_path}: {str(e)}")
            raise

    @staticmethod
    def _standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes DataFrame column names to lowercase, replaces spaces with
        underscores, removes non-alphanumeric characters, and collapses multiple
        underscores.

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


def create_comparison_df(
    sba_df: pd.DataFrame, gl_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Creates comparison DataFrames by generating hybrid columns that combine
    specified fields from the SBA and GL DataFrames, preparing them for
    record linkage or similarity analysis.

    Args:
        sba_df (pd.DataFrame): DataFrame containing SBA data with a `unique_id` column.
        gl_df (pd.DataFrame): DataFrame containing GL data with a `unique_id` column.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]: Two DataFrames for SBA and GL with hybrid
        fields based on specific columns, ready for comparison.
    """
    sba_fields = ["jobid", "clntname", "clntkey", "claccountid"]
    gl_desc_fields = [col for col in gl_df.columns if col.startswith("desc")]

    # Initialize empty DataFrames with unique_id
    sba_comp_df = pd.DataFrame({"unique_id": sba_df["unique_id"]})
    gl_comp_df = pd.DataFrame({"unique_id": gl_df["unique_id"]})

    # Create hybrid fields for comparison
    for sba_field in sba_fields:
        for gl_desc in gl_desc_fields:
            sba_comp_df[f"{sba_field}_{gl_desc}"] = sba_df[sba_field]
            gl_comp_df[f"{sba_field}_{gl_desc}"] = gl_df[gl_desc]

    return sba_comp_df, gl_comp_df


def main():
    """
    Main function to demonstrate the usage of the CSVImporter class and the
    creation of comparison DataFrames.

    Demonstrates importing and standardizing column names, adding unique IDs,
    and generating comparison fields from SBA and GL data.
    """
    try:
        importer = CSVImporter()

        # Example file paths - replace with actual paths
        sba_path = "data/sba.csv"
        gl_path = "data/gl.csv"

        # Import CSV files and add unique_id
        sba_df = importer.import_csv(sba_path)
        gl_df = importer.import_csv(gl_path)

        # Create comparison DataFrames
        sba_comp_df, gl_comp_df = create_comparison_df(sba_df, gl_df)

        # Display sample data with unique_id and comparison fields
        print("\nSBA Comparison DataFrame Preview:")
        print(sba_comp_df.head())

        print("\nGL Comparison DataFrame Preview:")
        print(gl_comp_df.head())

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()

import logging
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd
import splink.comparison_library as cl
from splink import DuckDBAPI, Linker, SettingsCreator, block_on
from splink.exploratory import completeness_chart

from app import CSVImporter, create_comparison_df

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class SBAGLLinker:
    """Handles record linkage between SBA and GL DataFrames using Splink."""

    def __init__(
        self, sba_df: pd.DataFrame, gl_df: pd.DataFrame, threshold: float = 0.9
    ):
        """
        Initializes the SBAGLLinker with SBA and GL DataFrames and a threshold
        for match probability.

        Args:
            sba_df (pd.DataFrame): SBA comparison DataFrame.
            gl_df (pd.DataFrame): GL comparison DataFrame.
            threshold (float): Minimum match probability threshold, between 0 and 1.
                Defaults to 0.9.
        """
        self.sba_df = sba_df
        self.gl_df = gl_df
        self.threshold = threshold
        self.hybrid_columns = self._get_hybrid_columns()
        self.linker = None

    def _get_hybrid_columns(self) -> List[str]:
        """
        Retrieves a list of hybrid columns present in both SBA and GL DataFrames.

        Returns:
            List[str]: List of column names that exist in both DataFrames,
            excluding 'unique_id'.
        """
        sba_cols = set(self.sba_df.columns)
        gl_cols = set(self.gl_df.columns)
        return sorted(list(sba_cols.intersection(gl_cols) - {"unique_id"}))

    def _create_settings(self) -> SettingsCreator:
        """
        Creates a Splink settings object with configurations for comparisons,
        blocking rules, and deterministic rules for training.

        Returns:
            SettingsCreator: Configuration object for Splink.
        """
        # Create blocking rules based on hybrid fields
        blocking_rules = [
            block_on(col) for col in self.hybrid_columns[:2]
        ]  # First two fields

        # Create comparison definitions
        comparisons = [
            cl.TextComparison(
                col,
                comparison_levels=[
                    cl.exact_match(term_frequency_adjustments=True),
                    cl.jaro_winkler(threshold=0.9),
                    cl.jaro_winkler(threshold=0.8),
                    cl.levenshtein(threshold=3),
                ],
            )
            for col in self.hybrid_columns
        ]

        # Create deterministic rules for training
        deterministic_rules = [f"l.{col} = r.{col}" for col in self.hybrid_columns[:3]]

        return SettingsCreator(
            link_type="link_only",
            blocking_rules_to_generate_predictions=blocking_rules,
            comparisons=comparisons,
            deterministic_rules=deterministic_rules,
        )

    def train_model(self) -> None:
        """
        Initializes and trains the Splink model by estimating probabilities
        and parameters using a combination of deterministic and EM-based methods.

        Raises:
            Exception: If an error occurs during model training.
        """
        try:
            logger.info("Initializing Splink linker...")

            # Initialize linker
            self.linker = Linker(
                [self.sba_df, self.gl_df],
                self._create_settings(),
                db_api=DuckDBAPI(),
                input_table_aliases=["sba", "gl"],
            )

            # Analyze data completeness
            logger.info("Analyzing data completeness...")
            completeness_chart(
                [self.sba_df, self.gl_df],
                cols=self.hybrid_columns,
                db_api=DuckDBAPI(),
                table_names_for_chart=["SBA", "GL"],
            )

            # Train model
            logger.info("Training model...")

            # Estimate probability of random matches
            self.linker.training.estimate_probability_two_random_records_match(
                self.linker.settings.deterministic_rules, recall=0.7
            )

            # Estimate u parameters
            self.linker.training.estimate_u_using_random_sampling(max_pairs=1e8)

            # Train parameters using EM for each blocking rule
            for col in self.hybrid_columns[:3]:  # Train on first three columns
                logger.info(f"Training parameters blocking on {col}...")
                self.linker.training.estimate_parameters_using_expectation_maximisation(
                    block_on(col)
                )

            logger.info("Model training completed")

        except Exception as e:
            logger.error(f"Error in model training: {str(e)}")
            raise

    def find_matches(self) -> pd.DataFrame:
        """
        Generates and returns matched records based on the trained model.

        Returns:
            pd.DataFrame: DataFrame containing matched records with match
            probabilities.

        Raises:
            ValueError: If the model is not trained before calling this method.
            Exception: If an error occurs during match generation.
        """
        try:
            if self.linker is None:
                raise ValueError("Model must be trained before finding matches")

            logger.info(f"Generating matches with threshold {self.threshold}...")
            results = self.linker.inference.predict(
                threshold_match_probability=self.threshold
            )

            # Convert to pandas DataFrame
            matches_df = results.as_pandas_dataframe()

            logger.info(
                f"Found {len(matches_df)} matches with probability >= {self.threshold}"
            )

            return matches_df

        except Exception as e:
            logger.error(f"Error in match generation: {str(e)}")
            raise


def main():
    """
    Main function to demonstrate the record linkage process.

    Demonstrates importing data, creating comparison DataFrames, initializing
    SBAGLLinker, training the model, finding matches, and saving matched results.
    """
    try:
        # Import data (using your existing CSVImporter)
        importer = CSVImporter()
        sba_df = importer.import_csv("data/sba.csv")
        gl_df = importer.import_csv("data/gl.csv")

        # Create comparison DataFrames
        sba_comp_df, gl_comp_df = create_comparison_df(sba_df, gl_df)

        # Initialize and train linker
        linker = SBAGLLinker(sba_comp_df, gl_comp_df, threshold=0.9)
        linker.train_model()

        # Get matches
        matches = linker.find_matches()

        # Display results
        print("\nTop matches:")
        print(matches.head())

        # Save results with additional information
        matches.to_csv(
            "output/matches.csv",
            index=False,
            float_format="%.3f",  # Format probabilities to 3 decimal places
        )
        logger.info("Matches saved to output/matches.csv")

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise


if __name__ == "__main__":
    main()

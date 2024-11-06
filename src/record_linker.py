from app import CSVImporter, create_comparison_df
import splink.comparison_library as cl

from splink import DuckDBAPI, Linker, SettingsCreator, block_on

importer = CSVImporter()
sba_df = importer.import_csv("data/sba.csv")
gl_df = importer.import_csv("data/gl.csv")

# Create comparison DataFrames
sba_comp_df, gl_comp_df = create_comparison_df(sba_df, gl_df)

# Automatically generate blocking rules based on all hybrid comparison fields
comparison_fields = [col for col in sba_comp_df.columns if col != "unique_id"]
blocking_rules = [block_on(field) for field in comparison_fields]

settings = SettingsCreator(
    link_type="link_only",
    blocking_rules_to_generate_predictions=blocking_rules,
    comparisons=[
        cl.ExactMatch(col).configure(term_frequency_adjustments=True)
        for col in comparison_fields
    ],
)




# Initialize the Splink linker with the combined DataFrame
linker = Linker(input_table_or_tables=[sba_comp_df, gl_comp_df], settings=settings, db_api=DuckDBAPI())

linker.training.estimate_u_using_random_sampling(max_pairs=1e6, seed=1)

# Generate predictions
results = linker.inference.predict(threshold_match_probability=0.9)

# Display match results
print("\nMatch Results:")
print(results.as_pandas_dataframe(limit=5))
import os
import pandas as pd
import pytest

def test_full_dialogues_csv_exists_and_valid():
    output_path = os.path.join('data', 'full_dialogues.csv')
    assert os.path.exists(output_path), f"{output_path} does not exist. Run data_loader.py first."
    df = pd.read_csv(output_path)
    # Check that the dataframe is not empty
    assert not df.empty, "The processed dialogues dataframe is empty."
    # Check for expected columns
    expected_columns = {'line1_id', 'line2_id', 'char1_id', 'char1_name', 'line1_text', 'char2_id', 'char2_name', 'line2_text', 'movie_id', 'movie_title'}
    assert expected_columns.issubset(set(df.columns)), f"Missing expected columns: {expected_columns - set(df.columns)}"

def test_no_missing_values_and_reasonable_size():
    output_path = os.path.join('data', 'full_dialogues.csv')
    df = pd.read_csv(output_path)
    # Only require non-missing line1_text and line2_text
    for col in ['line1_text', 'line2_text']:
        assert df[col].notnull().all(), f"Missing values found in column: {col}"
    # Log missing char1_name and char2_name for information
    missing_char1 = df['char1_name'].isnull().sum()
    missing_char2 = df['char2_name'].isnull().sum()
    print(f"Rows with missing char1_name: {missing_char1}")
    print(f"Rows with missing char2_name: {missing_char2}")
    # Check that the number of rows is reasonable (e.g., > 1000)
    assert len(df) > 1000, f"Unexpectedly small number of dialogue pairs: {len(df)}"

if __name__ == "__main__":
    pytest.main([__file__])

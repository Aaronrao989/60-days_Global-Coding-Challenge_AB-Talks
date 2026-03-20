import pandas as pd
import numpy as np
def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df
def compute_statistics(data):
    mean_val = np.mean(data)
    median_val = np.median(data)
    mode_val = pd.Series(data).mode().tolist()
    variance_val = np.var(data)
    std_dev_val = np.std(data)
    return mean_val, median_val, mode_val, variance_val, std_dev_val
def display_results(column_name, mean_v, median_v, mode_v, var_v, std_v):
    print("\n" + "-" * 70)
    print(f"STATISTICAL ANALYSIS FOR: {column_name.upper()}")
    print("-" * 70)
    print(f"{'Mean':<20}: {mean_v:.2f}")
    print(f"{'Median':<20}: {median_v:.2f}")
    print(f"{'Mode':<20}: {mode_v}")
    print(f"{'Variance':<20}: {var_v:.2f}")
    print(f"{'Std Deviation':<20}: {std_v:.2f}")
    print("-" * 70)
    print("Statistical Analysis Completed Successfully.")
def main():
    print("\n" + "=" * 70)
    print("DATASET STATISTICAL ANALYSIS SYSTEM")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        df = load_dataset(file_path)
        print("\nAvailable Columns:")
        print(list(df.columns))
        column = input("\nEnter column name for analysis (e.g., charges): ")
        if column not in df.columns:
            print("⚠ Column not found in dataset.")
            return
        if not pd.api.types.is_numeric_dtype(df[column]):
            print("⚠ Selected column is not numeric.")
            return
        data = df[column].dropna()
        mean_v, median_v, mode_v, var_v, std_v = compute_statistics(data)
        display_results(column, mean_v, median_v, mode_v, var_v, std_v)
    except FileNotFoundError:
        print("⚠ CSV file not found. Please check the path.")
    except Exception as e:
        print(f"⚠ Error occurred: {e}")
if __name__ == "__main__":
    main()
import pandas as pd
from scipy import stats
def load_dataset(file_path):
    return pd.read_csv(file_path)
def perform_t_test(df):
    smokers = df[df["smoker"] == "yes"]["charges"]
    non_smokers = df[df["smoker"] == "no"]["charges"]
    t_stat, p_value = stats.ttest_ind(smokers, non_smokers)
    return smokers, non_smokers, t_stat, p_value
def interpret_result(p_value, alpha=0.05):
    print("\n" + "-" * 70)
    print("HYPOTHESIS TEST RESULT")
    print("-" * 70)
    print(f"P-value: {p_value:.6f}")
    if p_value < alpha:
        print("Result: Reject the Null Hypothesis")
        print("Conclusion: There is a significant difference in charges between smokers and non-smokers.")
    else:
        print("Result: Fail to Reject the Null Hypothesis")
        print("Conclusion: No significant difference found.")
    print("-" * 70)
def main():
    print("\n" + "=" * 70)
    print("T-TEST ANALYSIS (SMOKER vs NON-SMOKER)")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        df = load_dataset(file_path)
        print("\nDataset Preview:")
        print(df.head())
        smokers, non_smokers, t_stat, p_value = perform_t_test(df)
        print("\nSmoker Charges Sample:", smokers.head().tolist())
        print("Non-Smoker Charges Sample:", non_smokers.head().tolist())
        print(f"\nT-statistic: {t_stat:.4f}")
        interpret_result(p_value)
    except FileNotFoundError:
        print("⚠ CSV file not found. Please check the path.")
    except Exception as e:
        print(f"⚠ Error occurred: {e}")
if __name__ == "__main__":
    main()
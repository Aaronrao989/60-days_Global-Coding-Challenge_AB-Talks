import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
def main():
    print("\n" + "=" * 70)
    print("LINEAR REGRESSION - FEATURE IMPACT ANALYSIS")
    print("=" * 70)
    df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day17.csv")
    X = df[["age", "bmi", "children"]]
    y = df["charges"]
    model = LinearRegression()
    model.fit(X, y)
    predictions = model.predict(X)
    r2 = r2_score(y, predictions)
    print(f"\nR² Score: {r2:.4f}")
    print("\nFeature Impact (Coefficients):")
    for feature, coef in zip(X.columns, model.coef_):
        print(f"{feature}: {coef:.2f}")
    plt.scatter(y, predictions)
    plt.xlabel("Actual Charges")
    plt.ylabel("Predicted Charges")
    plt.title("Actual vs Predicted Values")
    plt.plot([y.min(), y.max()], [y.min(), y.max()], color="red")
    plt.show()
if __name__ == "__main__":
    main()
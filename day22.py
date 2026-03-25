import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

def load_data(file_path):
    return pd.read_csv(file_path)
def preprocess_data(df):
    df = pd.get_dummies(df, columns=["sex", "smoker", "region"], drop_first=True)
    return df
def train_model(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model
def evaluate_model(y_test, predictions):
    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    print("\n" + "-" * 70)
    print("MODEL EVALUATION")
    print("-" * 70)
    print(f"Mean Absolute Error (MAE): {mae:.2f}")
    print(f"Mean Squared Error (MSE): {mse:.2f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
    print("-" * 70)
def main():
    print("\n" + "=" * 70)
    print("MACHINE LEARNING WORKFLOW (PRACTICAL)")
    print("=" * 70)
    file_path = input("\nEnter CSV file path: ")
    try:
        df = load_data(file_path)
        print("\nDataset Preview:")
        print(df.head())
        df = preprocess_data(df)
        X = df.drop("charges", axis=1)
        y = df["charges"]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model = train_model(X_train, y_train)
        predictions = model.predict(X_test)
        print("\nSample Predictions vs Actual:")
        for i in range(5):
            print(f"Predicted: {predictions[i]:.2f} | Actual: {y_test.iloc[i]:.2f}")
        evaluate_model(y_test, predictions)
        print("\nML Workflow Completed Successfully.")
    except FileNotFoundError:
        print("⚠ File not found.")
    except Exception as e:
        print(f"Error: {e}")
if __name__ == "__main__":
    main()
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score


def create_structured_data():
    data = {
        "Age": [
            25,25,25,25,  45,45,45,45,
            25,25,25,25,  45,45,45,45
        ],
        "Total_Price": [
            200,200,800,800,  200,200,800,800,
            200,200,800,800,  200,200,800,800
        ],
        "Rating": [
            5,3,5,3,  5,3,5,3,
            5,3,5,3,  5,3,5,3
        ],
        "Loyalty": [
            1,1,1,1,  1,1,1,1,
            0,0,0,0,  0,0,0,0
        ],
        "Order_Status": [
            1,0,1,0,
            0,1,0,1,
            1,0,0,1,
            0,1,1,0
        ]
    }
    return pd.DataFrame(data)


def main():
    print("\n" + "=" * 70)
    print("STRUCTURED DECISION TREE (WITH EVALUATION)")
    print("=" * 70)

    df = create_structured_data()

    print("\nDataset Preview:")
    print(df.head())

    # Features & Target
    X = df.drop("Order_Status", axis=1)
    y = df["Order_Status"]

    print("\nFeatures:", list(X.columns))
    print("Target: Order_Status")

    # Train model (no split to preserve clean structure)
    model = DecisionTreeClassifier(max_depth=3)
    model.fit(X, y)

    # Predictions
    predictions = model.predict(X)

    print("\nSample Predictions vs Actual:")
    for i in range(6):
        print(f"Predicted: {predictions[i]} | Actual: {y.iloc[i]}")

    # Accuracy
    accuracy = accuracy_score(y, predictions)
    print(f"\nModel Accuracy: {accuracy:.2f}")

    # 🌳 Visualization
    plt.figure(figsize=(16, 10))
    plot_tree(
        model,
        feature_names=X.columns,
        class_names=["Cancelled", "Completed"],
        filled=True,
        rounded=True
    )
    plt.title("Well-Structured 3-Level Decision Tree")
    plt.show()


if __name__ == "__main__":
    main()
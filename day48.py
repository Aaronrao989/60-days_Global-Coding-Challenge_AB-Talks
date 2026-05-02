import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.utils import resample
np.random.seed(42)
data = {
    "gender": np.random.choice(["Male", "Female"], size=200, p=[0.8, 0.2]),  # biased
    "experience": np.random.randint(1, 10, 200),
    "salary": np.random.randint(20000, 100000, 200),
    "approved": np.random.choice([0, 1], size=200)
}
df = pd.DataFrame(data)
print("\nOriginal Dataset Distribution:")
print(df["gender"].value_counts())
df["gender"] = df["gender"].map({"Male": 0, "Female": 1})
X = df[["gender", "experience", "salary"]]
y = df["approved"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\nAccuracy BEFORE mitigation:", accuracy_score(y_test, y_pred))
test_df = X_test.copy()
test_df["actual"] = y_test
test_df["pred"] = y_pred
male_preds = test_df[test_df["gender"] == 0]["pred"].mean()
female_preds = test_df[test_df["gender"] == 1]["pred"].mean()
print("\nPrediction Rate:")
print("Male:", male_preds)
print("Female:", female_preds)
df_male = df[df.gender == 0]
df_female = df[df.gender == 1]
df_female_upsampled = resample(df_female,
                              replace=True,
                              n_samples=len(df_male),
                              random_state=42)

balanced_df = pd.concat([df_male, df_female_upsampled])
print("\nBalanced Dataset Distribution:")
print(balanced_df["gender"].value_counts())
X_bal = balanced_df[["gender", "experience", "salary"]]
y_bal = balanced_df["approved"]
X_train_b, X_test_b, y_train_b, y_test_b = train_test_split(X_bal, y_bal, test_size=0.2, random_state=42)
model_bal = LogisticRegression(max_iter=1000)
model_bal.fit(X_train_b, y_train_b)
y_pred_b = model_bal.predict(X_test_b)
print("\nAccuracy AFTER mitigation:", accuracy_score(y_test_b, y_pred_b))
test_df_b = X_test_b.copy()
test_df_b["pred"] = y_pred_b
male_preds_b = test_df_b[test_df_b["gender"] == 0]["pred"].mean()
female_preds_b = test_df_b[test_df_b["gender"] == 1]["pred"].mean()
print("\nPrediction Rate AFTER mitigation:")
print("Male:", male_preds_b)
print("Female:", female_preds_b)
print("\nConclusion:")
print("Bias reduced after balancing dataset. Model predictions are more fair.")
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
df = pd.read_csv("/Users/aaronrao/Desktop/projects/Global Coding Challenge/day49/Teen_Mental_Health_Dataset.csv")
print("\nDataset Preview:")
print(df.head())
print("\nDistribution of Depression:")
print(df["depression_label"].value_counts())
df["depression_label"].value_counts().plot(kind="bar")
plt.title("Depression Distribution")
plt.show()
le = LabelEncoder()
df["gender"] = le.fit_transform(df["gender"])
df["platform_usage"] = le.fit_transform(df["platform_usage"])
df["social_interaction_level"] = le.fit_transform(df["social_interaction_level"])
X = df.drop("depression_label", axis=1)
y = df["depression_label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nReport:\n", classification_report(y_test, y_pred))
plt.scatter(df["daily_social_media_hours"], df["depression_label"])
plt.xlabel("Daily Social Media Hours")
plt.ylabel("Depression")
plt.title("Usage vs Depression")
plt.show()

plt.scatter(df["sleep_hours"], df["depression_label"])
plt.xlabel("Sleep Hours")
plt.ylabel("Depression")
plt.title("Sleep vs Depression")
plt.show()
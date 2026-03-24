def ml_workflow():
    print("\n" + "=" * 70)
    print("MACHINE LEARNING WORKFLOW")
    print("=" * 70)

    print("""
1. Data Collection:
   Gathering data from various sources such as databases, APIs, or CSV files.

2. Data Preprocessing:
   Cleaning data, handling missing values, encoding categorical variables,
   and scaling features.

3. Exploratory Data Analysis (EDA):
   Understanding patterns, distributions, and relationships in the data.

4. Feature Engineering:
   Creating or selecting important features that improve model performance.

5. Model Selection:
   Choosing appropriate algorithms (e.g., Linear Regression, Decision Trees).

6. Model Training:
   Training the model using training data.

7. Model Evaluation:
   Evaluating performance using metrics like accuracy, precision, recall, etc.

8. Model Deployment:
   Deploying the model into real-world applications.

9. Monitoring & Improvement:
   Continuously monitoring and improving the model.
""")


def learning_types():
    print("\n" + "=" * 70)
    print("SUPERVISED vs UNSUPERVISED LEARNING")
    print("=" * 70)

    print("""
Supervised Learning:
- Data is labeled (input + output known)
- Goal: Predict output from input

Examples:
• Predicting house prices (Regression)
• Spam email detection (Classification)
• Predicting medical charges (your dataset)

Unsupervised Learning:
- Data is unlabeled (no output given)
- Goal: Find hidden patterns or structure

Examples:
• Customer segmentation (Clustering)
• Grouping similar users
• Anomaly detection
""")


def real_world_examples():
    print("\n" + "=" * 70)
    print("REAL-WORLD PROBLEM CLASSIFICATION")
    print("=" * 70)

    print("""
1. Predicting insurance charges → Supervised (Regression)
2. Email spam detection → Supervised (Classification)
3. Customer segmentation → Unsupervised (Clustering)
4. Fraud detection → Unsupervised / Semi-supervised
5. Movie recommendation → Unsupervised / Hybrid
""")
def main():
    ml_workflow()
    learning_types()
    real_world_examples()
if __name__ == "__main__":
    main()
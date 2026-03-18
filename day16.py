import seaborn as sns
import matplotlib.pyplot as plt
def plot_distribution(scores):
    plt.figure()
    sns.histplot(scores, bins=10, kde=True)
    plt.title("Distribution of Exam Scores")
    plt.xlabel("Scores")
    plt.ylabel("Frequency")
    plt.show()
def main():
    print("\n" + "=" * 70)
    print("EXAM SCORE DISTRIBUTION VISUALIZATION")
    print("=" * 70)
    scores = [55, 67, 70, 72, 75, 78, 80, 82, 85, 87, 90, 92, 95, 60, 65]
    plot_distribution(scores)
if __name__ == "__main__":
    main()
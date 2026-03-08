def count_word_frequency(sentence):
    words = sentence.lower().split()
    frequency = {}

    for word in words:
        frequency[word] = frequency.get(word, 0) + 1

    return frequency


def display_results(frequency_dict):
    print("\n" + "-" * 70)
    print("WORD FREQUENCY SUMMARY")
    print("-" * 70)

    for word, count in frequency_dict.items():
        print(f"{word:<20}: {count}")

    print("-" * 70)
    print("Text Analysis Completed Successfully.")


def main():
    print("\n" + "=" * 70)
    print("WORD FREQUENCY ANALYSIS SYSTEM")
    print("=" * 70)

    sentence = input("\nEnter a sentence: ")

    frequency_dict = count_word_frequency(sentence)

    display_results(frequency_dict)


if __name__ == "__main__":
    main()
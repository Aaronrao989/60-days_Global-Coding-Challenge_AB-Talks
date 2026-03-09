def analyze_marks(student_marks):
    marks_list = list(student_marks.values())

    total_marks = sum(marks_list)
    average_marks = total_marks / len(marks_list)

    highest_student = max(student_marks, key=student_marks.get)
    lowest_student = min(student_marks, key=student_marks.get)

    return total_marks, average_marks, highest_student, lowest_student


def display_report(student_marks, total, average, highest, lowest):
    print("\n" + "-" * 70)
    print("STUDENT MARKS SUMMARY")
    print("-" * 70)

    for student, marks in student_marks.items():
        print(f"{student:<20}: {marks}")

    print("-" * 70)
    print(f"{'Total Marks':<20}: {total}")
    print(f"{'Average Marks':<20}: {average:.2f}")
    print(f"{'Top Performer':<20}: {highest} ({student_marks[highest]})")
    print(f"{'Lowest Score':<20}: {lowest} ({student_marks[lowest]})")
    print("-" * 70)
    print("Marks Analysis Completed Successfully.")


def main():
    print("\n" + "=" * 70)
    print("STUDENT MARKS ANALYSIS SYSTEM")
    print("=" * 70)

    student_marks = {}

    n = int(input("\nEnter number of students: "))

    for i in range(n):
        name = input(f"\nEnter student {i+1} name: ")
        marks = float(input("Enter marks: "))
        student_marks[name] = marks

    total, average, highest, lowest = analyze_marks(student_marks)

    display_report(student_marks, total, average, highest, lowest)


if __name__ == "__main__":
    main()
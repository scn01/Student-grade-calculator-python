from __future__ import annotations
from gradebook import Gradebook
from plotting import plot_subjects, plot_overall
from whatif import what_if_final


def menu() -> None:
    gb = Gradebook()

    while True:
        print("\n=== Student Grade Calculator ===")
        print("1) Add student")
        print("2) Remove student")
        print("3) Add grade component")
        print("4) View student report")
        print("5) Plot graph (subject or overall)")
        print("6) What-if predictor")
        print("0) Exit")

        choice = input("Choose: ").strip()

        try:
            if choice == "1":
                sid = input("Student ID: ").strip()
                name = input("Name: ").strip()
                gb.add_student(sid, name)
                print("Student added.")

            elif choice == "2":
                sid = input("Student ID to remove: ").strip()
                gb.remove_student(sid)
                print("Student removed (and their grades).")

            elif choice == "3":
                sid = input("Student ID: ").strip()
                subject = input("Subject: ").strip()
                component = input("Component (e.g., Coursework, Midterm, Final): ").strip()
                score = float(input("Score: ").strip())
                max_score = float(input("Max score: ").strip())
                weight = float(input("Weight % (e.g., 30): ").strip())
                gb.add_grade_component(sid, subject, component, score, max_score, weight)
                print("Grade component added.")

            elif choice == "4":
                sid = input("Student ID: ").strip()
                rep = gb.stats_for_student(sid)

                print("\n--- Weight Validation ---")
                if not rep["weight_validation"]:
                    print("No subjects/grades yet.")
                else:
                    for subj, status in rep["weight_validation"].items():
                        print(f"{subj}: {status}")

                print("\n--- Subject Percentages ---")
                if not rep["subject_percentages"]:
                    print("No valid subject totals yet (weights must equal 100%).")
                else:
                    for subj, p in rep["subject_percentages"].items():
                        print(f"{subj}: {p:.2f}%")

                print("\n--- Subject Stats (from subject totals) ---")
                s = rep["subject_stats"]
                print(f"Min: {s['min']}")
                print(f"Max: {s['max']}")
                print(f"Avg: {s['avg']}")

                print("\n--- Overall ---")
                if rep["overall"] is None:
                    print("Overall: N/A (need at least one valid subject with weights totaling 100%)")
                else:
                    print(f"Overall: {rep['overall']:.2f}%")
                    print("PASS" if rep["pass_overall"] else "FAIL")
                    if rep["progress"] is None:
                        print("Progression: N/A")
                    else:
                        print("Progression: PROGRESS" if rep["progress"] else "Progression: NO")

            elif choice == "5":
                sid = input("Student ID: ").strip()
                rep = gb.stats_for_student(sid)

                print("a) Plot per subject")
                print("b) Plot overall")
                sub = input("Choose (a/b): ").strip().lower()
                if sub == "a":
                    plot_subjects(rep["subject_percentages"], title=f"Subject Percentages for {sid}")
                elif sub == "b":
                    plot_overall(rep["overall"], title=f"Overall Percentage for {sid}")

            elif choice == "6":
                sid = input("Student ID: ").strip()
                subject = input("Subject: ").strip()
                component = input("Component to predict (must already exist, e.g., Final): ").strip()
                predicted_score = float(input("Predicted score: ").strip())
                predicted_max = float(input("Predicted max score: ").strip())

                predicted = what_if_final(
                    gb.grades, sid, subject, component, predicted_score, predicted_max
                )
                if predicted is None:
                    print("Could not predict. Check:")
                    print("- subject exists")
                    print("- component exists already (so we know its weight)")
                    print("- weights total 100% for that subject")
                else:
                    print(f"Predicted final % for {subject}: {predicted:.2f}%")

            elif choice == "0":
                print("Bye!")
                break

            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    menu()

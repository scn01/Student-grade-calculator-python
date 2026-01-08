from __future__ import annotations
import matplotlib.pyplot as plt


def plot_subjects(subject_percentages: dict[str, float], title: str) -> None:
    if not subject_percentages:
        print("Nothing to plot.")
        return

    subjects = list(subject_percentages.keys())
    values = list(subject_percentages.values())

    plt.figure()
    plt.bar(subjects, values)
    plt.ylim(0, 100)
    plt.ylabel("Percentage (%)")
    plt.title(title)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.show()


def plot_overall(overall: float | None, title: str) -> None:
    if overall is None:
        print("No overall score to plot.")
        return

    plt.figure()
    plt.bar(["Overall"], [overall])
    plt.ylim(0, 100)
    plt.ylabel("Percentage (%)")
    plt.title(title)
    plt.tight_layout()
    plt.show()

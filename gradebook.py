from __future__ import annotations
import numpy as np
import pandas as pd

from config import PASS_THRESHOLD, PROGRESSION_THRESHOLD, PROGRESS_IF_GREATER_EQUAL
from storage import load_students, load_grades, save_students, save_grades


class Gradebook:
    def __init__(self) -> None:
        self.students = load_students()
        self.grades = load_grades()

    # Student management
    def add_student(self, student_id: str, name: str) -> None:
        if (self.students["student_id"] == student_id).any():
            raise ValueError("Student ID already exists.")
        self.students = pd.concat(
            [self.students, pd.DataFrame([{"student_id": student_id, "name": name}])],
            ignore_index=True
        )
        save_students(self.students)

    def remove_student(self, student_id: str) -> None:
        self.students = self.students[self.students["student_id"] != student_id].copy()
        self.grades = self.grades[self.grades["student_id"] != student_id].copy()
        save_students(self.students)
        save_grades(self.grades)

    # Subject and grade management
    def add_grade_component(
        self,
        student_id: str,
        subject: str,
        component: str,
        score: float,
        max_score: float,
        weight: float
    ) -> None:
        if not (self.students["student_id"] == student_id).any():
            raise ValueError("Student ID not found. Add the student first.")

        if max_score <= 0:
            raise ValueError("max_score must be > 0.")
        if weight <= 0:
            raise ValueError("weight must be > 0.")
        if score < 0 or score > max_score:
            raise ValueError("score must be between 0 and max_score.")

        new_row = {
            "student_id": student_id,
            "subject": subject.strip(),
            "component": component.strip(),
            "score": float(score),
            "max_score": float(max_score),
            "weight": float(weight),
        }
        self.grades = pd.concat([self.grades, pd.DataFrame([new_row])], ignore_index=True)
        save_grades(self.grades)

    def subjects(self) -> list[str]:
        if self.grades.empty:
            return []
        return sorted(self.grades["subject"].dropna().unique().tolist())

    # Making sure the weightage adds up to 100%
    def validate_subject_weights(self, student_id: str) -> dict[str, str]:
        """
        Returns dict: subject -> status message
        - "OK" if weights sum exactly to 100
        - "ERROR: ..." otherwise
        """
        df = self.grades[self.grades["student_id"] == student_id].copy()
        if df.empty:
            return {}

        statuses: dict[str, str] = {}
        for subj, g in df.groupby("subject"):
            total_w = float(np.sum(g["weight"].to_numpy(dtype=float)))
            if total_w > 100.0 + 1e-9:
                statuses[subj] = f"ERROR: weights exceed 100% (got {total_w:.2f}%)"
            elif abs(total_w - 100.0) > 1e-6:
                statuses[subj] = f"ERROR: weights must total 100% (got {total_w:.2f}%)"
            else:
                statuses[subj] = "OK"
        return statuses

    # Calculations
    def _subject_percentage(self, student_id: str, subject: str) -> float | None:
        g = self.grades[
            (self.grades["student_id"] == student_id) &
            (self.grades["subject"] == subject)
        ].copy()

        if g.empty:
            return None

        weights = g["weight"].to_numpy(dtype=float)
        total_w = float(np.sum(weights))
        if abs(total_w - 100.0) > 1e-6:
            # if invalid, return None so caller can show error
            return None

        scores = g["score"].to_numpy(dtype=float)
        max_scores = g["max_score"].to_numpy(dtype=float)

        # percentage contribution per component: (score/max)*weight
        contrib = (scores / max_scores) * weights
        return float(np.sum(contrib))

    def subject_percentages(self, student_id: str) -> dict[str, float]:
        out: dict[str, float] = {}
        for subj in self.subjects():
            p = self._subject_percentage(student_id, subj)
            if p is not None:
                out[subj] = p
        return out

    def overall_percentage(self, student_id: str) -> float | None:
        """
        Overall = average of valid subject percentages.
        """
        subj_perc = self.subject_percentages(student_id)
        if not subj_perc:
            return None
        arr = np.array(list(subj_perc.values()), dtype=float)
        return float(np.mean(arr))

    def stats_for_student(self, student_id: str) -> dict:
        """
        min/max/avg by subject and overall
        Uses NumPy for computations.
        """
        subj = self.subject_percentages(student_id)
        overall = self.overall_percentage(student_id)

        if subj:
            subj_arr = np.array(list(subj.values()), dtype=float)
            per_subj_stats = {
                "min": float(np.min(subj_arr)),
                "max": float(np.max(subj_arr)),
                "avg": float(np.mean(subj_arr)),
            }
        else:
            per_subj_stats = {"min": None, "max": None, "avg": None}

        return {
            "subject_percentages": subj,
            "overall": overall,
            "subject_stats": per_subj_stats,
            "pass_overall": (overall is not None and overall >= PASS_THRESHOLD),
            "progress": self._progression_decision(overall),
            "weight_validation": self.validate_subject_weights(student_id),
        }

    def _progression_decision(self, overall: float | None) -> bool | None:
        if overall is None:
            return None
        if PROGRESS_IF_GREATER_EQUAL:
            return overall >= PROGRESSION_THRESHOLD
        else:
            return overall <= PROGRESSION_THRESHOLD

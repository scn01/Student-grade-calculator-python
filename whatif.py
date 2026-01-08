from __future__ import annotations
import numpy as np
import pandas as pd


def what_if_final(
    grades_df: pd.DataFrame,
    student_id: str,
    subject: str,
    target_component: str,
    predicted_score: float,
    predicted_max: float
) -> float | None:
    # Predict the subject final percentage if the student scores X in Y component.
    g = grades_df[
        (grades_df["student_id"] == student_id) &
        (grades_df["subject"] == subject)
    ].copy()

    if g.empty:
        return None

    # Remove existing rows for that component (replace it with predicted)
    g = g[g["component"] != target_component].copy()

    # Need to know the weight of the target component from original dataset
    original = grades_df[
        (grades_df["student_id"] == student_id) &
        (grades_df["subject"] == subject) &
        (grades_df["component"] == target_component)
    ].copy()
    if original.empty:
        return None

    w = float(original.iloc[0]["weight"])

    if predicted_max <= 0:
        raise ValueError("predicted_max must be > 0")
    if predicted_score < 0 or predicted_score > predicted_max:
        raise ValueError("predicted_score must be between 0 and predicted_max")

    predicted_row = {
        "student_id": student_id,
        "subject": subject,
        "component": target_component,
        "score": float(predicted_score),
        "max_score": float(predicted_max),
        "weight": w
    }

    g = pd.concat([g, pd.DataFrame([predicted_row])], ignore_index=True)

    weights = g["weight"].to_numpy(dtype=float)
    if abs(np.sum(weights) - 100.0) > 1e-6:
        return None

    scores = g["score"].to_numpy(dtype=float)
    max_scores = g["max_score"].to_numpy(dtype=float)
    return float(np.sum((scores / max_scores) * weights))

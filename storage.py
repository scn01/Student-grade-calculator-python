from __future__ import annotations
import os
import pandas as pd
from config import DATA_DIR, STUDENTS_CSV, GRADES_CSV

STUDENTS_COLUMNS = ["student_id", "name"]
GRADES_COLUMNS = ["student_id", "subject", "component", "score", "max_score", "weight"]


def ensure_data_files() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)

    if not os.path.exists(STUDENTS_CSV):
        pd.DataFrame(columns=STUDENTS_COLUMNS).to_csv(STUDENTS_CSV, index=False)

    if not os.path.exists(GRADES_CSV):
        pd.DataFrame(columns=GRADES_COLUMNS).to_csv(GRADES_CSV, index=False)


def load_students() -> pd.DataFrame:
    ensure_data_files()
    df = pd.read_csv(STUDENTS_CSV)
    return df


def load_grades() -> pd.DataFrame:
    ensure_data_files()
    df = pd.read_csv(GRADES_CSV)
    return df


def save_students(df: pd.DataFrame) -> None:
    df.to_csv(STUDENTS_CSV, index=False)


def save_grades(df: pd.DataFrame) -> None:
    df.to_csv(GRADES_CSV, index=False)

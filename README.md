# Student Grade Calculator (Python)

A modular **Student Grade Management System** built in **Python**, using **NumPy**, **Pandas**, and **Matplotlib**.  
The program allows users to manage students, calculate grades, visualize results, and predict outcomes using a “what-if” analysis.

This project demonstrates clean software design, data persistence, statistical computation, and graphical visualisation — suitable for academic submission and portfolio use.

---

## ✨ Features

- 👤 Add and remove students
- 📚 Add subjects and multiple assessment components per subject
- 🧮 Calculate:
  - Subject percentages (weighted)
  - Overall percentage
  - Minimum, maximum, and average grades
- ✅ Automatic **Pass / Fail** decision (40% threshold)
- 🎓 **Progression decision** (≥ 50% required)
- 📊 Visualise grades using **Matplotlib**
  - Per subject
  - Overall performance
- 🔮 **What-If Grade Predictor**
  - Predict final scores without modifying stored data
- 💾 storage using CSV files
- 🛡  error handling
  - Invalid grades
  - Incorrect weight totals
  - Missing or empty data files
 
 ---

## 🧱 Project Structure

student-grade-calculator/
│
├── main.py # user interaction
├── gradebook.py # calculations (NumPy)
├── storage.py # CSV handling (Pandas)
├── plotting.py # Graph visualisation (Matplotlib)
├── whatif.py # What-if grade prediction logic
├── config.py # Global configuration
│
└── data/
├── students.csv # Student records
└── grades.csv # Grade and assessment data


---

## 🧮 How Grades Are Calculated

Each subject consists of assessment components whose **weights must total 100%**.

**Formula:**

The final subject percentage is the sum of all weighted components.

Overall percentage is calculated as the **average of all valid subject percentages**.

---

## 📊 Visualisation

Grades are displayed using bar charts via **Matplotlib**:
- Subject-wise performance
- Overall performance

All graphs scale automatically between 0 - 100%.

---

## 🔮 What-If Grade Predictor

The system allows hypothetical predictions such as:

> *“What if I score 75 in the Final Exam?”*

The predictor:
- Temporarily replaces the chosen assessment
- Recalculates the final subject percentage
- Leaves stored data unchanged

---

## 🗃 Data Storage

All data is stored using **CSV files** managed by Pandas:
- Automatically created and repaired if missing or empty
- Data persists between program runs

---

## ▶️ How to Run
```bash
python main.py
```

### 1️⃣ Install dependencies
```bash
pip install numpy pandas matplotlib
```

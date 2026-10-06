import random
from datetime import datetime
import numpy as np
import pandas as pd
from faker import Faker

# Seed setup for reproducible realistic data
fake = Faker("en_IN")
Faker.seed(101)
np.random.seed(101)
random.seed(101)

# --- CONFIGURATION ---
NUM_EMPLOYEES = 500
MONTHS = [
    "2023-01",
    "2023-02",
    "2023-03",
    "2023-04",
    "2023-05",
    "2023-06",
    "2023-07",
    "2023-08",
    "2023-09",
    "2023-10",
    "2023-11",
    "2023-12",
]

DEPARTMENTS = {
    "Sales": ["Sales Executive", "Account Executive", "Sales Manager"],
    "IT": ["Software Engineer", "System Analyst", "DevOps Engineer"],
    "HR": ["HR Executive", "Recruiter", "HR Manager"],
    "Finance": ["Financial Analyst", "Accountant", "Finance Lead"],
    "Operations": ["Operations Associate", "Process Lead", "Operations Manager"],
    "Marketing": [
        "Marketing Specialist",
        "SEO Analyst",
        "Content Strategist",
    ],
    "Customer Support": [
        "Support Specialist",
        "Technical Support Lead",
        "CS Executive",
    ],
}

LOCATIONS = [
    "Mumbai",
    "Bengaluru",
    "Delhi NCR",
    "Hyderabad",
    "Pune",
    "Chennai",
]

BASE_SALARIES = {
    "Sales": 45000,
    "IT": 65000,
    "HR": 40000,
    "Finance": 52000,
    "Operations": 42000,
    "Marketing": 48000,
    "Customer Support": 35000,
}

# --- 1. EMPLOYEES DATASET (500 Rows) ---
employees = []

for i in range(1, NUM_EMPLOYEES + 1):
    emp_id = f"EMP{i:04d}"
    gender = random.choice(["Male", "Female"])
    name = (
        fake.name_male()
        if gender == "Male"
        else fake.name_female()
    )

    age = random.randint(22, 58)
    # Experience bounded logically by age
    max_exp = max(0, age - 21)
    exp_years = random.randint(0, min(max_exp, 25))

    dept = random.choice(list(DEPARTMENTS.keys()))
    role = random.choice(DEPARTMENTS[dept])
    location = random.choice(LOCATIONS)

    # Hire Date based on experience
    hire_year = 2023 - random.randint(0, min(exp_years, 10))
    hire_date = fake.date_between_dates(
        date_start=datetime(hire_year, 1, 1),
        date_end=datetime(2023, 1, 1),
    )

    status = random.choices(
        ["Active", "Terminated", "On Leave"],
        weights=[0.88, 0.08, 0.04],
    )[0]

    employees.append(
        {
            "Employee_ID": emp_id,
            "Employee_Name": name,
            "Gender": gender,
            "Age": age,
            "Department": dept,
            "Job_Role": role,
            "Location": location,
            "Experience_Years": exp_years,
            "Hire_Date": hire_date,
            "Employment_Status": status,
        }
    )

df_employees = pd.DataFrame(employees)

# --- 2 & 3. PERFORMANCE & LABOR COST DATASETS (6,000 Rows each) ---
performance_records = []
labor_records = []

for _, emp in df_employees.iterrows():
    emp_id = emp["Employee_ID"]
    dept = emp["Department"]
    base_sal = BASE_SALARIES[dept] + (emp["Experience_Years"] * 1500)

    for month in MONTHS:
        # Performance Dataset Logic
        tasks = random.randint(20, 80)

        # Only Sales dept generates direct sales revenue
        if dept == "Sales":
            sales = round(random.uniform(200000, 1200000), 2)
        else:
            sales = 0.00

        accuracy = round(random.uniform(82.0, 99.8), 2)
        attendance = round(random.uniform(85.0, 100.0), 1)
        prod_hours = round(random.uniform(120.0, 185.0), 1)

        # Weighted performance score calculation
        perf_score = round(
            min(
                100,
                (tasks / 80 * 30)
                + ((accuracy - 80) / 20 * 35)
                + ((attendance - 85) / 15 * 35),
            ),
            2,
        )

        performance_records.append(
            {
                "Employee_ID": emp_id,
                "Month": month,
                "Tasks_Completed": tasks,
                "Sales_Revenue": sales,
                "Accuracy_Percent": accuracy,
                "Attendance_Percent": attendance,
                "Productivity_Hours": prod_hours,
                "Performance_Score": perf_score,
            }
        )

        # Labor Cost Dataset Logic
        ot_hours = random.choices(
            [0, random.randint(4, 30)], weights=[0.6, 0.4]
        )[0]
        hourly_rate = base_sal / 160
        ot_cost = round(ot_hours * (hourly_rate * 1.5), 2)

        train_hours = random.choices(
            [0, random.randint(2, 16)], weights=[0.7, 0.3]
        )[0]
        train_cost = round(train_hours * 650.0, 2)

        labor_records.append(
            {
                "Employee_ID": emp_id,
                "Month": month,
                "Base_Salary": round(base_sal, 2),
                "Overtime_Hours": ot_hours,
                "Overtime_Cost": ot_cost,
                "Training_Hours": train_hours,
                "Training_Cost": train_cost,
            }
        )

df_performance = pd.DataFrame(performance_records)
df_labor_cost = pd.DataFrame(labor_records)

# --- CSV SAVE ---
df_employees.to_csv("employees.csv", index=False)
df_performance.to_csv("employee_performance.csv", index=False)
df_labor_cost.to_csv("labor_cost.csv", index=False)

print("Files generated successfully!")
print(f"1. employees.csv -> {len(df_employees)} rows")
print(f"2. employee_performance.csv -> {len(df_performance)} rows")
print(f"3. labor_cost.csv -> {len(df_labor_cost)} rows")
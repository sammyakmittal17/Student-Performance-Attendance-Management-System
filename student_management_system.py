import pandas as pd

STUDENTS_FILE = "students.csv"
MARKS_FILE = "marks.csv"
ATTENDANCE_FILE = "attendance.csv"

SUBJECTS = ["Maths", "Physics", "Programming", "English", "Chemistry"]
GRADE_BOUNDARIES = ((90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (0, "F"))


def get_int(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(prompt))
            if min_val is not None and max_val is not None:
                if val < min_val or val > max_val:
                    print(f"Please enter a number between {min_val} and {max_val}.")
                    continue
            elif min_val is not None and val < min_val:
                print(f"Please enter a number >= {min_val}.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter a whole number.")


def get_float(prompt, min_val=None, max_val=None):
    while True:
        try:
            val = float(input(prompt))
            if min_val is not None and max_val is not None:
                if val < min_val or val > max_val:
                    print(f"Value must be between {min_val} and {max_val}.")
                    continue
            return val
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def load_csv(filename, columns):
    try:
        df = pd.read_csv(filename)
        if df.empty:
            return pd.DataFrame(columns=columns)
        return df
    except FileNotFoundError:
        return pd.DataFrame(columns=columns)
    except pd.errors.EmptyDataError:
        print(f"{filename} is empty")
        return pd.DataFrame(columns=columns)


def load_data():
    students_df = load_csv(STUDENTS_FILE, ["Roll", "Name", "Course"])
    marks_df = load_csv(MARKS_FILE, ["Roll"] + SUBJECTS)
    attendance_df = load_csv(ATTENDANCE_FILE, ["Roll", "Subject", "Held", "Attended"])
    return students_df, marks_df, attendance_df


def save_data(students_df, marks_df, attendance_df):
    students_df.to_csv(STUDENTS_FILE, index=False)
    marks_df.to_csv(MARKS_FILE, index=False)
    attendance_df.to_csv(ATTENDANCE_FILE, index=False)


def add_student(students_df):
    existing_rolls = set(students_df["Roll"].astype(int).tolist()) if not students_df.empty else set()
    roll = get_int("Roll number: ", min_val=1)
    if roll in existing_rolls:
        print("A student with this roll number already exists.")
        return students_df
    name = input("Name: ").strip()
    course = input("Course: ").strip()
    new_student = {"Roll": roll, "Name": name, "Course": course}
    students_df = pd.concat([students_df, pd.DataFrame([new_student])], ignore_index=True)
    print(f"Student {name} added.")
    return students_df


def view_students(students_df):
    if students_df.empty:
        print("No student records found.")
        return
    print(f"{'Roll':<6} {'Name':<18} {'Course':<10}")
    for _, row in students_df.iterrows():
        print(f"{int(row['Roll']):<6} {row['Name']:<18} {row['Course']:<10}")


def update_student(students_df):
    roll = get_int("Enter roll number to update: ", min_val=1)
    if students_df.empty or roll not in students_df["Roll"].astype(int).values:
        print("No student with that roll number.")
        return students_df
    name = input("New name: ").strip()
    course = input("New course: ").strip()
    idx = students_df["Roll"].astype(int) == roll
    students_df.loc[idx, "Name"] = name
    students_df.loc[idx, "Course"] = course
    print("Student record updated.")
    return students_df


def delete_student(students_df, marks_df, attendance_df):
    roll = get_int("Enter roll number to delete: ", min_val=1)
    if students_df.empty or roll not in students_df["Roll"].astype(int).values:
        print("No student with that roll number.")
        return students_df, marks_df, attendance_df
    students_df = students_df[students_df["Roll"].astype(int) != roll].reset_index(drop=True)
    if not marks_df.empty:
        marks_df = marks_df[marks_df["Roll"].astype(int) != roll].reset_index(drop=True)
    if not attendance_df.empty:
        attendance_df = attendance_df[attendance_df["Roll"].astype(int) != roll].reset_index(drop=True)
    print("Student record deleted.")
    return students_df, marks_df, attendance_df


def search_student(students_df):
    roll = get_int("Enter roll number to search: ", min_val=1)
    if students_df.empty or roll not in students_df["Roll"].astype(int).values:
        print("No student with that roll number.")
        return
    row = students_df[students_df["Roll"].astype(int) == roll].iloc[0]
    print(f"Found: Roll {int(row['Roll'])} | {row['Name']} | {row['Course']}")


def student_records_menu(students_df, marks_df, attendance_df):
    while True:
        print("\n-- Student Records --")
        print("1. Add  2. View all  3. Update  4. Delete  5. Search  6. Back")
        choice = get_int("Choice: ", 1, 6)
        if choice == 1:
            students_df = add_student(students_df)
        elif choice == 2:
            view_students(students_df)
        elif choice == 3:
            students_df = update_student(students_df)
        elif choice == 4:
            students_df, marks_df, attendance_df = delete_student(students_df, marks_df, attendance_df)
        elif choice == 5:
            search_student(students_df)
        else:
            break
    return students_df, marks_df, attendance_df


def enter_marks(students_df, marks_df):
    roll = get_int("Enter roll number: ", min_val=1)
    if students_df.empty or roll not in students_df["Roll"].astype(int).values:
        print("No student with that roll number.")
        return marks_df
    record = {"Roll": roll}
    for sub in SUBJECTS:
        record[sub] = get_float(f"Marks in {sub} (0-100): ", 0, 100)
    if not marks_df.empty and roll in marks_df["Roll"].astype(int).values:
        marks_df = marks_df[marks_df["Roll"].astype(int) != roll]
    marks_df = pd.concat([marks_df, pd.DataFrame([record])], ignore_index=True)
    print("Marks saved.")
    return marks_df


def record_attendance(students_df, attendance_df):
    roll = get_int("Enter roll number: ", min_val=1)
    if students_df.empty or roll not in students_df["Roll"].astype(int).values:
        print("No student with that roll number.")
        return attendance_df
    for i, sub in enumerate(SUBJECTS, start=1):
        print(f"{i}. {sub}")
    sub_idx = get_int("Choose subject: ", 1, len(SUBJECTS))
    subject = SUBJECTS[sub_idx - 1]
    held = get_int("Classes held: ", min_val=1)
    attended = get_int("Classes attended: ", 0, held)
    pct = (attended / held) * 100
    print(f"Attendance for {subject}: {pct:.1f}%")
    if pct < 75:
        print("ALERT: below 75% attendance!")
    if not attendance_df.empty:
        mask = (attendance_df["Roll"].astype(int) == roll) & (attendance_df["Subject"] == subject)
        attendance_df = attendance_df[~mask]
    new_row = {"Roll": roll, "Subject": subject, "Held": held, "Attended": attended}
    attendance_df = pd.concat([attendance_df, pd.DataFrame([new_row])], ignore_index=True)
    return attendance_df


def calculate_grade(percentage):
    for boundary, grade in GRADE_BOUNDARIES:
        if percentage >= boundary:
            return grade
    return "F"


def compute_results(students_df, marks_df):
    if students_df.empty or marks_df.empty:
        return pd.DataFrame()
    merged = pd.merge(students_df, marks_df, on="Roll", how="inner")
    if merged.empty:
        return merged
    merged["Total"] = merged[SUBJECTS].sum(axis=1)
    merged["Average"] = merged[SUBJECTS].mean(axis=1)
    merged["Percentage"] = (merged["Total"] / (len(SUBJECTS) * 100)) * 100
    merged["Grade"] = merged["Percentage"].apply(calculate_grade)
    return merged


def performance_analysis(students_df, marks_df):
    results = compute_results(students_df, marks_df)
    if results.empty:
        print("No marks data available for analysis.")
        return
    print("\nClass average per subject:")
    subject_avgs = results[SUBJECTS].mean()
    for sub, avg in subject_avgs.items():
        print(f"{sub:<14} {avg:.2f}")
    weak_sub = subject_avgs.idxmin()
    print(f"\nWeak subject : {weak_sub} ({subject_avgs[weak_sub]:.2f})")
    ranked = results.sort_values(by="Percentage", ascending=False).reset_index(drop=True)
    topper = ranked.iloc[0]
    lowest = ranked.iloc[-1]
    print(f"Topper       : {topper['Name']} (Roll {int(topper['Roll'])}) - {topper['Percentage']:.1f}% [{topper['Grade']}]")
    print(f"Lowest       : {lowest['Name']} (Roll {int(lowest['Roll'])}) - {lowest['Percentage']:.1f}% [{lowest['Grade']}]")
    print("\nAll students (ranked):")
    print(f"{'Roll':<6} {'Name':<16} {'Total':>6} {'Average':>8} {'Percentage':>11} {'Grade':>6}")
    for _, r in ranked.iterrows():
        print(f"{int(r['Roll']):<6} {r['Name']:<16} {r['Total']:>6.1f} {r['Average']:>8.1f} {r['Percentage']:>10.1f}% {r['Grade']:>6}")


def attendance_report(students_df, attendance_df):
    if students_df.empty or attendance_df.empty:
        return pd.DataFrame()
    grouped = attendance_df.groupby("Roll", as_index=False)[["Held", "Attended"]].sum()
    grouped["Attendance %"] = (grouped["Attended"] / grouped["Held"]) * 100
    return pd.merge(students_df, grouped, on="Roll", how="inner")


def student_report(students_df, marks_df, attendance_df):
    roll = get_int("Enter roll number: ", min_val=1)
    results = compute_results(students_df, marks_df)
    if results.empty or roll not in results["Roll"].astype(int).values:
        print("No marks record found for this student.")
        return
    row = results[results["Roll"].astype(int) == roll].iloc[0]
    print(f"\n===== Report: {row['Name']} (Roll {int(row['Roll'])}) =====")
    for sub in SUBJECTS:
        print(f"{sub:<13}: {row[sub]:.1f}")
    print(f"{'Total':<13}: {row['Total']:.1f}")
    print(f"{'Average':<13}: {row['Average']:.1f}")
    print(f"{'Percentage':<13}: {row['Percentage']:.1f}%  Grade: {row['Grade']}")
    att = attendance_report(students_df, attendance_df)
    if not att.empty and roll in att["Roll"].astype(int).values:
        att_pct = att[att["Roll"].astype(int) == roll].iloc[0]["Attendance %"]
        flag = "  <-- BELOW 75%" if att_pct < 75 else ""
        print(f"{'Attendance':<13}: {att_pct:.1f}%{flag}")


def class_report(students_df, marks_df):
    performance_analysis(students_df, marks_df)


def low_attendance_list(students_df, attendance_df):
    att = attendance_report(students_df, attendance_df)
    if att.empty:
        print("No attendance records found.")
        return
    low = att[att["Attendance %"] < 75]
    print("\n===== Students below 75% attendance =====")
    if low.empty:
        print("No students below 75% attendance.")
        return
    print(f"{'Roll':<6} {'Name':<16} {'Held':>6} {'Attended':>9} {'Attendance %':>13}")
    for _, r in low.iterrows():
        print(f"{int(r['Roll']):<6} {r['Name']:<16} {int(r['Held']):>6} {int(r['Attended']):>9} {r['Attendance %']:>12.1f}")


def report_menu(students_df, marks_df, attendance_df):
    print("\n-- Report Generation --")
    print("1. Student Report  2. Class Report  3. Low-Attendance List")
    choice = get_int("Choice: ", 1, 3)
    if choice == 1:
        student_report(students_df, marks_df, attendance_df)
    elif choice == 2:
        class_report(students_df, marks_df)
    else:
        low_attendance_list(students_df, attendance_df)


def main():
    students_df, marks_df, attendance_df = load_data()
    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Student Records")
        print("2. Marks Entry")
        print("3. Attendance Tracking")
        print("4. Performance Analysis")
        print("5. Report Generation")
        print("6. Exit")
        choice = get_int("Enter choice: ", 1, 6)
        if choice == 1:
            students_df, marks_df, attendance_df = student_records_menu(students_df, marks_df, attendance_df)
        elif choice == 2:
            marks_df = enter_marks(students_df, marks_df)
        elif choice == 3:
            attendance_df = record_attendance(students_df, attendance_df)
        elif choice == 4:
            performance_analysis(students_df, marks_df)
        elif choice == 5:
            report_menu(students_df, marks_df, attendance_df)
        else:
            save_data(students_df, marks_df, attendance_df)
            print("Data saved. Exiting...")
            break
        save_data(students_df, marks_df, attendance_df)


if __name__ == "__main__":
    main()

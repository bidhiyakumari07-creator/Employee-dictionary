from flask import Flask, render_template, request, redirect
from openpyxl import load_workbook
from datetime import datetime

app = Flask(__name__)

EXCEL_FILE = "employees.xlsx"


def load_employees():
    workbook = load_workbook(EXCEL_FILE)
    sheet = workbook.active

    employees = {}

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row[0]:
            employees[str(row[0])] = (
                row[1],
                row[2],
                row[3],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8]
            )

    return employees


def save_employees(employees):
    workbook = load_workbook(EXCEL_FILE)
    sheet = workbook.active

    sheet.delete_rows(2, sheet.max_row)

    for emp_id, data in employees.items():
        sheet.append([emp_id] + list(data))

    workbook.save(EXCEL_FILE)

def get_upcoming_events(employees):
    today = datetime.today().date()

    birthdays = []
    anniversaries = []

    for emp_id, data in employees.items():

        name = data[0]
        birthdate = data[3]
        joining_date = data[6]

        try:
            birthday = datetime.strptime(str(birthdate), "%Y-%m-%d").date()
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year >= today:
                days = (birthday_this_year - today).days

                if days <= 30:
                    birthdays.append((name, birthday_this_year, days))

        except:
            pass

        try:
            joining = datetime.strptime(str(joining_date), "%Y-%m-%d").date()
            anniversary_this_year = joining.replace(year=today.year)

            if anniversary_this_year >= today:
                days = (anniversary_this_year - today).days

                if days <= 30:
                    anniversaries.append((name, anniversary_this_year, days))

        except:
            pass

    return birthdays, anniversaries

@app.route("/")
def home():
    employees = load_employees()

    birthdays, anniversaries = get_upcoming_events(employees)

    return render_template(
        "index.html",
        employees=employees,
        birthdays=birthdays,
        anniversaries=anniversaries
    )


@app.route("/add", methods=["POST"])
def add_employee():

    employees = load_employees()

    emp_id = request.form["emp_id"]

    if emp_id in employees:
        return "Employee ID already exists!"

    employees[emp_id] = (
        request.form["name"],
        request.form["email"],
        request.form["phone"],
        request.form["birthdate"],
        request.form["gender"],
        request.form["job_role"],
        request.form["joining_date"],
        request.form["status"]
    )

    save_employees(employees)

    return redirect("/")


@app.route("/delete/<emp_id>")
def delete_employee(emp_id):

    employees = load_employees()

    if emp_id in employees:
        employees.pop(emp_id)

    save_employees(employees)

    return redirect("/")


@app.route("/update/<emp_id>", methods=["GET", "POST"])
def update_employee(emp_id):

    employees = load_employees()

    if request.method == "POST":

        employees[emp_id] = (
            request.form["name"],
            request.form["email"],
            request.form["phone"],
            request.form["birthdate"],
            request.form["gender"],
            request.form["job_role"],
            request.form["joining_date"],
            request.form["status"]
        )

        save_employees(employees)

        return redirect("/")

    return render_template(
        "edit_employee.html",
        emp_id=emp_id,
        data=employees[emp_id]
    )


@app.route("/search")
def search_employee():

    emp_id = request.args.get("emp_id")

    employees = load_employees()

    if emp_id in employees:
        employee = {emp_id: employees[emp_id]}
    else:
        employee = {}

    return render_template("index.html", employees=employee)

@app.route("/employee/<emp_id>")
def employee_profile(emp_id):

    employees = load_employees()

    if emp_id not in employees:
        return "Employee not found!"

    return render_template(
        "employee_profile.html",
        emp_id=emp_id,
        data=employees[emp_id]
    )

if __name__ == "__main__":
    app.run(debug=True)
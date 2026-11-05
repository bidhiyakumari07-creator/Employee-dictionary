
import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect
from sqlalchemy import create_engine, text

app = Flask(__name__)

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create table automatically
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            emp_id TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            phone TEXT,
            birthdate TEXT,
            gender TEXT,
            job_role TEXT,
            joining_date TEXT,
            status TEXT
        )
    """))


def load_employees():
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT * FROM employees")).mappings().all()

    return {
        row["emp_id"]: (
            row["name"], row["email"], row["phone"],
            row["birthdate"], row["gender"], row["job_role"],
            row["joining_date"], row["status"]
        )
        for row in rows
    }


def get_upcoming_events(employees):
    today = date.today()
    birthdays = []
    anniversaries = []

    for emp_id, data in employees.items():
        for index, events in [(3, birthdays), (6, anniversaries)]:
            try:
                event_date = datetime.strptime(
                    str(data[index]), "%Y-%m-%d"
                ).date()

                try:
                    upcoming = event_date.replace(year=today.year)
                except ValueError:
                    upcoming = date(today.year, 2, 28)

                if upcoming < today:
                    try:
                        upcoming = event_date.replace(year=today.year + 1)
                    except ValueError:
                        upcoming = date(today.year + 1, 2, 28)

                days = (upcoming - today).days

                if days <= 30:
                    events.append((data[0], upcoming, days))
            except (ValueError, TypeError):
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
    data = {
        key: request.form[key]
        for key in [
            "emp_id", "name", "email", "phone",
            "birthdate", "gender", "job_role",
            "joining_date", "status"
        ]
    }

    if data["emp_id"] in load_employees():
        return "Employee ID already exists!", 409

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO employees VALUES (
                :emp_id, :name, :email, :phone,
                :birthdate, :gender, :job_role,
                :joining_date, :status
            )
        """), data)

    return redirect("/")


@app.route("/delete/<emp_id>", methods=["POST"])
def delete_employee(emp_id):
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM employees WHERE emp_id = :id"),
            {"id": emp_id}
        )

    return redirect("/")


@app.route("/update/<emp_id>", methods=["GET", "POST"])
def update_employee(emp_id):
    employees = load_employees()

    if emp_id not in employees:
        return "Employee not found!", 404

    if request.method == "POST":
        data = {
            key: request.form[key]
            for key in [
                "name", "email", "phone", "birthdate",
                "gender", "job_role", "joining_date", "status"
            ]
        }
        data["emp_id"] = emp_id

        with engine.begin() as conn:
            conn.execute(text("""
                UPDATE employees SET
                    name=:name,
                    email=:email,
                    phone=:phone,
                    birthdate=:birthdate,
                    gender=:gender,
                    job_role=:job_role,
                    joining_date=:joining_date,
                    status=:status
                WHERE emp_id=:emp_id
            """), data)

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

    result = {emp_id: employees[emp_id]} if emp_id in employees else {}

    return render_template("index.html", employees=result)


@app.route("/employee/<emp_id>")
def employee_profile(emp_id):
    employees = load_employees()

    if emp_id not in employees:
        return "Employee not found!", 404

    return render_template(
        "employee_profile.html",
        emp_id=emp_id,
        data=employees[emp_id]
    )


if __name__ == "__main__":
    app.run(debug=True)

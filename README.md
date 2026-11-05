# Employee Directory Manager

A simple web-based **Employee Directory Management System** built with **Python, Flask, HTML, CSS, and Excel**. It helps users maintain employee records through an easy-to-use interface.

## Features

- **Add employees** with details such as name, email, phone number, birthdate, gender, job role, joining date, and employment status.
- **View employee records** on the main directory page.
- **Search employees** by Employee ID.
- **Update employee information** using an edit form.
- **Delete employee records** from the directory.
- **View individual employee profiles**.
- **See upcoming birthdays and work anniversaries** within the next 30 days.
- **Store employee data in an Excel workbook** (`employees.xlsx`) using `openpyxl`.
- **Prevent duplicate Employee IDs** when adding new employees.

## Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Backend logic |
| Flask | Web framework and routing |
| HTML | Web page structure |
| CSS | Styling |
| Jinja2 | Rendering dynamic templates |
| openpyxl | Reading and writing Excel records |
| Microsoft Excel (`.xlsx`) | Employee data storage |

## Project Structure

```text
Employee-Directory-Manager/
├── app.py
├── employees.xlsx
├── employees.json
├── static/
│   └── style.css
├── templates/
│   ├── add_employee.html
│   ├── edit_employee.html
│   ├── employee_profile.html
│   └── index.html
└── README.md
```

> **Note:** The current application reads and writes employee data in `employees.xlsx`. The included `employees.json` file is not used by the current version of `app.py`.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Employee-Directory-Manager.git
cd Employee-Directory-Manager
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install Flask openpyxl
```

### 4. Run the application

Make sure `employees.xlsx` is present in the project directory, then run:

```bash
python app.py
```

### 5. Open the application

Visit **http://127.0.0.1:5000/** in your browser.

## How to Use

1. **Add:** Enter an Employee ID and the employee's details in the add form.
2. **View:** Browse the employee directory on the home page.
3. **Search:** Enter an Employee ID to find a specific record.
4. **Edit:** Open an employee's edit page to update their information.
5. **Delete:** Remove an employee record when it is no longer needed.
6. **Profile:** Open an employee's profile page to see their details.
7. **Upcoming events:** Check the home page for birthdays and work anniversaries occurring within 30 days.

## Data Fields

Each employee record includes:

- Employee ID
- Name
- Email
- Phone Number
- Birthdate
- Gender
- Job Role
- Joining Date
- Employment Status

## Future Improvements

- User authentication and role-based access
- More advanced search and filtering
- Dashboard analytics and charts
- CSV/Excel export options
- Database integration (SQLite or PostgreSQL)
- Improved validation and error handling

## Important Notes

- This is a **learning/portfolio project** and runs locally with Flask's development server.
- The application starts with `debug=True`, which should be disabled before production deployment.
- The current delete action is accessed via a URL. A production version should use a protected POST request, authentication, and appropriate security controls.
- **Do not upload real employees' personal information to a public GitHub repository.** Replace any personal data in `employees.xlsx` and `employees.json` with fictional sample records before publishing.

## Author

Bidhya Kumari  



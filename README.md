Mariam Ahmed Mohamed-2304242-did everything

# Database Lab 2 — Login and Personal To-Do List

## 1. Project Overview

This project is a web-based application that allows users to register, log in securely, and manage their personal to-do lists. Users can create, view, edit, complete, and delete their tasks. Each user can access only their own tasks.

## 2. Technologies Used

- **Back End:** Python with Flask
- **Front End:** HTML, CSS, and JavaScript
- **Database:** MySQL
- **Database Management Tool:** MySQL Workbench
- **Version Control:** Git and GitHub
- **Password Security:** bcrypt password hashing

## 3. How to Run the Project from Scratch

Follow these steps to set up and run the application on a new computer.

### Step 1: Install the Required Software

Install the following programs:

- Python
- MySQL Server
- MySQL Workbench
- Git

A code editor, such as Visual Studio Code, is recommended.

### Step 2: Download the Project

Clone the GitHub repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Navigate to the project folder:

```bash
cd db-lab2
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the actual repository URL.

### Step 3: Create and Activate a Virtual Environment

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### Step 4: Install the Python Dependencies

Run:

```bash
pip install -r requirements.txt
```

### Step 5: Set Up the Database

1. Open MySQL Workbench.
2. Connect to the local MySQL Server.
3. Open `database/schema.sql`.
4. Execute the SQL script.
5. Confirm that the database named `registration` and its `users` and `todos` tables have been created.

### Step 6: Configure Environment Variables

Copy `.env.example` to a new file named `.env` in the project root directory.

On Windows Command Prompt, you can use:

```bash
copy .env.example .env
```

Open `.env` and enter the correct MySQL connection settings and a unique session secret.

Do not upload the `.env` file or real credentials to GitHub.

### Step 7: Start the Application

Run the Flask application:

```bash
python app.py
```

### Step 8: Open the Application

Open your browser and visit:

```text
http://127.0.0.1:5000
```

The application should now be available locally.

## 4. Implemented Features (R1–R10)

The application is designed to provide the following features:

- **R1 — User Registration:** Users can create accounts using their name, email, and password.
- **R2 — Input Validation:** Required fields are validated, and invalid or empty inputs are rejected.
- **R3 — Duplicate Email Prevention:** Each email address must be unique. Duplicate registration attempts display `Email Already Exists`.
- **R4 — Secure Login:** Users authenticate using their email and password. Invalid credentials display `Invalid email or password`.
- **R5 — Session Management:** Login sessions are maintained, and users can log out securely.
- **R6 — Personal To-Do List:** Authenticated users can view their own tasks, ordered from newest to oldest.
- **R7 — Add Tasks:** Users can create new tasks with valid titles.
- **R8 — Edit Tasks:** Users can update their task titles.
- **R9 — Complete and Delete Tasks:** Users can mark tasks as completed or incomplete and delete tasks.
- **R10 — Security and Ownership:** Parameterized SQL queries, password hashing, and user ownership checks help protect user data.


## 5. Database Structure

The application uses two tables.

### Users Table

Stores registered users and their account information.

- `user_id`: Primary key and automatically generated user identifier.
- `email`: Unique email address.
- `name`: User's name.
- `password_hash`: Hashed password.
- `registration_date`: Date and time of registration.

### Todos Table

Stores the tasks belonging to registered users.

- `todo_id`: Primary key and automatically generated task identifier.
- `user_id`: Foreign key referencing the `users` table.
- `title`: Task description.
- `is_done`: Indicates whether the task is completed.
- `created_at`: Date and time the task was created.

The foreign key establishes a relationship between users and their tasks.

## 6. Database and Security Questions

### (a) Why do UPDATE and DELETE contain `AND user_id = ?`, and what changes if you remove it?

The condition `AND user_id = ?` ensures that a user can update or delete only tasks that belong to their own account. The task ID identifies the task, while the user ID verifies its ownership.

If this condition is removed, the application may allow a user to modify or delete another user's task by providing its task ID. This creates a security vulnerability known as an authorization or access-control failure.

### (b) What happens if you insert a to-do for a user_id that does not exist, and which constraint is responsible?

The insertion fails because the specified `user_id` does not reference an existing record in the `users` table. The **foreign key constraint** prevents the database from storing a task associated with a nonexistent user. This maintains referential integrity.

### (c) Why do you store a hash and not the password?

Passwords should not be stored as plain text because anyone who gains access to the database could read them directly. Instead, the application stores a password hash generated using a suitable password-hashing algorithm such as bcrypt.

During login, the submitted password is verified against the stored hash. The original password is not stored in the database. This reduces the risk of exposing users' actual passwords if the database is compromised.

### (d) The name column is NOT NULL. Why is an additional check needed for an empty name?

The `NOT NULL` constraint prevents a database column from containing SQL `NULL`, but it does not prevent an empty string or a string containing only spaces.

For example, `''` and `'   '` are not SQL `NULL` values. Therefore, the application must validate the name before inserting it into the database, for example by trimming whitespace and rejecting the value if nothing remains.

This provides stronger input validation and ensures that every registered user has a meaningful name.

## 7. Screenshots

1- <img width="583" height="820" alt="Image 2026-10-12 at 4 00 55 PM" src="https://github.com/user-attachments/assets/7fd60849-9a9f-4590-b900-d3e386a00182" />
2- <img width="3840" height="2160" alt="Screenshot (7)" src="https://github.com/user-attachments/assets/f2691ca7-84b3-4e68-80f4-1f80adacbcb4" />
3- <img width="3840" height="2160" alt="Screenshot (8)" src="https://github.com/user-attachments/assets/c749885d-fcae-44f9-90ab-bcb65e037985" />
4- <img width="3840" height="2160" alt="Screenshot (9)" src="https://github.com/user-attachments/assets/af9ed506-e5e1-4aad-9f71-8bf4d506931c" />
5-<img width="3840" height="2160" alt="Screenshot (18)" src="https://github.com/user-attachments/assets/b5885ae2-bbd0-4054-aad4-56f562f586f5" />
6-<img width="417" height="703" alt="Image 2026-10-13 at 3 58 18 AM" src="https://github.com/user-attachments/assets/b78934bf-6831-4242-a0c6-e1c6b2514979" />

## 8. Conclusion

This project demonstrates the integration of a MySQL database with a web application, including user registration, authentication, session management, data validation, and personal task management. It also demonstrates the importance of database constraints, secure password storage, parameterized SQL queries, and authorization checks.






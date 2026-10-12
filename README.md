Login & To-Do Application

Project Description

This project is a web-based Login and To-Do application developed as part of the Database Systems Lab.

The application allows users to register, log in, and manage their personal tasks.

Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- Bootstrap

Features

- User Registration
- User Login and Logout
- Password Hashing using bcrypt
- Session-Based Authentication
- Add New Tasks
- Edit Existing Tasks
- Delete Tasks
- Mark Tasks as Done or Not Done
- Display the Number of Completed Tasks
- Display the Number of Incomplete Tasks

Requirements

- Flask
- PyMySQL
- bcrypt
- python-dotenv

Installation and Setup

1. Clone the Repository

git clone YOUR_REPOSITORY_URL
cd Login-Todo-App

2. Install Dependencies

pip install -r requirements.txt

3. Configure the Database

Create the required MySQL database and tables according to the project requirements.

Create a local ".env" file and configure the database connection settings.

4. Run the Application

python app.py

Open the local URL displayed in the terminal in your web browser.

Security

- Passwords are hashed using bcrypt.
- Database credentials and secret keys should be stored in a local ".env" file.
- The ".env" file must not be uploaded to GitHub.

Project Purpose

The purpose of this project is to apply database concepts and web application development using Python Flask and MySQL.
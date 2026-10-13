import os
import pymysql
import bcrypt
from flask import Flask, render_template, request, redirect, session, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


def get_db():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    errors = []
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        if not name:
            errors.append("Name is required")
        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")
        if not confirm:
            errors.append("Confirm password is required")
        if password and confirm and password != confirm:
            errors.append("Passwords do not match")

        if not errors:
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            conn = get_db()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO users (email, name, password_hash) VALUES (%s, %s, %s)",
                        (email, name, hashed),
                    )
                    conn.commit()
                    session["user_id"] = cur.lastrowid
                    session["name"] = name
                return redirect(url_for("todos"))
            except pymysql.err.IntegrityError as e:
                if e.args[0] == 1062:
                    errors.append("Email Already Exists")
                else:
                    raise
            finally:
                conn.close()

    return render_template("register.html", errors=errors)


@app.route("/login", methods=["GET", "POST"])
def login():
    errors = []
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email:
            errors.append("Email is required")
        if not password:
            errors.append("Password is required")

        if not errors:
            conn = get_db()
            try:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT user_id, name, password_hash FROM users WHERE email = %s",
                        (email,),
                    )
                    user = cur.fetchone()
            finally:
                conn.close()

            if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
                session["user_id"] = user["user_id"]
                session["name"] = user["name"]
                return redirect(url_for("todos"))
            errors.append("Invalid email or password")

    return render_template("login.html", errors=errors)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


def fetch_todos(user_id):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT todo_id, title, is_done, created_at FROM todos "
                "WHERE user_id = %s ORDER BY todo_id DESC",
                (user_id,),
            )
            return cur.fetchall()
    finally:
        conn.close()


def run_write(sql, params):
    conn = get_db()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
        conn.commit()
    finally:
        conn.close()


def title_error(title):
    if not title:
        return "Title is required"
    if len(title) > 200:
        return "Title is too long (200 characters at most)"
    return None


def show_todos(errors):
    items = fetch_todos(session["user_id"])
    done_count = sum(1 for t in items if t["is_done"])
    return render_template(
        "todos.html",
        todos=items,
        errors=errors,
        name=session["name"],
        open_count=len(items) - done_count,
        done_count=done_count,
    )


@app.route("/todos")
def todos():
    if "user_id" not in session:
        return redirect(url_for("login"))
    return show_todos([])


@app.route("/todos/add", methods=["POST"])
def add_todo():
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    err = title_error(title)
    if err:
        return show_todos([err])
    run_write(
        "INSERT INTO todos (user_id, title) VALUES (%s, %s)",
        (session["user_id"], title),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/edit", methods=["POST"])
def edit_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    title = request.form.get("title", "").strip()
    err = title_error(title)
    if err:
        return show_todos([err])
    run_write(
        "UPDATE todos SET title = %s WHERE todo_id = %s AND user_id = %s",
        (title, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/toggle", methods=["POST"])
def toggle_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    is_done = 1 if request.form.get("is_done") == "1" else 0
    run_write(
        "UPDATE todos SET is_done = %s WHERE todo_id = %s AND user_id = %s",
        (is_done, todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.route("/todos/<int:todo_id>/delete", methods=["POST"])
def delete_todo(todo_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    run_write(
        "DELETE FROM todos WHERE todo_id = %s AND user_id = %s",
        (todo_id, session["user_id"]),
    )
    return redirect(url_for("todos"))


@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", message="Page not found"), 404


@app.errorhandler(500)
def server_error(e):
    return render_template("error.html", message="Something went wrong. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=True)
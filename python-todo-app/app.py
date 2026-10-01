from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# DATABASE = "todo.db"
DATABASE = os.environ.get("DATABASE_PATH", "todo.db")


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def index():
    conn = get_db()
    todos = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()

    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task", "").strip()

    if task:
        conn = get_db()
        conn.execute(
            "INSERT INTO todos (task) VALUES (?)",
            (task,)
        )
        conn.commit()
        conn.close()

    return redirect("/")


@app.route("/toggle/<int:todo_id>", methods=["POST"])
def toggle(todo_id):
    conn = get_db()

    conn.execute("""
        UPDATE todos
        SET done = CASE WHEN done = 0 THEN 1 ELSE 0 END
        WHERE id = ?
    """, (todo_id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:todo_id>", methods=["POST"])
def delete(todo_id):
    conn = get_db()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    init_db()

    app.run(
        host="0.0.0.0",
        port=8009,
        debug=True
    )


from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = "todo.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            task TEXT NOT NULL, 
                            completed BOOLEAN NOT NULL DEFAULT 0)''')
        conn.commit()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    task = request.form.get("task")
    if task:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task, completed) VALUES (?, ?)", (task, 0))
        conn.commit()
        conn.close()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)

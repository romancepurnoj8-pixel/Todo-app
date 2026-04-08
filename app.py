from flask import Flask, render_template, request
import sqlite3
from datetime import date

app = Flask(__name__)

# 1. Создаем таблицу при запуске (один раз)
conn = sqlite3.connect("main.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        priority TEXT NOT NULL,
        task_type TEXT NOT NULL,
        dade TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
""")
conn.commit()
conn.close()

@app.route("/", methods=["POST", "GET"])
def index():
    conn = sqlite3.connect("main.db")
    conn.row_factory = sqlite3.Row
    message = ""

    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        todo_priority = request.form.get("todo_priority")
        todo_return = request.form.get("todo_return")
        todo_dade = request.form.get("todo_dade")

        if todo_name and todo_priority and todo_return and todo_dade:
            conn.execute("""
                INSERT INTO todo (name, priority, task_type, dade) 
                VALUES (?, ?, ?, ?)
            """, (todo_name, todo_priority, todo_return, todo_dade))
            conn.commit()
        else:
            message = "Заполни все поля!"


    tasks = conn.execute('SELECT * FROM todo').fetchall()
    
    conn.close()

    return render_template('index.html', tasks=tasks, message=message)

if __name__ == "__main__":
    app.run(debug=True)
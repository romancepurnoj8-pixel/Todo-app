import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from CalendarMatrix import MonthCalendar

app = Flask(__name__)
DATABASE = "main.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                priority TEXT NOT NULL,
                task_type TEXT NOT NULL,
                date TEXT NOT NULL,
                status INTEGER DEFAULT 0
            )
        """)
        conn.commit()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    
    selected_date = request.args.get('date') # Например: 2026-04-08
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if request.method == "POST":
        task_data = {
            "name": request.form.get("todo_name"),
            "priority": request.form.get("todo_priority"),
            "type": request.form.get("todo_return"),
            "date": request.form.get("todo_date")
        }

        if all(task_data.values()):
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO todo (name, priority, task_type, date)
                    VALUES (?, ?, ?, ?)
                """, (task_data["name"], task_data["priority"], 
                      task_data["type"], task_data["date"]))
                conn.commit()
            return redirect(url_for('index', date=task_data["date"]))
        
        message = "Пожалуйста, заполните все поля!"

    calendar_view = MonthCalendar(year, month)

    with get_db_connection() as conn:
        if selected_date:
            tasks = conn.execute(
                'SELECT * FROM todo WHERE date = ? ORDER BY id DESC', 
                (selected_date,)
            ).fetchall()
            display_title = f"Задачи на {selected_date}"
        else:
            tasks = conn.execute('SELECT * FROM todo ORDER BY date ASC, id DESC').fetchall()
            display_title = "Все задачи"

    return render_template(
        'index.html',
        cal=calendar_view,
        tasks=tasks,
        message=message,
        selected_date=selected_date,
        display_title=display_title
    )

if __name__ == "__main__":
    app.run(debug=True)
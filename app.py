from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from CalendarMatrix import MonthCalendar

app = Flask(__name__)

# Функция для инициализации БД (лучше вынести отдельно)
def init_db():
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

init_db()

@app.route("/", methods=["POST", "GET"])
def index():
    conn = sqlite3.connect("main.db")
    conn.row_factory = sqlite3.Row  # Чтобы обращаться к колонкам по именам
    message = ""

    # 1. ОБРАБОТКА POST (Добавление задачи)
    if request.method == "POST":
        todo_name = request.form.get("todo_name")
        todo_priority = request.form.get("todo_priority")
        todo_return = request.form.get("todo_return")
        todo_date = request.form.get("todo_date") # В HTML мы исправили на todo_date

        if todo_name and todo_priority and todo_return and todo_date:
            conn.execute("""
                INSERT INTO todo (name, priority, task_type, dade) 
                VALUES (?, ?, ?, ?)
            """, (todo_name, todo_priority, todo_return, todo_date))
            conn.commit()
            # После добавления лучше сделать редирект, чтобы не дублировать задачи при обновлении страницы
            conn.close()
            return redirect(url_for('index'))
        else:
            message = "Заполни все поля!"

    # 2. ПОДГОТОВКА ДАННЫХ ДЛЯ ОТОБРАЖЕНИЯ
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    cal_obj = MonthCalendar(year, month)

    # Получаем список всех задач
    tasks = conn.execute('SELECT * FROM todo ORDER BY id DESC').fetchall()
    
    conn.close()

    # 3. ЕДИНЫЙ RETURN (В самом конце!)
    return render_template('index.html', 
                           cal=cal_obj, 
                           tasks=tasks, 
                           message=message)

if __name__ == "__main__":
    app.run(debug=True)
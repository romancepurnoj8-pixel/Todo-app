from flask import Flask, render_template, request
import sqlite3

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
def new_todo():
    message = ""
    if request.method == "POST":
        # Получаем данные из формы
        todo_item = request.form.get("todo_name")
        todo_priority = request.form.get("todo_priority")
        todo_return = request.form.get("todo_return")
        todo_dade = request.form.get("todo_dade")

        if todo_item and todo_priority and todo_return:
            # Прямая запись в базу без обработчиков
            conn = sqlite3.connect("main.db")
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO todo (name, priority, task_type, dade) 
                VALUES (?, ?, ?, ?)
            """, (todo_item, todo_priority, todo_return, todo_dade))
            
            conn.commit()
            conn.close()
            
            message = f"Добавлено: {todo_item}"
        else:
            message = "Заполни все поля!"
        
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
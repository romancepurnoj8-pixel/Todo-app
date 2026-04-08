import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from CalendarMatrix import MonthCalendar

app = Flask(__name__)
app.secret_key = "super_secret_key_123" # Необходимо для работы сессий
DATABASE = "main.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                priority TEXT NOT NULL,
                task_type TEXT NOT NULL,
                date TEXT NOT NULL,
                status INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        conn.commit()

init_db()

# --- МАРШРУТЫ АВТОРИЗАЦИИ ---

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    
    if not username or not password:
        return redirect(url_for('auth_page'))

    try:
        with get_db_connection() as conn:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
        return redirect(url_for('auth_page')) # После регистрации отправляем на вход
    except sqlite3.IntegrityError:
        return "Пользователь уже существует", 400

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    with get_db_connection() as conn:
        user = conn.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                            (username, password)).fetchone()
        
    if user:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect(url_for('index'))
    
    return "Неверный логин или пароль", 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth_page'))

@app.route("/auth")
def auth_page():
    # Отображает ту самую страницу с формами, которую мы сделали раньше
    return render_template('auth.html')

# --- ОСНОВНОЙ ФУНКЦИОНАЛ ---

@app.route("/", methods=["GET", "POST"])
def index():
    # Если пользователь не вошел — отправляем на страницу авторизации
    if 'user_id' not in session:
        return redirect(url_for('auth_page'))

    selected_date = request.args.get('date')
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)

    if request.method == "POST":
        name = request.form.get("todo_name")
        priority = request.form.get("todo_priority")
        task_type = request.form.get("todo_return")
        date = request.form.get("todo_date")

        if all([name, priority, task_type, date]):
            with get_db_connection() as conn:
                conn.execute("""
                    INSERT INTO todo (user_id, name, priority, task_type, date)
                    VALUES (?, ?, ?, ?, ?)
                """, (session['user_id'], name, priority, task_type, date))
                conn.commit()
            return redirect(url_for('index', date=date))

    calendar_view = MonthCalendar(year, month)

    with get_db_connection() as conn:
        # Теперь выбираем задачи ТОЛЬКО текущего пользователя
        if selected_date:
            tasks = conn.execute(
                'SELECT * FROM todo WHERE user_id = ? AND date = ? ORDER BY id DESC', 
                (session['user_id'], selected_date)
            ).fetchall()
            display_title = f"Задачи на {selected_date}"
        else:
            tasks = conn.execute(
                'SELECT * FROM todo WHERE user_id = ? ORDER BY date ASC, id DESC',
                (session['user_id'],)
            ).fetchall()
            display_title = "Ваши задачи"

    return render_template(
        'index.html',
        cal=calendar_view,
        tasks=tasks,
        display_title=display_title,
        username=session['username']
    )

# ... маршрут update_status остается без изменений, 
# но желательно добавить в него проверку session['user_id']

if __name__ == "__main__":
    app.run(debug=True)
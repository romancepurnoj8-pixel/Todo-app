from flask import Flask, render_template, request
import sqlite3	


conn = sqlite3.connect("main.db")
app = Flask(__name__)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        priority TEXT NOT NULL,
        task_type TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )
""")
conn.commit()

@app.route("/", methods=["POST", "GET"])
def new_todo():
    message = ""
    if request.method == "POST":
        todo_item = request.form.get("todo_name")
        todo_priority = request.form.get("todo_priority")
        todo_return = request.form.get("todo_return")
        
        message = f"Added: {todo_item} ({todo_priority})"
        print(request.form)
        

        
    return render_template('index.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
conn.close()
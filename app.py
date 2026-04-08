from flask import Flask, render_template, request

app = Flask(__name__)

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
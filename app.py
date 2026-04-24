from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    duty_list = [f"Duty {i}" for i in range(1, 14)]
    return render_template('index.html', duties=duty_list)

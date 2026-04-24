from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    duty_list = [f"Duty {i}" for i in range(1, 14)]
    added_duties = []

    if request.method == "POST":
        added_duties = request.form.getlist("duties")


    return render_template('index.html', duties=duty_list, added_duties=added_duties)

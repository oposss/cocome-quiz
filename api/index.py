import os
from flask import Flask, render_template, request, send_from_directory

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__, template_folder="../templates", static_folder="../static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/result", methods=["POST"])
def result():
    score = sum(int(request.form.get(f"q{i}", 0)) for i in range(1, 9))

    if score <= 3:
        result_type = "cocome_fuwafuwa"
    elif score <= 5:
        result_type = "cocome_majime"
    elif score == 6:
        result_type = "cocome_tension"
    elif score == 7:
        result_type = "cocome_tsundere"
    else:
        result_type = "cocome_uranai"

    return render_template("result.html", result_type=result_type)

@app.route("/ramen")
def ramen():
    return send_from_directory(_ROOT, "ramen_story.html")

@app.route("/shufu")
def shufu():
    return send_from_directory(_ROOT, "shufu_story.html")

# Vercel entry point
handler = app

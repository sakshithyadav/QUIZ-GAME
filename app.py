import os
import secrets

from flask import Flask, redirect, render_template, request, session, url_for

from questions import QUESTIONS

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", secrets.token_hex(16))
QUIZ_DURATION_SECONDS = 15 * 60


@app.route("/")
def index():
    return render_template("index.html", total=len(QUESTIONS))


@app.route("/quiz")
def quiz():
    session["quiz_start"] = True
    session.pop("results", None)
    return render_template(
        "quiz.html",
        questions=QUESTIONS,
        duration_seconds=QUIZ_DURATION_SECONDS,
    )


@app.route("/submit", methods=["POST"])
def submit():
    if not session.get("quiz_start"):
        return redirect(url_for("index"))

    correct = 0
    wrong = 0
    unanswered = 0

    for index, question in enumerate(QUESTIONS):
        user_answer = request.form.get(f"q{index}", "").strip().upper()
        if not user_answer:
            unanswered += 1
        elif user_answer == question["answer"]:
            correct += 1
        else:
            wrong += 1

    total = len(QUESTIONS)
    session["results"] = {
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "total": total,
        "percentage": round((correct / total) * 100, 1) if total else 0,
    }
    session.pop("quiz_start", None)
    return redirect(url_for("results"))


@app.route("/results")
def results():
    data = session.get("results")
    if not data:
        return redirect(url_for("index"))
    return render_template("results.html", **data)


if __name__ == "__main__":
    app.run(debug=True)

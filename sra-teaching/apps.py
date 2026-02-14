from flask import Flask, render_template, request, redirect, url_for, session,send_from_directory

app = Flask(__name__)
app.secret_key = "secret123"


chapters_data = {
    "10": {
        "english": 10,
        "maths": 14,
        "science": 16,
        "hindi": 18,
        "punjabi": 10,
        "social": 22
    },
    "12": {
        "psychology": 7,
        "maths": 10,
        "english": 10,
        "punjabi": 10,
        "hindi": 18,
        "it": 5,
        "physical": 10
    }
}

# -----------------------------
# TEMP USER DATABASE (simple)
# -----------------------------
users = {}

# -----------------------------
# CLASSES & SUBJECTS
# -----------------------------
classes = {
    "10": ["Math", "Science"],
    "12": ["Psychology"]
}

# -----------------------------
# NOTES -> CHAPTERS -> PDFs
# -----------------------------
notes = {
    "10": {
        "Math": {
            "Chapter 1": "math10_ch1.pdf",
            "Chapter 2": "math10_ch2.pdf"
        },
        "Science": {
            "Chapter 1": "science10_ch1.pdf",
            "Chapter 2": "science10_ch2.pdf"
        }
    },
    "12": {
        "Psychology": {
            "Chapter 1": "psychology12_ch1.pdf",
            "Chapter 2": "psychology12_ch2.pdf",
            "Chapter 3": "psychology12_ch3.pdf",
            "Chapter 4": "psychology12_ch4.pdf",
            "Chapter 5": "psychology12_ch5.pdf"
        }
    }
}

# -----------------------------
# HOME
# -----------------------------
@app.route("/")
def index():
    return render_template("index.html")

# -----------------------------
# SIGNUP
# -----------------------------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        # read existing usersf
        with open("users.txt", "r") as f:
            users = f.readlines()

        for user in users:
            u, p = user.strip().split(",")
            if u == username:
                return "User already exists"

        # save new user
        with open("users.txt", "a") as f:
            f.write(username + "," + password + "\n")

        return redirect("/login")

    return render_template("signup.html")

# -----------------------------
# LOGIN
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        with open("users.txt", "r") as f:
            users = f.readlines()

        for user in users:
            u, p = user.strip().split(",")
            if u == username and p == password:
                session["user"] = username
                return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("/login"))
    return render_template("dashboard.html",
        classes=classes)

# -----------------------------
# NOTES PAGE
# -----------------------------
@app.route("/notes")
def notes_page():
    if "user" not in session:
        return redirect("/login")
    return render_template("notes.html", classes=classes)

# -----------------------------
# OPTIONS (CLASS -> SUBJECT)
# -----------------------------
@app.route("/options", methods=["POST"])
def options():
    if "user" not in session:
        return redirect("/login")

    c = request.form["class"]
    subjects = classes.get(c, [])
    return render_template("options.html", c=c, subjects=subjects)

# -----------------------------
# SHOW CHAPTERS
# -----------------------------
@app.route("/chapters", methods=["POST"])
def chapters():
    if "user" not in session:
        return redirect("/login")

    c = request.form["class"]
    subject = request.form["subject"]
    chapters = notes[c][subject]

    return render_template(
        "revision.html",
        c=c,
        subject=subject,
        chapters=chapters
    )

# -----------------------------
# OPEN PDF
# -----------------------------
@app.route("/pdf/<filename>")
def pdf(filename):
    if "user" not in session:
        return redirect("/login")
    return send_from_directory("static/pdfs", filename)

# -----------------------------
# LOGOUT
# -----------------------------
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("/login"))

@app.route("/class/<int:class_no>")
def select_subject(class_no):
 return render_template("options.html",class_no=class_no)

@app.route("/notes/<int:class_no>/<subject>")
def notes(class_no,subject):
    class_key=str(class_no)

    total_chapters=chapters_data.get(class_no,{}).get(subject,0)
    chapters=list(range(1,total_chapters+1))
    return render_template("notes.html",class_no=class_no,subject=subject,chapters=chapters)

@app.route("/subject/<int:class_no>/<subject>")
def subject_options(class_no, subject):
    return render_template(
        "options_subject.html",
        class_no=class_no,
        subject=subject
    )

@app.route("/test/<int:class_no>/<subject>")
def test(class_no, subject):

    tests = {
        10: {
            "english": [
                {
                    "question": "What is a noun?",
                    "a": "Name of a person/place/thing",
                    "b": "Action word",
                    "c": "Quality",
                    "d": "Feeling",
                    "answer": "a"
                }
            ],
            "hindi": [
                {
                    "question": "संज्ञा क्या है?",
                    "a": "नाम बताने वाला शब्द",
                    "b": "काम बताने वाला शब्द",
                    "c": "गुण बताने वाला शब्द",
                    "d": "भाव",
                    "answer": "a"
                }
            ],
            "punjabi": [
                {
                    "question": "ਸੰਗਿਆ ਕੀ ਹੈ?",
                    "a": "ਨਾਂ ਦਰਸਾਉਣ ਵਾਲਾ ਸ਼ਬਦ",
                    "b": "ਕਿਰਿਆ",
                    "c": "ਵਿਸ਼ੇਸ਼ਣ",
                    "d": "ਭਾਵ",
                    "answer": "a"
                }
            ]
        },

        12: {
            "english": [
                {
                    "question": "What is a phrase?",
                    "a": "Group of words",
                    "b": "Single word",
                    "c": "Sentence",
                    "d": "Verb",
                    "answer": "a"
                }
            ],
            "hindi": [
                {
                    "question": "समास क्या है?",
                    "a": "दो शब्दों का मेल",
                    "b": "एक शब्द",
                    "c": "वाक्य",
                    "d": "भाव",
                    "answer": "a"
                }
            ],
            "punjabi": [
                {
                    "question": "ਸਮਾਸ ਕੀ ਹੈ?",
                    "a": "ਦੋ ਸ਼ਬਦਾਂ ਦਾ ਜੋੜ",
                    "b": "ਇੱਕ ਸ਼ਬਦ",
                    "c": "ਵਾਕ",
                    "d": "ਭਾਵ",
                    "answer": "a"
                }
            ]
        }
    }

    questions = tests.get(class_no, {}).get(subject, [])

    return render_template(
        "test.html",
        class_no=class_no,
        subject=subject,
        questions=questions
    )

@app.route("/result/<int:class_no>/<subject>", methods=["POST"])
def result(class_no, subject):

    tests = {
        10: {
            "english": [
                {"answer": "a"},
                {"answer": "b"}
            ]
        },
        12: {
            "english": [
                {"answer": "a"}
            ]
        }
    }

    questions = tests.get(class_no, {}).get(subject, [])
    score = 0

    for i, q in enumerate(questions, start=1):
        user_answer = request.form.get(f"q{i}")
        if user_answer == q["answer"]:
            score += 1

    total = len(questions)

    return render_template(
        "result.html",
        score=score,
        total=total,
        class_no=class_no,
        subject=subject
    )
# -----------------------------
# RUN APP
# -----------------------------
if (__name__)

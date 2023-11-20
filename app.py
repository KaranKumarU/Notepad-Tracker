import subprocess
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save_note", methods=["POST"])
def save_note():
    note_text = request.form.get("note_text")

    # Save the note to a file
    with open("note.txt", "w") as file:
        file.write(note_text)

    # Commit changes to Git
    subprocess.run(["git", "add", "note.txt"])
    subprocess.run(["git", "commit", "-m", "Auto commit: Save note"])

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

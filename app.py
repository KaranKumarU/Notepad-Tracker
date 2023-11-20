from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_from_directory,
)
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ALLOWED_EXTENSIONS"] = {"txt", "md"}  # Specify allowed file extensions


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save_note", methods=["POST"])
def save_note():
    note_text = request.form.get("note_text")

    # Save the note to a file
    filename = secure_filename("note.txt")
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    with open(file_path, "w") as file:
        file.write(note_text)

    # Commit changes to Git
    subprocess.run(["git", "add", file_path])
    subprocess.run(["git", "commit", "-m", f"Auto commit: Save note ({filename})"])

    return redirect(url_for("index"))


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    app.run(debug=True)

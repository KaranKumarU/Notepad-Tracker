from flask import Flask, render_template, request, send_from_directory
import os
import subprocess

app = Flask(__name__)

UPLOADS_FOLDER = "uploads"
app.config["UPLOADS_FOLDER"] = UPLOADS_FOLDER


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/save_note", methods=["POST"])
def save_note():
    note_text = request.form.get("note_text")

    # Save the note to a file
    with open("note.txt", "w") as file:
        file.write(note_text)

    # Commit the changes to the Git repository
    subprocess.run(["git", "add", "note.txt"])
    subprocess.run(["git", "commit", "-m", "Update note"])

    # Handle file upload
    if "file" in request.files:
        uploaded_file = request.files["file"]
        if uploaded_file.filename != "":
            file_path = os.path.join(
                app.config["UPLOADS_FOLDER"], uploaded_file.filename
            )
            uploaded_file.save(file_path)

    return render_template("index.html", message="Note and file saved successfully.")


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOADS_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)

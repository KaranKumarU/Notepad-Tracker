from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "notes"

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


@app.route("/")
def index():
    notes = get_note_list()
    return render_template("index.html", notes=notes)


@app.route("/create", methods=["POST"])
def create_note():
    note_name = request.form["note_name"]
    note_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{note_name}.txt")

    with open(note_path, "w") as file:
        file.write("")

    return redirect(url_for("index"))


@app.route("/upload", methods=["POST"])
def upload_note():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], uploaded_file.filename)
        uploaded_file.save(file_path)

    return redirect(url_for("index"))


@app.route("/edit/<note_name>", methods=["GET", "POST"])
def edit_note(note_name):
    note_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{note_name}.txt")

    if request.method == "GET":
        with open(note_path, "r") as file:
            content = file.read()

        return render_template("edit.html", note_name=note_name, content=content)

    elif request.method == "POST":
        new_content = request.form["new_content"]
        with open(note_path, "w") as file:
            file.write(new_content)

        return redirect(url_for("index"))


def get_note_list():
    notes = []
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        if filename.endswith(".txt"):
            notes.append(os.path.splitext(filename)[0])
    return notes


if __name__ == "__main__":
    app.run(debug=True)

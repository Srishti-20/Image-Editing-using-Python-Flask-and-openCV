from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(filename, operation):
    print(f"The operation is {operation} and filename is {filename}")
    img = cv2.imread(os.path.join(UPLOAD_FOLDER, filename))

    if operation == "cgray":
        img_processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        new_filename = f"static/{filename}"
        cv2.imwrite(new_filename, img_processed)
        return new_filename

    elif operation in {"cwebp", "cjpg", "cpng"}:
        new_filename = f"static/{os.path.splitext(filename)[0]}.{operation[1:]}"
        cv2.imwrite(new_filename, img)
        return new_filename

    else:
        return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")
@app.route("/how")
def how():
    return render_template("how.html")
@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "POST":
        operation = request.form.get("operation")
        if 'file' not in request.files:
            flash('No file part')
            return "Error: No file part"

        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return "Error: No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = process_image(filename, operation)
            if new:
                flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            else:
                flash("Error: Invalid operation")
        else:
            flash("Error: File format not allowed")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)

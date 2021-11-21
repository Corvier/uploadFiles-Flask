import os

from flask import Flask, request, render_template, redirect, flash, send_from_directory
from werkzeug.utils import secure_filename # simplifica la codificacion de la imagen y nos devuleve el nombre del archivo

# UPLOAD_FOLDER = os.path.abspath('./static/imgDB/')
UPLOAD_FOLDER = './static/imgDB/'

app = Flask(__name__)
app.secret_key = "6HnUF1dhfjRwjQQnZc5LiLtfz25rvwhr"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.debug = True


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@app.route("/")
def index():
    return render_template("form.html")

# Función para verificar si el archivo tiene una extension permitida
def allowed_file(filename):
    # Devuelve True dependiedo las siguientes dos sentencias
        # 1 - El nombre del archivo tiene un punto
        # 2 - El nombre del archivo tiene una extension permitida segun la variable ALLOWED_EXTENSIONS
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           # rsplit es para dividir el nombre del archivo para poder recuperar la extension
              # rsplit('.', 1)[1] el primer parametro indica donde se va a dividir, el segundo parametro indica cuantas veces se va a dividir
              # [1] recuperamos la extension del archivo, ya que se dividio en dos y en la posicion 1 se encuentra la extension


# upload image
@app.route("/uploader", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        # Comprueba si la solicitud mediante POST tiene la parte del archivo
        if 'file' not in request.files:
            flash('The form has no file part', 'alert-danger')
            return redirect('/')

        file = request.files['file']
        # si el usuario no selecciona el archivo, el navegador también y enviar una parte vacía sin nombre de archivo
        if file.filename == '':
            flash('No selected file', 'alert-danger')
            return redirect('/')

        # Si existe el archivo y ademas el nombre del archivo tiene una extension de archivo permitida
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            dirFile = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            print(f"\n\n{dirFile}\n\n")

            flash('File uploaded successfully', 'alert-success')
            return redirect('/')

        else:
            flash('File extension not allowed', 'alert-warning')
            return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
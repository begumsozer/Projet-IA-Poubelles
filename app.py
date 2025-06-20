

from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Vérifie si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route principale : affiche le formulaire
@app.route('/')
def index():
    return render_template('index.html')

# Route de traitement de l'image
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return 'Aucun fichier envoyé'
    file = request.files['file']
    if file.filename == '':
        return 'Nom de fichier vide'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return render_template('index.html', image_url=url_for('static', filename='uploads/' + filename))
    return 'Fichier non autorisé'

if __name__ == '__main__':
    app.run(debug=True)
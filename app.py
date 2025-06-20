import os
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import numpy as np
from database import init_db

# Initialisation de Flask
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Création de la base si elle n'existe pas
init_db()

# Fonction pour extraire les métadonnées de l'image
def extract_metadata(filepath):
    img = Image.open(filepath)
    arr = np.array(img)
    red = int(np.mean(arr[:, :, 0]))
    green = int(np.mean(arr[:, :, 1]))
    blue = int(np.mean(arr[:, :, 2]))
    width, height = img.size
    file_size = os.path.getsize(filepath)
    return file_size, width, height, red, green, blue

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None

    if request.method == 'POST':
        file = request.files['image']
        annotation = request.form['annotation']

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Extraction des métadonnées
            file_size, width, height, r, g, b = extract_metadata(filepath)
            upload_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Enregistrement dans la base de données
            conn = sqlite3.connect('data.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO images 
                (file_path, upload_date, annotation, file_size, width, height, mean_red, mean_green, mean_blue)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (filepath, upload_date, annotation, file_size, width, height, r, g, b))
            conn.commit()
            conn.close()

            image_url = filepath

    # Affichage des images enregistrées
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM images ORDER BY id DESC')
    images = c.fetchall()
    conn.close()

    return render_template('index.html', image_url=image_url, images=images)

# Lancement de l'application
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

import os
from flask import Flask, request, flash, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS

from analyze_tiff import cutTIFF;

app = Flask(__name__, static_url_path='', static_folder='static')

UPLOAD_FOLDER = 'uploads'
CUT_FOLDER = 'uploads/cut'
ALLOWED_EXTENSIONS = {'tif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CUT_FOLDER'] = CUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CUT_FOLDER, exist_ok=True)

CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if not file or file.filename == '':
        flash('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    
    print(f"Uploaded file: {file.filename}")

    if not allowed_file(file.filename):
        return jsonify({'error': 'You selected wrong file dude.'}), 400
        
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/analyze', methods=['POST'])
def analyze_file():
    filename = request.get_json()['filename']
    cutTIFF(app.config['CUT_FOLDER'], filename)
    return jsonify({'message': 'File analyzed successfully'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
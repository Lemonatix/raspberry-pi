#!/usr/bin/env python3
"""
Simple file upload server for Raspberry Pi
Allows clients to upload files via HTTP POST requests
"""

from flask import Flask, request, jsonify, render_template_string
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 'zip'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SECRET_KEY'] = os.urandom(24)  # Generate random secret key for session security

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# HTML template for upload form
UPLOAD_FORM = """
<!DOCTYPE html>
<html>
<head>
    <title>Raspberry Pi File Upload Server</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        .upload-form {
            margin-top: 20px;
        }
        input[type="file"] {
            margin: 10px 0;
        }
        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #45a049;
        }
        .message {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
        }
        .success {
            background-color: #d4edda;
            color: #155724;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
        }
        .info {
            background-color: #d1ecf1;
            color: #0c5460;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🍓 Raspberry Pi File Upload Server</h1>
        <p>Upload files to your Raspberry Pi</p>
        
        <div class="upload-form">
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <br>
                <button type="submit">Upload File</button>
            </form>
        </div>
        
        <div class="info">
            <strong>Allowed file types:</strong> txt, pdf, png, jpg, jpeg, gif, doc, docx, zip<br>
            <strong>Max file size:</strong> 16MB
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """Display upload form"""
    return render_template_string(UPLOAD_FORM)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    # Secure the filename and add timestamp to avoid conflicts
    filename = secure_filename(file.filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = os.path.splitext(filename)
    unique_filename = f"{name}_{timestamp}{ext}"
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    
    try:
        file.save(filepath)
        file_size = os.path.getsize(filepath)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'filename': unique_filename,
            'size': file_size,
            'timestamp': timestamp
        }), 200
    except Exception as e:
        return jsonify({'error': f'Failed to save file: {str(e)}'}), 500

@app.route('/files', methods=['GET'])
def list_files():
    """List all uploaded files"""
    try:
        files = []
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(filepath):
                files.append({
                    'name': filename,
                    'size': os.path.getsize(filepath),
                    'modified': datetime.fromtimestamp(os.path.getmtime(filepath)).strftime('%Y-%m-%d %H:%M:%S')
                })
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to list files: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'upload_folder': app.config['UPLOAD_FOLDER'],
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    print(f"Starting file upload server...")
    print(f"Upload folder: {os.path.abspath(UPLOAD_FOLDER)}")
    print(f"Max file size: {MAX_FILE_SIZE / (1024*1024)}MB")
    print(f"Allowed extensions: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Run on all interfaces (0.0.0.0) so it's accessible from network
    # Use port 5000 by default
    app.run(host='0.0.0.0', port=5000, debug=False)

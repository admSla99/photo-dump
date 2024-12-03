from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from ftplib import FTP
import tempfile

app = Flask(__name__)

# Configure upload settings
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "temp_uploads")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# FTP settings
FTP_HOST = 'localhost'
FTP_USER = 'user'
FTP_PASS = 'password'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_to_ftp(file_path, filename):
    try:
        ftp = FTP(FTP_HOST)
        ftp.login(FTP_USER, FTP_PASS)
        
        with open(file_path, 'rb') as file:
            ftp.storbinary(f'STOR {filename}', file)
        
        ftp.quit()
        return True
    except Exception as e:
        print(f"FTP upload error: {str(e)}")
        return False

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file temporarily
        file.save(temp_path)
        
        # Upload to FTP
        if upload_to_ftp(temp_path, filename):
            # Clean up temp file
            os.remove(temp_path)
            return jsonify({'message': 'File uploaded successfully'}), 200
        else:
            os.remove(temp_path)
            return jsonify({'error': 'FTP upload failed'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    # Use PORT environment variable, default to 5000 if not set
    port = int(os.environ.get('FLASK_PORT', 5000))
    app.run(host='0.0.0.0', port=port)

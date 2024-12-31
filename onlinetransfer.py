from flask import Flask, request, send_from_directory
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mkv', 'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'}  # Added image formats

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 * 1024  # 1 GB limit

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')  # Serve index.html from the current working directory

@app.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400  # No file was sent with the 'file' key

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400  # The file input was empty

    if file and allowed_file(file.filename):
        filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            return f'''
            File uploaded successfully: {filename}
            <br>
            <a href="/uploads/{filename}">Click here to view the file</a>
            ''', 200
        except Exception as e:
            return f'Error saving file: {str(e)}', 500  # Log error if file save fails

    return 'Invalid file type', 400  # If the file type is not allowed

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

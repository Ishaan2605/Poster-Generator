import sys
import os
from flask import Flask, request, render_template, redirect, url_for, send_file
from werkzeug.utils import secure_filename

# Add src folder for importing backend pipeline module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from inference import run_pipeline  # Now import should work

app = Flask(__name__)



# Configure folders
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
POSTERS_DIR = "data/posters"
ANNOTATIONS_DIR = "data/annotations"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # max 10MB upload size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'userimg' not in request.files:
            return render_template('index.html', error="No file part in the request")

        file = request.files['userimg']
        if file.filename == '':
            return render_template('index.html', error="No file selected")

        if not allowed_file(file.filename):
            return render_template('index.html', error="Unsupported file type")

        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        # Run your backend pipeline - this function should generate output image path
        output_path = run_pipeline(input_path, POSTERS_DIR, ANNOTATIONS_DIR, app.config['OUTPUT_FOLDER'])

        output_filename = os.path.basename(output_path)
        output_url = url_for('static', filename=f'outputs/{output_filename}')

        return render_template('index.html', 
                               uploaded_img=url_for('static', filename=f'uploads/{filename}'),
                               output_img=output_url)

    # GET request
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

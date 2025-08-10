import sys
import os
from flask import Flask, request, render_template, jsonify, url_for
from werkzeug.utils import secure_filename

# Add src folder for importing backend pipeline module
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from inference import run_pipeline  # Your movie poster pipeline

app = Flask(__name__)

# Configurations for movie posters
UPLOAD_FOLDER = "static/uploads"
OUTPUT_FOLDER = "static/outputs"
POSTERS_DIR = "data/movie_posters"    # <- Update this to your movie posters folder
ANNOTATIONS_DIR = "data/annotations"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # max 10MB upload size

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Your token and phone number for MCP validation
VALID_BEARER_TOKEN = "0b035b2b9386"
USER_PHONE_NUMBER = "919967387737"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_bearer_token(token):
    return token == VALID_BEARER_TOKEN

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
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
        # Run your movie poster pipeline
        output_path = run_pipeline(input_path, POSTERS_DIR, ANNOTATIONS_DIR, app.config['OUTPUT_FOLDER'])
        output_filename = os.path.basename(output_path)
        output_url = url_for('static', filename=f'outputs/{output_filename}')
        return render_template('index.html', 
                               uploaded_img=url_for('static', filename=f'uploads/{filename}'),
                               output_img=output_url)
    return render_template('index.html')

@app.route('/mcp', methods=['POST'])
def mcp():
    data = request.json
    tool = data.get("tool")
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "") if auth_header.startswith("Bearer ") else None
    if not token or not check_bearer_token(token):
        return jsonify({"error": "Unauthorized"}), 401
    if tool == "validate":
        return jsonify({"phoneNumber": USER_PHONE_NUMBER})
    # Movie poster tool endpoint
    if tool == "movie_poster_replace":
        input_image_path = data.get("input_image_path")
        if not input_image_path or not os.path.exists(input_image_path):
            return jsonify({"error": "Invalid input image path"}), 400
        try:
            output_path = run_pipeline(input_image_path, POSTERS_DIR, ANNOTATIONS_DIR, OUTPUT_FOLDER)
            output_url = url_for('static', filename=f'outputs/{os.path.basename(output_path)}', _external=True)
            return jsonify({"output_image": output_url})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "Unknown tool"}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

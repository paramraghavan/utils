from flask import Flask, render_template, request, jsonify, send_from_directory
import yaml
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'yaml_files'
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def yaml_to_dict(yaml_content):
    """Convert YAML content to Python dictionary"""
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError as e:
        return {'error': str(e)}


def dict_to_yaml(data):
    """Convert Python dictionary to YAML string"""
    try:
        return yaml.dump(data, default_flow_style=False)
    except yaml.YAMLError as e:
        return str(e)


@app.route('/')
def index():
    """Main page route"""
    yaml_files = [f for f in os.listdir(app.config['UPLOAD_FOLDER'])
                  if f.endswith(('.yml', '.yaml'))]
    return render_template('index.html', yaml_files=yaml_files)


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle YAML file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and file.filename.endswith(('.yml', '.yaml')):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'filename': filename})

    return jsonify({'error': 'Invalid file type'})


@app.route('/load/<filename>')
def load_yaml(filename):
    """Load YAML file content"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        with open(file_path, 'r') as file:
            content = file.read()
            data = yaml_to_dict(content)
            return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/save', methods=['POST'])
def save_yaml():
    """Save modified YAML content"""
    try:
        data = request.json
        filename = secure_filename(data['filename'])
        content = dict_to_yaml(data['content'])

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'w') as file:
            file.write(content)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=9090)

# app.py
from flask import Flask, render_template, request, jsonify
import os
import yaml
import json
from process_yaml_file import read_yaml_file

app = Flask(__name__)

# Configuration
YAML_DIR = 'yaml_files'
os.makedirs(YAML_DIR, exist_ok=True)


def load_yaml_file(filename):
    try:
        # with open(os.path.join(YAML_DIR, filename), 'r') as file:
        #     return yaml.safe_load(file)
        return read_yaml_file(os.path.join(YAML_DIR, filename))
    except Exception as e:
        return {'error': str(e)}


def save_yaml_file(filename, content):
    try:
        with open(os.path.join(YAML_DIR, filename), 'w') as file:
            yaml.dump(content, file, sort_keys=False)
        return True
    except Exception as e:
        return False


@app.route('/')
def index():
    yaml_files = [f for f in os.listdir(YAML_DIR) if f.endswith(('.yml', '.yaml'))]
    return render_template('index.html', yaml_files=yaml_files)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})

    if not file.filename.endswith(('.yml', '.yaml')):
        return jsonify({'success': False, 'error': 'Invalid file type'})

    try:
        file.save(os.path.join(YAML_DIR, file.filename))
        return jsonify({'success': True, 'filename': file.filename})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

import json
@app.route('/load/<filename>')
def load_file(filename):
    content = load_yaml_file(filename)
    return json.dumps(content)
    # return jsonify(content)


@app.route('/save', methods=['POST'])
def save_file():
    data = request.json
    filename = data.get('filename')
    content = data.get('content')

    if not filename or content is None:
        return jsonify({'success': False, 'error': 'Missing filename or content'})

    success = save_yaml_file(filename, content)
    return jsonify({'success': success})


if __name__ == '__main__':
    app.run(debug=True, port=9090)
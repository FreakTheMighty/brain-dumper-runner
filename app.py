from flask import Flask, request, jsonify, send_from_directory
from werkzeug import secure_filename
import git

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = '/code/inputs/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def init(repo):
    git.Git().clone("git@github.com:%s.git"%repo)
    
@app.route('/')
def isalive():
    return "We're alive!"

@app.route('/forward', methods=['POST'])
def foward():
    attached_file = request.files['image']
    inputs = []
    for file_key in request.files.keys():
        if allowed_file(attached_file[file_key]):
            attached_file = request.files[file_key]
            filename = secure_filename(attached_file.filename)
            inputs.append(filename)


    return jsonify({'nearest': results})

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

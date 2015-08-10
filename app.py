from flask import Flask, request, jsonify, send_from_directory
from werkzeug import secure_filename
import git
import sys
import datetime
import imp

app = Flask(__name__, static_url_path='')

app.config['UPLOAD_FOLDER'] = '/brain/inputs/'

name = 'engine'
fp, pathname, description = imp.find_module('engine', ['/brain/'])
engine = imp.load_module(name, fp, pathname, description)
engine_ = engine.Engine()

@app.route('/')
def isalive():
    return "We're alive!"

@app.route('/forward', methods=['POST'])
def foward():
    inputs = []
    
    for file_key in request.files.keys():
       attached_file = request.files[file_key]
       filename_ = str(datetime.datetime.now()).replace(' ', '_') + \
           secure_filename(imagefile.filename)
       filename = os.path.join(UPLOAD_FOLDER, filename_)
       inputs.append(filename)
       attached_file.save(filename)

    results = engine_.forward(inputs)
    return jsonify(results)

if __name__ == "__main__":
    engine_.load()
    app.run(host="0.0.0.0", debug=True)

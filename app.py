from flask import Flask, request, jsonify
from werkzeug import secure_filename
import datetime
import imp
import os

app = Flask(__name__, static_url_path='')

BRAIN_DIR = '/brain'
UPLOAD_FOLDER = os.path.join(BRAIN_DIR, 'inputs')
BRAIN_MODULE = os.path.join(BRAIN_DIR, 'engine.py')

engine_ = None
if os.path.exists(BRAIN_MODULE):
    name = 'engine'
else:
    name = 'base_engine'
    
fp, pathname, description = imp.find_module(name, [ BRAIN_DIR , '/code' ])
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
           '_' + secure_filename(attached_file.filename)
       filename = os.path.join(UPLOAD_FOLDER, filename_)
       inputs.append(filename)
       attached_file.save(filename)

    results = engine_.foward(inputs)
    return jsonify(results)

if __name__ == "__main__":
    engine_.net = engine_.load()
    app.run(host="0.0.0.0", debug=True)

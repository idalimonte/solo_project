from flask import Flask
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
app.secret_key = "shhhhhh"
UPLOAD_FOLDER = os.path.join('staticFiles', 'uploads')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

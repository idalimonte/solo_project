from flask import Flask
from PIL import Image
import os
from werkzeug.utils import secure_filename


app = Flask(__name__, template_folder='templates', static_folder='staticFiles')
app.secret_key = "shhhhhh"
UPLOAD_FOLDER = "flask_app/staticFiles/uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


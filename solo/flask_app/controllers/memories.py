from flask import render_template,redirect,request, session, flash
from flask import flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.memory import Memory
from flask_bcrypt import Bcrypt

from werkzeug.utils import secure_filename
import os

bcrypt = Bcrypt(app)



@app.route('/success')
def success():
    if "user_id" not in session:
        return redirect('/logout')
    user = User.by_id(session["user_id"])
    print(session['user_id'])
    return render_template("dashboard.html", user=user, all_memories = Memory.get_all_memories())


@app.route('/show/<int:id>')
def show(id):
    data = {
        "id":id,
        }
    memory = Memory.get_one_memory(data)
    return render_template("show.html", memory=memory, user=User.show(data))


@app.route('/new')
def new_mem():
    return render_template("add.html")

@app.route('/add', methods = ['POST'])
def new_memory():
    if request.method == 'POST':
        # Upload file flask
        uploaded_img = request.files['media']
        # Extracting uploaded data file name
        img_filename = secure_filename(uploaded_img.filename)
        # Upload file to database (defined uploaded folder in static path)
        uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], img_filename)
    if not Memory.validate_memory(request.form):
        return redirect('/new')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'media': request.files['media'],
        'user_id': session['user_id']
    }
    Memory.add_memory(data)
    return redirect('/success')


@app.route('/show_image')
def displayImage():
    # Retrieving uploaded file path from session
    img_file_path = session.get('uploaded_img_file_path', None)
    # Display image in Flask application web page
    return render_template('show_image.html', user_image = img_file_path)



@app.route('/user/account')
def account_page():
    data = {
        'id': session['user_id']
    }
    user = User.get_user_mem(data)
    memory = Memory.get_one_memory(data)
    return render_template("edit.html", memory = memory, user=user, all_memories= Memory.get_all_memories())

@app.route('/user/account/update', methods=["POST"])
def update():
    Memory.update_mem(request.form)
    return redirect('/success')

@app.route('/destroy/<int:id>')
def delete(id):
    data = {
        "id":id
    }
    Memory.destroy(data)
    return redirect('/success')
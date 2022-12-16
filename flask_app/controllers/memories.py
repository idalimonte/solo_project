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
        if request.files:
            uploaded_img = request.files['media']
            filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_img.filename))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not Memory.validate_memory(request.form):
        return redirect('/new')
    data = {
        'title': request.form['title'],
        'description': request.form['description'],
        'media': request.files['media'],
        'user_id': session['user_id']
    }
    Memory.add_memory(data)
    return redirect('/show_image')


@app.route('/show_image')
def displayImage():
    img_file_path = session['uploaded_img_file_path']
    return render_template('show_image.html', img_file_path = img_file_path)



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
    if request.method == 'POST':
        if request.files:
            uploaded_img = request.files['media']
            filename = secure_filename(uploaded_img.filename)
            uploaded_img.save(os.path.join(app.config['UPLOAD_FOLDER'], uploaded_img.filename))
            session['uploaded_img_file_path'] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    data = {
        'id':request.form['id'],
        'title': request.form['title'],
        'description': request.form['description'],
        'media': request.files['media'],
        'user_id': session['user_id']
    }
    Memory.update_mem(data)
    return redirect('/success')

@app.route('/destroy/<int:id>')
def delete(id):
    data = {
        "id":id
    }
    Memory.destroy(data)
    return redirect('/success')
from datetime import datetime
import os

from flask import Flask, render_template, request, redirect, url_for, session
from passlib.hash import pbkdf2_sha256

from model import Task, User

app = Flask(__name__)

app.secret_key = b'\x9d\xb1u\x08%\xe0\xd0p\x9bEL\xf8JC\xa3\xf4J(hAh\xa4\xcdw\x12S*,u\xec\xb8\xb8'

@app.route('/all')
def all_tasks():
	return render_template('all.jinja2', tasks=Task.select())


@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        task = Task(name=request.form['name'])
        task.save()
        return redirect(url_for('all_tasks'))

    else:
        return render_template('create.jinja2')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is attempting to submit the login form (method is POST)
    if request.method == 'POST':
        user = User.select().where(User.username == request.form['name']).get()

        if user and pbkdf2_sha256.verify(request.form['password'], user.password):
            session['username'] = request.form['name']
            return redirect(url_for('all_tasks'))

        return render_template('login.jinja2', error="Incorrect username or password.")

    else:
        return render_template('login.jinja2')
    #    Find a user from the database that matches the username provided in the form submission
    #    If you find such a user and their password matches the provided password:
    #        Then log the user in by settings session['username'] to the users name
    #        And redirect the user to the list of all tasks
    #    Else:
    #        Render the login.jinja2 template and include an error message 
    # Else the user is just trying to view the login form
    #    so render the login.jinja2 template
@app.route('/incomplete', methods=['GET', 'POST'])
def incomplete_tasks():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        user = User.select().where(User.username == session['username']).get()

        Task.update(performed=datetime.now(), performed_by=user)\
            .where(Task.id == request.form['task_id'])\
            .execute()

    return render_template('incomplete.jinja2', tasks=Task.select().where(Task.performed.is_null()))


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

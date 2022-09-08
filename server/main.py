#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import sys

sys.path.append("../")
sys.path.append("../db")
sys.path.append("../eschool")
sys.path.append("../exceptions")
sys.path.append("../firebase")
sys.path.append("../mailing")
sys.path.append("../server")

from server.login import login
from db.database import Database
from eschool.eschool_server import EschoolServer
from exceptions.http_exceptions import *
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

eschool = EschoolServer()
db = Database(eschool)


@app.route('/')
def index():
    return "test passed"


@app.route('/login', methods=['POST'])
def login_request():
    firebase_id = request.form['firebase_id']
    username = request.form['login']
    password = request.form['password']
    try:
        version = request.form['version']
    except KeyError:
        version = "None"

    try:
        login(firebase_id, username, password, version, db, eschool)
    except EschoolAuthorisationException:
        return "wrong username or password"
    return "success"


@app.route('/logout', methods=['POST'])
def logout():
    db.connect()
    print(f'user deleted #{request.form["firebase_id"]}')
    db.del_user(request.form["firebase_id"], "logout", "logout")
    db.commit()
    return "success"


@app.route('/ver')
def ver():
    return db.get_ver()


@app.route('/new_event', methods=['POST'])
def new_event():
    db.insert_stat(request.form["msg"], request.form["event"], request.form["firebase_id"])
    return "success"


if __name__ == '__main__':
    app.run(debug=True)

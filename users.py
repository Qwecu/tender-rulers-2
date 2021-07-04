from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def logout():
    del session["username"]
    del session["user_id"]
    del session["csrf_token"]

def login(username, password):
    error = ""
    sql = "SELECT password_hash, id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        error = "No such user"
    else:
        hash_value = user[0]
        if check_password_hash(hash_value, password):
            session["username"] = username
            session["user_id"] = user[1]
            session["csrf_token"] = os.urandom(16).hex()
        else:
            error = "Password is incorrect"
    return error

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (:username, :hash)"
        db.session.execute(
            sql,
            {"username":username, "hash":hash_value}
            )
        db.session.commit()
    except:
        return "Registration failed"
    return login(username, password)

def user_exists(username):
    sql = "SELECT * FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone() != None

def loggedin():
    if session.get("username"):
        return True
    return False

def csrf():
    return session["csrf_token"]
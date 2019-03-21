import json

import bcrypt

from .models import User


def hash_password(pw):
    pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
    return pwhash.decode('utf8')


def validate_user(db, user, pwd):
    found_user = db.query(User).filter(User.name==user).first()
    if not found_user:  # User not found
        return -2

    if found_user.check_password(pwd):
        return found_user.permissions

    return -1  # Password wrong

def add_user(db, user, pwd):
    user_exists = db.query(User).filter(User.name==user).first()
    if user_exists:
        return 0
    try:
        new_user = User(name=user)
        new_user.set_password(pwd)
        db.add(new_user)
        db.flush()
        return 1
    except:
        return -1


def get_secret():
    """
    Returns secrets as a dict
    """
    with open('secrets') as f:
        secrets = json.load(f)
    return secrets

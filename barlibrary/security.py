import bcrypt
from sqlalchemy import and_

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
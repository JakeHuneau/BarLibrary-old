import transaction

from ..models import User

def change_user_permission(db, user, permission):
    with transaction.manager:
        found_user = db.query(User).filter(User.name == user).first()
        if not found_user:
            return False
        found_user.permissions = permission
    return True

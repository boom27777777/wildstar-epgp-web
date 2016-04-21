from epgp.db_objects.user import User, hash
from epgp.database import db_session


def add_user(username: str, password: str):
    user_id = User.query.all()[-1].id + 1
    tmp_user = User(user_id, username, hash(password))

    db_session.add(tmp_user)
    db_session.commit()

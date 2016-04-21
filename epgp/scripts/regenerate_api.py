from epgp.db_objects.user import User
from epgp.database import db_session


def run():
    for user in User.query.all():
        user.generate_api()
        db_session.add(user)
    db_session.commit()


if __name__ == '__main__':
    run()

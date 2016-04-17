import time
from base64 import encodebytes
from hashlib import md5
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.hybrid import hybrid_method
from epgp.database import Base


class Unauth:
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return 0


class User(Base):
    __tablename__ = 'users'
    _id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True)
    _hash = Column(String(20))
    _api_key = Column(String(26))

    def __init__(self, id, name, pass_hash):
        self._id = id
        self.name = name
        self._hash = pass_hash
        self._api_key = encodebytes(hash('Nope{}'.format(time.time())))

    def generate_api(self):
        self._api_key = encodebytes(hash('Nope{}'.format(time.time()))).decode()
        self._api_key = self._api_key.replace('\n', '')


    @hybrid_method
    def validate(self, password):
        return self._hash == hash(password)

    def validate_api(self, api_key):
        if type(api_key) is not bytes:
            return self._api_key == bytes(api_key, 'utf8')
        else:
            return self._api_key == api_key

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    @property
    def id(self):
        return self._id

    @property
    def api_key(self):
        return self._api_key

    def get_id(self):
        return self.id

    def __repr__(self):
        return self.name


def hash(password):
    hasher = md5()
    hasher.update(bytes(password, 'utf8'))
    return hasher.digest()


def user_by_api(api_key):
    for user in User.query.all():
        if user.api_key == api_key:
            return User

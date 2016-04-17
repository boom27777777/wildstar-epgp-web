from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from epgp import get_resource

engine = create_engine('sqlite:///' + get_resource('data', 'test.db'), convert_unicode=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


# noinspection PyUnresolvedReferences
def init_db():
    import epgp.db_objects.user

    Base.metadata.create_all(bind=engine)

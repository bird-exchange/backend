from sqlalchemy.ext.declarative import declarative_base
from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()


def get_db_session():
    engine = create_engine(current_app.config['DATABASE_URL'])
    db_session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
    return db_session


def init_db():
    engine = create_engine(current_app.config['DATABASE_URL'])
    db_session = get_db_session()
    Base.query = db_session.query_property()
    Base.metadata.create_all(bind=engine)

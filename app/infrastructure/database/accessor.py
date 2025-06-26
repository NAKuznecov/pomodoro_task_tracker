from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.settings import Settings

settings = Settings()

engine = create_engine(settings.db_url)

Session = sessionmaker(bind=engine)


def get_db_session():
    return Session

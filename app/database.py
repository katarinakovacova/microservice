from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


def get_engine(postgres_password: str):
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        password=postgres_password,
        host="localhost",
        database="postgres",
        port=5432,
    )

    return create_engine(url)


def get_session(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)()

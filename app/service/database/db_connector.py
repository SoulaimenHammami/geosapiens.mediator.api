from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.Utils import database_url, CONNECTION_MAX_OVERFLOW, CONNECTION_POOL_SIZE


class Connection:
    def __init__(self) -> None:
        self.engine = create_engine(
            database_url,
            pool_size=int(CONNECTION_POOL_SIZE),
            max_overflow=int(CONNECTION_MAX_OVERFLOW)
        )

    def get_session(self) -> Session:
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)
        db = SessionLocal()
        try:
            yield db
            print("currently session is opened")
        finally:
            db.close()
            print("currently session is closed")

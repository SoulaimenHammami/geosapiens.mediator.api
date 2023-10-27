from sqlalchemy import String,  Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Base(DeclarativeBase):
    pass


class Client(Base):
    __tablename__ = "client"
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[String] = mapped_column(String, nullable=False)
    expiration: Mapped[int] = mapped_column(Integer)
    request_limit: Mapped[int] = mapped_column(Integer)

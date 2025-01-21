"""The module responsible for model descriptions in the database."""

from uuid import UUID

from sqlalchemy import Integer, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base orm class."""

    pass


class Wallet(Base):
    """ORM representation of the wallet."""

    __tablename__ = "wallet"

    uuid: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

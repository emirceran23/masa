"""SQLAlchemy Base sınıfı."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Tüm modellerin miras alacağı temel sınıf."""

    pass

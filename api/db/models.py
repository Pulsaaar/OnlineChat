from sqlalchemy import Integer, String, Boolean, Text, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'  # Добавляем имя таблицы
    telegram_id: Mapped[str] = mapped_column(String, nullable=False, unique=True)

class Message(Base):
    __tablename__ = 'message'
    
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))  # Указываем корректную таблицу
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))  # Указываем корректную таблицу
    content: Mapped[str] = mapped_column(Text)

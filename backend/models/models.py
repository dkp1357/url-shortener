from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy import Index

from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime)

    urls = relationship("URL", back_populates="user")


class URL(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True, nullable=False)
    long_url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    is_custom = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    click_count = Column(Integer, default=0)
    expires_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="urls")
    clicks = relationship("ClickEvent", back_populates="url")

    __table_args__ = (
        Index("idx_short_code", "short_code"),
    )


class ClickEvent(Base):
    __tablename__ = "click_events"

    id = Column(Integer, primary_key=True, index=True)
    url_id = Column(Integer, ForeignKey("urls.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    ip_hash = Column(String)
    country_code = Column(String)
    device_type = Column(String)
    browser = Column(String)
    os = Column(String)
    referrer_host = Column(String)

    url = relationship("URL", back_populates="clicks")

    __table_args__ = (
        Index("idx_url_timestamp", "url_id", "timestamp"),
    )
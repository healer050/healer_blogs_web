# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime

# from pbkdf2 import PBKDF2
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ( Column, Integer, String,
                        Boolean, DateTime,Text)

from libs.db.dbsession import engine
from libs.db.dbsession import dbSession

Base = declarative_base(engine)


class Message_board(Base):
    __tablename__ = 'messages'
    uid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text,nullable=False)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    is_top = Column(Boolean,default=0)


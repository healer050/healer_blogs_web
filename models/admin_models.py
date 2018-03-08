#coding=utf-8
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ( Column, Integer, String,
                        Boolean, DateTime)

from libs.db.dbsession import engine
from libs.db.dbsession import dbSession
from utils.hashers import make_password,check_password
Base = declarative_base(engine)



class CmsUsers(Base):

    __tablename__ = 'cms_users'

    uuid = Column(String(36), unique=True, nullable=False, default=lambda: str(uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_name = Column(String(50), nullable=True)
    email = Column(String(50),unique=False,nullable=False)
    _password = Column('password', String(128))
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime)
    last_login = Column(DateTime)
    loginnum = Column(Integer, default=False)
    _locked = Column(Boolean, default=False, nullable=False)
    avatar = Column(String(128))

    # set_password
    def set_password(self, raw_password):
        if not raw_password:
            return None
        temp_password = make_password(raw_password, self.email)
        return temp_password



    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self.set_password(password)

    # check_password
    def auth_password(self, raw_password):
        return check_password(raw_password, self.password, self.email)


    @classmethod
    def all(cls):
        return dbSession.query(cls).all()

    @classmethod
    def by_id(cls, id):
        return dbSession.query(cls).filter(cls.id == id).first()

    @classmethod
    def by_email(cls, email):
        return dbSession.query(cls).filter(cls.email == email).first()

    @classmethod
    def by_uuid(cls, uuid):
        return dbSession.query(cls).filter(cls.uuid == uuid).first()

    @classmethod
    def black_list(cls):
        return dbSession.query(cls).filter(cls._locked == 1).all()

    @classmethod
    def white_list(cls):
        return dbSession.query(cls).filter(cls._locked == 0).all()

    @classmethod
    def by_name(cls, name):
        return dbSession.query(cls).filter(cls.admin_name == name).first()

    @property
    def locked(self):
        return self._locked



    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value


    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'last_login': self.last_login,
        }

    def __repr__(self):
        return u'<CmsUser - id: %s  email: %s>' % (self.id,self.email)
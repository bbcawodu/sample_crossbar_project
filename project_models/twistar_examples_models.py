from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    age = Column(Integer)
    first_name = Column(String(1000))
    last_name = Column(String(1000))
    nickname = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    posts = relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s')>" % (
                                self.first_name, self.last_name)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    body = Column(String(140))
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


class PresenceBrowsingData(Base):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, primary_key=True)
    cookie_id = Column(String(10000))
    oncology_clicks = Column(Integer)
    oncology_hover_time = Column(Float)

    def __repr__(self):
        return "<PresenceBrowsingData_entry(cookie_id='%s')>" % self.cookie_id

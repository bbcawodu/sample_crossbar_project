from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    age = Column(Integer)
    first_name = Column(String(1000))
    last_name = Column(String(1000))

    def __repr__(self):
        return "<User(first_name='%s', last_name='%s')>" % (
                                self.first_name, self.last_name)

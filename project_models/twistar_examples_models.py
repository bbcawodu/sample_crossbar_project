from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

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


class PresenceBrowsingData(Base):
    __tablename__ = 'presencebrowsingdata'

    id = Column(Integer, Sequence('presencebrowsingdata_id_seq'), primary_key=True)
    cookie_id = Column(String(10000))
    oncology_clicks = Column(Integer)
    oncology_hover_time = Column(Float)

    def __repr__(self):
        return "<PresenceBrowsingData_entry(cookie_id='%s')>" % self.cookie_id

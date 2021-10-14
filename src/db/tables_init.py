import logging
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
google.cloud.logging.handlers.setup_logging(handler)
logging.getLogger().setLevel(logging.DEBUG)

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from .db_connect import init_connection_engine


db = init_connection_engine()
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"
    TableID = Column(Integer, primary_key=True, autoincrement=True)
    ContactID = Column(String(100), primary_key=True)
    Company = Column(String(100))
    City = Column(String(100))
    Country = Column(String(100))
    EmailAddress = Column(String(100))
    FirstName = Column(String(100))
    LastName = Column(String(100))
    Title = Column(String(100))
    MobilePhone = Column(String(100))
    LastModifiedUTC = Column(DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return "<Contact(ContactID='%s')>" % self.ContactID


def create_tables():
    try:
        Base.metadata.create_all(db)
        logging.debug("-----CREATED----- table Contact")
        return True
    except Exception as e:
        logging.debug(e)
        return False


def delete_tables():
    try:
        Base.metadata.drop_all(db)
        logging.debug("-----DELETED----- table Contact")
        return True
    except Exception as e:
        logging.debug(e)
        return False

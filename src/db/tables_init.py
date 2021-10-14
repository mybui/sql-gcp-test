import google.cloud.logging

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

from sqlalchemy import Column, String, DateTime, Integer, text
from sqlalchemy.ext.declarative import declarative_base

from .db_connect import init_connection_engine

import logging

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
    TimeLastUpdatedInUTC = Column(DateTime(timezone=True),
                                  server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))

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

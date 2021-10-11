import google.cloud.logging

client = google.cloud.logging.Client()
client.get_default_handler()
client.setup_logging()

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

from .db_connect import init_connection_engine

import logging

db = init_connection_engine()
Base = declarative_base()


class Contact(Base):
    __tablename__ = "contact"
    ContactUUID = Column(String(100), primary_key=True)
    C_Company = Column(String(100))
    C_City = Column(String(100))
    C_Country = Column(String(100))
    C_EmailAddress = Column(String(100))
    C_FirstName = Column(String(100))
    C_LastName = Column(String(100))
    C_Title = Column(String(100))
    C_MobilePhone = Column(String(100))
    TimeInsertedUTC = Column(DateTime(timezone=True))

    def __repr__(self):
        return "<Contact(C_SFDCContactID='%s')>" % self.C_SFDCContactID


def create_tables():
    try:
        Base.metadata.create_all(db)
        logging.debug("-----CREATED----- tables Contact")
        return True
    except Exception as e:
        logging.debug(e)
        return False


def delete_tables():
    try:
        Base.metadata.drop_all(db)
        logging.debug("-----DELETED----- tables Contact")
        return True
    except Exception as e:
        logging.debug(e)
        return False

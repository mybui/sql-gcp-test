import logging
import google.cloud.logging
from google.cloud.logging_v2.handlers import CloudLoggingHandler

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client)
google.cloud.logging.handlers.setup_logging(handler)
logging.getLogger().setLevel(logging.DEBUG)

from contextlib import contextmanager

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from .tables_init import *

import pandas
import json


@contextmanager
def start_psql_session():
    session = Session(bind=init_connection_engine())
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_query(session_, purpose, type):
    try:
        if purpose == "sort_upsert_data":
            if type == "contact":
                query = session_.query(Contact.ContactID)
                return query
        if purpose == "select_all_data":
            if type == "contact":
                query = session_.execute(select(*Contact.__table__.columns))
                return query
    except Exception as e:
        logging.debug(e)
        return None


def sort_upsert_data(session_, type, data):
    ids_to_update = []
    result = dict()
    if type == "contact":
        ids = [entry_["ContactID"] for entry_ in data]
        existing_data = None
        if type == "contact":
            existing_data = create_query(session_=session_, purpose="sort_upsert_data", type=type).filter(Contact.ContactID.in_(ids)).all()
        for entry in existing_data:
            ids_to_update.append(entry[0])
        result["entries_to_update"] = [entry for entry in data if entry["ContactID"] in ids_to_update]
        result["entries_to_insert"] = [entry for entry in data if entry["ContactID"] not in ids_to_update]
    return result


def upsert_contact(session_, data):
    if data:
        upsert_data = sort_upsert_data(session_=session_, type="contact", data=data)
        contacts_to_update = upsert_data.get("entries_to_update", [])
        contacts_to_insert = upsert_data.get("entries_to_insert", [])
        update_check = None
        insert_check = None
        if contacts_to_update:
            try:
                for i in range(0, len(contacts_to_update)):
                    session_.execute(
                        Contact.__table__.update()
                            .values
                                (
                                    ContactID=contacts_to_update[i].get("ContactID", None) or None,
                                    Company=contacts_to_update[i].get("Company", None),
                                    City=contacts_to_update[i].get("City", None) or None,
                                    Country=contacts_to_update[i].get("Country", None) or None,
                                    EmailAddress=contacts_to_update[i].get("EmailAddress", None) or None,
                                    FirstName=contacts_to_update[i].get("FirstName", None) or None,
                                    LastName=contacts_to_update[i].get("LastName", None) or None,
                                    Title=contacts_to_update[i].get("Title", None) or None,
                                    MobilePhone=contacts_to_update[i].get("MobilePhone", None) or None,
                                )
                            .where(Contact.ContactID == contacts_to_update[i]["ContactID"])
                    )
                update_check = True
                no_contacts_to_update = len(contacts_to_update)
            except Exception as e:
                print(e)
        if contacts_to_insert:
            try:
                session_.execute(
                    Contact.__table__.insert(),
                    [
                        dict
                            (
                                ContactID=contacts_to_insert[i].get("ContactID", None) or None,
                                Company=contacts_to_insert[i].get("Company", None) or None,
                                City=contacts_to_insert[i].get("City", None) or None,
                                Country=contacts_to_insert[i].get("Country", None) or None,
                                EmailAddress=contacts_to_insert[i].get("EmailAddress", None) or None,
                                FirstName=contacts_to_insert[i].get("FirstName", None) or None,
                                LastName=contacts_to_insert[i].get("LastName", None) or None,
                                Title=contacts_to_insert[i].get("Title", None) or None,
                                MobilePhone=contacts_to_insert[i].get("MobilePhone", None) or None,
                            )
                        for i in range(0, len(contacts_to_insert))
                    ]
                )
                insert_check = True
                no_contacts_to_insert = len(contacts_to_insert)
            except Exception as e:
                print(e)
        if update_check and insert_check:
            logging.debug(
                "-----UPSERTED----- {0} records to table Contact".format(no_contacts_to_update + no_contacts_to_insert))
            return True, {"Updated": no_contacts_to_update,
                          "Inserted": no_contacts_to_insert}
        elif update_check and not insert_check:
            logging.debug("-----UPDATED----- {0} records to table Contact".format(no_contacts_to_update))
            return True, {"Updated": no_contacts_to_update,
                          "Inserted": 0}
        elif not update_check and insert_check:
            logging.debug("-----INSERTED----- {0} records to table Contact".format(no_contacts_to_insert))
            return True, {"Updated": 0,
                          "Inserted": no_contacts_to_insert}
        else:
            logging.debug("-----ERROR----- bulk upsert to table Contact")
            return False, {"Updated": "failed",
                           "Inserted": "failed"}
    else:
        logging.debug("No data to upsert to table Contact")
        return None, {"Updated": 0,
                      "Inserted": 0}


def select_all_contact(session_):
    rows = create_query(session_=session_, purpose="select_all_data", type="contact")
    if rows:
        return json.loads(pandas.DataFrame.from_records(list(rows), columns=rows.keys()).to_json(orient="records"))
    return None

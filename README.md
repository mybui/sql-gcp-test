# Contact DB API

- A web application that displays contact information hosted on Google Cloud Platform.
- CI/CD: Docker, Cloud Build and Cloud Run
- Stack: Flask, SQLAlchemy, PostgreSQL, Google Cloud SQL

****

## Starting API
### Locally via Postman or a web browser
https://sql-gcp-test-teryvp4d3a-lz.a.run.app/

### Locally via CLI
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service/account/key.json
export DB_HOST='127.0.0.1:5433'
export DB_USER='<DB_USER_NAME>'
export DB_PASS='<DB_PASSWORD>'
export DB_NAME='<DB_NAME>'
./cloud_sql_proxy -instances=<project-id>:<region>:<instance-name>=tcp:5433 -credential_file=$GOOGLE_APPLICATION_CREDENTIALS &

virtualenv --python python3 venv
source venv/bin/activate

cd src
pip3 install -r requirements.txt
python3 app.py
`````


### Cloud environment via Google Cloud Platform Cloud Run
```bash
gcloud init
gcloud auth login
gcloud builds submit --tag gcr.io/[project-id]/sql-gcp-test

# follow the url that appears on cloud run
`````

***


## Check app status
- Endpoint: `/`
- Full endpoint: https://sql-gcp-test-teryvp4d3a-lz.a.run.app/

### Request
Method: `GET`

### Response
Body:
```
{
    "Status": "OK"
}
```

## Check database status
Endpoint: `/db`
Full endpoint: https://sql-gcp-test-teryvp4d3a-lz.a.run.app/db

### Request
Method: `GET`

### Response
Body:
```
{
    "Details": [
        {
            "Database": "ruukki_integration_renewal"
        }
    ],
    "Status": "OK"
}
```

## List all contacts
- Endpoint: `/contact`
- Full endpoint: https://sql-gcp-test-teryvp4d3a-lz.a.run.app/contact

### Request
Method: `GET`

### Response
Body:
```
{
    "Count": 4,
    "Details": [
        {
            "Database": "ruukki_integration_renewal",
            "Result": [
                {
                    "City": "Helsinki",
                    "Company": "Test Company 1",
                    "ContactID": "UUID1234",
                    "Country": "Finland",
                    "EmailAddress": "abc_2@abc.com",
                    "FirstName": "Blue",
                    "LastModifiedUTC": 1634215517780,
                    "LastName": "Berry",
                    "MobilePhone": "0401234567",
                    "TableID": 1,
                    "Title": "Manager"
                },
                {
                    "City": "Helsinki",
                    "Company": "Test Company 2",
                    "ContactID": "UUID12345678",
                    "Country": "Finland",
                    "EmailAddress": "abc@abc.com",
                    "FirstName": "Pink",
                    "LastModifiedUTC": 1634215748925,
                    "LastName": "Berry",
                    "MobilePhone": "0401234568",
                    "TableID": 2,
                    "Title": "Manager"
                },
                {
                    "City": "Stockholm",
                    "Company": "Test Company 3",
                    "ContactID": "UUID12345999",
                    "Country": "Sweden",
                    "EmailAddress": "abc_3@abc.com",
                    "FirstName": "Black",
                    "LastModifiedUTC": 1634216095297,
                    "LastName": "Berry",
                    "MobilePhone": "0501234599",
                    "TableID": 3,
                    "Title": "Specialist"
                },
                {
                    "City": "Stockholm",
                    "Company": "Test Company 4",
                    "ContactID": "UUID12345888",
                    "Country": "Sweden",
                    "EmailAddress": "abc_4@abc.com",
                    "FirstName": "Blue",
                    "LastModifiedUTC": 1634217053582,
                    "LastName": "Berry",
                    "MobilePhone": "0501234888",
                    "TableID": 4,
                    "Title": "Specialist"
                }
            ],
            "Table": "Contact"
        }
    ],
    "Status": "OK"
}
```

## Create a contact
- Endpoint: `/contact`
- Full endpoint: https://sql-gcp-test-teryvp4d3a-lz.a.run.app/contact

### Request
Method: `POST`
Body:
```
[
    {
        "City": "Stockholm",
        "Company": "Test Company 4",
        "Country": "Sweden",
        "EmailAddress": "abc_4@abc.com",
        "FirstName": "Blue",
        "LastName": "Berry",
        "MobilePhone": "0501234888",
        "Title": "Specialist",
        "ContactID": "UUID12345888"
    }
]
```

### Response
Body: note that "Inserted": 1
```
{
    "Count": [
        {
            "Inserted": 1,
            "Updated": 0
        }
    ],
    "Details": [
        {
            "Database": "ruukki_integration_renewal",
            "Table": "Contact"
        }
    ],
    "Status": "OK"
}
```

## Update a contact
### (by repeat creating a contact with same ContactID, should be a separate PUT/PATCH request in real production scenario)
- Endpoint: `/contact`
- Full endpoint: https://sql-gcp-test-teryvp4d3a-lz.a.run.app/contact

### Request
Method: `POST`
Body:
```
[
    {
        "City": "Stockholm",
        "Company": "Test Company 4",
        "Country": "Sweden",
        "EmailAddress": "abc_4@abc.com",
        "FirstName": "Blue",
        "LastName": "Berry",
        "MobilePhone": "0501234888",
        "Title": "Specialist",
        "ContactID": "UUID12345888"
    }
]
```

### Response
Body: note that "Updated": 1
```
{
    "Count": [
        {
            "Inserted": 0,
            "Updated": 1
        }
    ],
    "Details": [
        {
            "Database": "ruukki_integration_renewal",
            "Table": "Contact"
        }
    ],
    "Status": "OK"
}
```
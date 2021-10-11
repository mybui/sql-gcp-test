### local

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
pip install -r requirements.txt
python3 app.py
`````


### cloud run
```bash
gcloud init
gcloud auth login
gcloud builds submit --tag gcr.io/[project-id]/sql-gcp-test
`````
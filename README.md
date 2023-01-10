# ML Dataflow

App for simulating AI-backed receipt image recognition.

 - WebAPI: FastAPI
 - DB: Postgres
 - IaC: Airflow

are for my choice.

## Usage

In this directory,
```bash
cd ml_dag_dataflow
docker compose up -d
```
Or you might need airflow initialization before the above line by
```bash
docker compose up airflow-init
```

After all the containers are ready,

## to access to Airflow GUI (can be done by CLI, too)

on your browser, go to http://localhost:8080/  and login with
 - user: airflow
 - pass: airflow

"ml_task" in the DAG columns is my workflow so execute it as many as you want by clicking run button.

NOTE: one cycle only generates only one query from the corresponding id so to see the GET response in the next step, you should run several times in this step.


## to access to analytics web api

on your browser, go to http://localhost:8000/api/analytics/{business_id}, where business_id is 0~9 for this dev environment.

For example, if query parameter {business_id} exists, you could see this kind of response.

```
{"total":3116.0,"average_ai_score":0.30333334,"average_ocr_score":0.32444444,"num_valid_receipts":9,"business_id":8,"bbox":"[0.34, 0.48, 0.21, 0.92], [0.47, 0.76, 0.15, 0.83], [0.46, 0.8, 0.06, 0.29], [0.36, 0.11, 0.91, 0.41], [0.84, 0.07, 0.09, 0.76]"}
```

If not, it returns null.


For Airflow testing,

Go to the container commandline
```
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.0/airflow.sh'
chmod +x airflow.sh
./airflow.sh bash
```
then,

- to check dag is well defined
```
python pipeline.py
```
- to check if it runs correctly
```
airflow dags test ml_task
```
- for unittest
```
pytest dags/tests/test_pipeline.py
```

# Comments on this Implementation

- DB choice: I chose SQL for storing analytics data but would be better to use NoSQL especially Key-Value DB, if # of users (business_ids) are becoming large for the following reasons.
    - when accessing to SQL, it searches a target data using bussiness_id as an unique key but it costs linear time while Key-Values DB only takes constant time.
    - easy to scale (like sharding with respect to id etc)

- DataFlow: I defined the DAG flow for every user's input as
```
    create_receipt  ->  parse_ml_response -> push_to_parsed_db
```
but when user's input comes more fequently (like < 3 sec interval), this dag might not be effective. If so "parse_ml_response" should not always comes after "creat_receipt" but instead can be reguraly run.


- data schema management: I defined shema at /dags/manage_data/db/create_fixtures.sql but would be manageable if using openapi.
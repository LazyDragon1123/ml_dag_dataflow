db_name = "veryfidev"
db_user = "airflow"
db_pass = "airflow"
db_host = "db"
db_port = "5432"
db_string = "postgresql://{}:{}@{}:{}/{}".format(db_user, db_pass, db_host, db_port, db_name)

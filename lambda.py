import json
import mysql.connector
import os


def lambda_handler(event, context):
    user = os.environ["PERSONAL_DB_USER"]
    password = os.environ["PERSONAL_DB_PASS"]
    host = os.environ["PERSONAL_DB_HOST"]
    database = os.environ["PERSONAL_DB_DB"]
    print(user)
    print(password)
    print(host)
    print(database)
    cnx = mysql.connector.connect(
        user=user,
        password=password,
        host=host,
        database=database,
    )
    cnx.close()

    return {"statusCode": 200, "body": json.dumps("Success")}

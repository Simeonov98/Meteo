import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT"), 
    ssl_verify_identity=True
    )


def push(data):
    cursor = connection.cursor()
    cursor.execute(data)
    connection.commit()
    



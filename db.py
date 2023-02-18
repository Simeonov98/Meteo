import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector

load_dotenv()


def connect(data):
    connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT"), #tova go nqmash
    ssl_verify_identity=True
    )
    # try:
    #     if connection.is_connected():
    #         cursor = connection.cursor()
    #     cursor.execute("select @@version ")
    #     version = cursor.fetchone()
    #     if version:
    #         print('Running version: ', version)
    #     else:
    #         print('Not connected.')
    # except Error as e:
    #     print("Error while connecting to MySQL", e)
    #finally:
     #   connection.close()
    cursor = connection.cursor()
    cursor.execute(data)
    connection.commit()


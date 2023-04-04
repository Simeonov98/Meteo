import os
from dotenv import load_dotenv
from mysql.connector import Error
import mysql.connector
from PIL import Image
import hash



load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT"), 
    ssl_verify_identity=True,
    
    )


def push(data):
    cursor = connection.cursor()
    cursor.execute(data)
    connection.commit()
    
def select(data):
    cursor = connection.cursor()
    cursor.execute(data)
    res=cursor.fetchall()
    return res

def readBLOB(id):
    print("Reading BLOB data from python_employee table")

    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("PASSWORD"),
            ssl_ca=os.getenv("SSL_CERT"), 
            ssl_verify_identity=True)

        cursor = connection.cursor()
        sql_fetch_blob_query = """SELECT * from Image where id = %s"""

        cursor.execute(sql_fetch_blob_query, (id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], )
            print("Name = ", row[1])
            image = row[2]
            
            print("Storing employee image and bio-data on disk \n")
            write_file(image, row[1]+".png")
           

    except mysql.connector.Error as error:
        print("Failed to read BLOB data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insertBLOB(name, photo):
    print("Inserting BLOB into Images table")
    try:
        connection = mysql.connector.connect(
            host=os.getenv("HOST"),
            database=os.getenv("DATABASE"),
            user=os.getenv("DB_USERNAME"),
            password=os.getenv("PASSWORD"),
            ssl_ca=os.getenv("SSL_CERT"), 
            ssl_verify_identity=True)
        cursor = connection.cursor()
        sql_insert_blob_query = """ INSERT IGNORE INTO Image
                          (name, src) VALUES (%s,%s)"""

        empPicture = hash.convertToBinaryData(photo)
       

        # Convert data into tuple format
        insert_blob_tuple = (name, empPicture)
        result = cursor.execute(sql_insert_blob_query, insert_blob_tuple)
        connection.commit()
        print("Image and file inserted successfully as a BLOB into Image table", result)

    except mysql.connector.Error as error:
        print("Failed inserting BLOB data into MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")   

def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open("./imgtest/"+filename, 'wb') as file:
        file.write(data)

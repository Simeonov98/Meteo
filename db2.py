
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from PIL import Image
import hash

load_dotenv()

# Establish connection to PostgreSQL database
connection = psycopg2.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("DB_USERNAME"),
    password=os.getenv("PASSWORD"),
    sslmode='require',
    sslrootcert=os.getenv("SSL_CERT")
)

def push(query, params=None):
#    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params)
            connection.commit()
#    except Exception as e:
#        print(f"Error executing query: {e}")
#        connection.rollback()
def select(query, params=None):
#    try:
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
#    except Exception as e:
#        print(f"Error executing query: {e}")
#        return []

def readBLOB(record_id):
    print("Reading BLOB data from Image table")
    try:
        with connection.cursor() as cursor:
            query = sql.SQL("SELECT * FROM Image WHERE id = %s")
            cursor.execute(query, (record_id,))
            records = cursor.fetchall()
            for row in records:
                print("Id = ", row[0])
                print("Name = ", row[1])
                image = row[2]
                print("Storing image on disk \n")
                write_file(image, f"{row[1]}.png")
    except Exception as e:
        print(f"Failed to read BLOB data from PostgreSQL table: {e}")
        connection.rollback()
    # finally:
    #     if connection:
    #         connection.close();
    #         print("Postgres Connection is close from READBLOB func")

def insertBLOB(name, photo):
    print("Inserting BLOB into Images table")
    try:
        with connection.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO Image (name, src) VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """)
            emp_picture = hash.convertToBinaryData(photo)
            cursor.execute(query, (name, emp_picture))
            connection.commit()
            print("Image inserted successfully as a BLOB into Image table")
    except Exception as e:
        print(f"Failed to insert BLOB data into PostgreSQL table: {e}")
        connection.rollback()
    # finally:
    #     if connection:
    #         connection.close();
    #         print("Postgres connection closed from InsertBlob func")

def write_file(data, filename):
    # Convert binary data to proper format and write it on disk
    with open(f"./imgtest/{filename}", 'wb') as file:
        file.write(data)

# def close_conn():
#     connection.close();
#     print("Connection is closed from func close_conn");

# Ensure the connection is properly closed when done
# try:
#    pass # Add your testing or function calls here if needed
# finally:
#    if connection:
#        connection.close()
#        print("PostgreSQL connection is closed FROM FINAL LINE!!!!!!!")

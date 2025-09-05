import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from PIL import Image
import hash  # assuming you have a hash module with convertToBinaryData

load_dotenv()

def get_connection():
    """Create and return a new PostgreSQL connection."""
    return psycopg2.connect(
        host=os.getenv("HOST"),
        database=os.getenv("DATABASE"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("PASSWORD"),
        sslmode='require',
        sslrootcert=os.getenv("SSL_CERT")
    )


def push(query, params=None):
    """Execute an INSERT/UPDATE/DELETE query."""
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
    except Exception as e:
        print(f"Error executing query: {e}")


def select(query, params=None):
    """Execute a SELECT query and return results as list of dicts."""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
    except Exception as e:
        print(f"Error executing query: {e}")
        return []


def insertBLOB(name, photo):
    """Insert an image as BLOB into the Image table."""
    print("Inserting BLOB into Image table")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("""
                    INSERT INTO Image (name, src) VALUES (%s, %s)
                    ON CONFLICT (name) DO NOTHING
                """)
                emp_picture = hash.convertToBinaryData(photo)
                cursor.execute(query, (name, emp_picture))
                conn.commit()
                print("Image inserted successfully as a BLOB into Image table")
    except Exception as e:
        print(f"Failed to insert BLOB data into PostgreSQL table: {e}")


def readBLOB(record_id, save_dir="./imgtest"):
    """Read a BLOB from the Image table and write it to disk."""
    print("Reading BLOB data from Image table")
    try:
        with get_connection() as conn:
            with conn.cursor() as cursor:
                query = sql.SQL("SELECT id, name, src FROM Image WHERE id = %s")
                cursor.execute(query, (record_id,))
                record = cursor.fetchone()
                if record:
                    _, name, image_data = record
                    os.makedirs(save_dir, exist_ok=True)
                    filepath = os.path.join(save_dir, f"{name}.png")
                    with open(filepath, "wb") as f:
                        f.write(image_data)
                    print(f"Image saved to {filepath}")
                else:
                    print(f"No record found with id {record_id}")
    except Exception as e:
        print(f"Failed to read BLOB data from PostgreSQL table: {e}")


def write_file(data, filename, save_dir="./imgtest"):
    """Write binary data to disk."""
    os.makedirs(save_dir, exist_ok=True)
    with open(os.path.join(save_dir, filename), 'wb') as file:
        file.write(data)

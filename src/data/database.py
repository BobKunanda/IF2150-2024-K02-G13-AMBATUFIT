import sqlite3
import os


def connect_db(db_filename):
    """Membuka koneksi ke database SQLite3 dan mengembalikan objek koneksi dan cursor."""
    connection = sqlite3.connect(db_filename)
    cursor = connection.cursor()

    connection.row_factory = sqlite3.Row
    return connection, cursor


def execute_query(connection, cursor, query, params=None):
    """Menjalankan query SQL (INSERT, UPDATE, DELETE, SELECT)."""
    if params is None:
        params = []
    cursor.execute(query, params)
    connection.commit()


def fetch_all(connection, cursor, query, params=None):
    """Menjalankan query SELECT dan mengembalikan hasil dalam bentuk list of dicts."""
    if params is None:
        params = []
    cursor.execute(query, params)
    return cursor.fetchall()


def fetch_one(connection, cursor, query, params=None):
    """Menjalankan query SELECT dan mengembalikan satu hasil."""
    if params is None:
        params = []
    cursor.execute(query, params)
    return cursor.fetchone()


def close_db(connection):
    """Menutup koneksi database."""
    connection.close()
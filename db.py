# db.py

import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

db = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME
)

cursor = db.cursor()

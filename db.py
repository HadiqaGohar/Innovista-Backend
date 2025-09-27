# # db.py
# import pymysql
# import os

# def get_db():
#     conn = pymysql.connect(
#         host=os.getenv("DB_HOST", "127.0.0.1"),
#         user=os.getenv("DB_USER", "root"),
#         password=os.getenv("DB_PASS", ""),
#         database=os.getenv("DB_NAME", "medicura"),
#         port=int(os.getenv("DB_PORT", 4000)),
#         cursorclass=pymysql.cursors.DictCursor
#     )
#     return conn



# db.py
import pymysql
import os

def get_db():
    conn = pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "medicura"),
        port=int(os.getenv("DB_PORT", 4000)),
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn

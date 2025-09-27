# # db_setup.py
# from main import get_db

# def init_db():
#     conn = get_db()
#     with conn.cursor() as cur:
#         cur.execute("""
#             CREATE TABLE IF NOT EXISTS appointments (
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 patient_name VARCHAR(255),
#                 doctor_name VARCHAR(255),
#                 appointment_time DATETIME,
#                 notes TEXT,
#                 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#             )
#         """)
#     conn.commit()
#     conn.close()
#     print("✅ appointments table created")


# if __name__ == "__main__":
#     init_db()



# db_setup.py
from db import get_db

def init_db():
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                patient_name VARCHAR(255),
                doctor_name VARCHAR(255),
                appointment_time DATETIME,
                notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    conn.commit()
    conn.close()
    print("✅ appointments table created")


if __name__ == "__main__":
    init_db()

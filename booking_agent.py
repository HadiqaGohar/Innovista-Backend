# import random
# from datetime import datetime, timedelta
# import pymysql
# import os
# from typing import Tuple, Dict, Any

# # TiDB Configuration (same as your main.py)
# DB_CONFIG = {
#     "host": os.getenv("TIDB_HOST", "gateway01.us-west-2.prod.aws.tidbcloud.com"),
#     "port": 4000,
#     "user": os.getenv("TIDB_USERNAME", "34oY1b3G6arXWAM.root"),
#     "password": os.getenv("TIDB_PASSWORD", "M9iWYjgizxiiT1qh"),
#     "database": os.getenv("TIDB_DATABASE", "test"),
#     "charset": "utf8mb4",
#     "ssl": {"ssl_mode": "VERIFY_IDENTITY"}
# }

# def get_db_connection():
#     """Establish connection to TiDB"""
#     try:
#         return pymysql.connect(**DB_CONFIG)
#     except Exception as e:
#         raise Exception(f"Database connection failed: {str(e)}")

# def init_appointments_table():
#     """Initialize appointments table if not exists"""
#     try:
#         conn = get_db_connection()
#         with conn.cursor() as cur:
#             cur.execute("""
#                 CREATE TABLE IF NOT EXISTS appointments (
#                     id INT AUTO_INCREMENT PRIMARY KEY,
#                     citizen_name VARCHAR(255) NOT NULL,
#                     service VARCHAR(255) NOT NULL,
#                     contact VARCHAR(255) NOT NULL,
#                     appointment_time DATETIME NOT NULL,
#                     status VARCHAR(50) DEFAULT 'scheduled',
#                     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#                     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
#                 )
#             """)
#             conn.commit()
#         conn.close()
#         print("Appointments table initialized successfully")
#     except Exception as e:
#         print(f"Error initializing appointments table: {str(e)}")

# def save_appointment_to_db(appointment_data: Dict[str, Any]) -> int:
#     """Save appointment to TiDB and return appointment ID"""
#     try:
#         conn = get_db_connection()
#         with conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO appointments (citizen_name, service, contact, appointment_time, status)
#                 VALUES (%s, %s, %s, %s, %s)
#             """, (
#                 appointment_data['citizen_name'],
#                 appointment_data['service'],
#                 appointment_data['contact'],
#                 appointment_data['appointment_time'],
#                 'scheduled'
#             ))
#             appointment_id = cur.lastrowid
#             conn.commit()
#         conn.close()
#         return appointment_id
#     except Exception as e:
#         raise Exception(f"Failed to save appointment to database: {str(e)}")

# def get_appointments_from_db():
#     """Get all appointments from TiDB"""
#     try:
#         conn = get_db_connection()
#         with conn.cursor(pymysql.cursors.DictCursor) as cur:
#             cur.execute("SELECT * FROM appointments ORDER BY created_at DESC")
#             appointments = cur.fetchall()
#         conn.close()
#         return appointments
#     except Exception as e:
#         print(f"Error fetching appointments: {str(e)}")
#         return []

# def generate_local_confirmation(citizen_name: str, service: str, appointment_time: str, appointment_id: int) -> str:
#     """Generate confirmation message"""
#     return (
#         f"Hello {citizen_name}, your appointment for {service} has been booked successfully!\n"
#         f"Appointment ID: {appointment_id}\n"
#         f"Date & Time: {appointment_time}\n"
#         f"Please arrive 10 minutes early.\n"
#         "Thank you for using Medicura-AI Booking Service!"
#     )

# def send_confirmation(contact: str, message: str):
#     """Simulate sending confirmation (print to console)"""
#     print(f"\n=== SENDING CONFIRMATION TO {contact} ===")
#     print(message)
#     print("=== CONFIRMATION SENT ===\n")

# def book_appointment(citizen_name: str, service: str, contact: str) -> Tuple[Dict[str, Any], str]:
#     """
#     Booking Agent:
#     - Assigns random appointment time
#     - Saves data to TiDB
#     - Sends confirmation
#     """
#     try:
#         # Generate appointment time (next 1-7 days, between 9 AM - 5 PM)
#         appointment_time = datetime.now() + timedelta(
#             days=random.randint(1, 7),
#             hours=random.randint(9, 16)  # 9 AM to 4 PM
#         )
#         appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M:%S")

#         # Create appointment data
#         appointment_data = {
#             "citizen_name": citizen_name,
#             "service": service,
#             "contact": contact,
#             "appointment_time": appointment_time_str
#         }

#         # Save to TiDB
#         appointment_id = save_appointment_to_db(appointment_data)
        
#         # Generate confirmation message
#         confirmation = generate_local_confirmation(citizen_name, service, appointment_time_str, appointment_id)
        
#         # Add appointment ID to returned data
#         appointment_data["appointment_id"] = appointment_id
#         appointment_data["status"] = "scheduled"

#         # Send confirmation (simulated)
#         send_confirmation(contact, confirmation)

#         return appointment_data, confirmation

#     except Exception as e:
#         raise Exception(f"Booking failed: {str(e)}")

# # Initialize table when module is imported
# init_appointments_table()

# # -----------------------
# # CLI / Standalone testing
# if __name__ == "__main__":
#     print("=== Booking Agent (TiDB) ===\n")

#     name = input("Enter citizen name: ")
#     service = input("Enter service (e.g., Cardiology, Dermatology): ")
#     contact = input("Enter contact info: ")

#     try:
#         form, msg = book_appointment(name, service, contact)

#         print("\n--- Appointment Details ---")
#         print(form)
#         print("\n--- Confirmation Message ---")
#         print(msg)
        
#         # Show all appointments
#         print("\n--- All Appointments ---")
#         all_appointments = get_appointments_from_db()
#         for apt in all_appointments:
#             print(apt)
            
#     except Exception as e:
#         print(f"Error: {str(e)}")



import random
from datetime import datetime, timedelta
import pymysql
import os
from typing import Tuple, Dict, Any

# TiDB Configuration
DB_CONFIG = {
    "host": os.getenv("TIDB_HOST", "gateway01.us-west-2.prod.aws.tidbcloud.com"),
    "port": 4000,
    "user": os.getenv("TIDB_USERNAME", "34oY1b3G6arXWAM.root"),
    "password": os.getenv("TIDB_PASSWORD", "M9iWYjgizxiiT1qh"),
    "database": os.getenv("TIDB_DATABASE", "test"),
    "charset": "utf8mb4",
    "ssl": {"ssl_mode": "VERIFY_IDENTITY"}
}

def get_db_connection():
    """Establish connection to TiDB"""
    try:
        return pymysql.connect(**DB_CONFIG)
    except Exception as e:
        raise Exception(f"Database connection failed: {str(e)}")

def init_appointments_table():
    """Check if appointments table exists with correct structure"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Check table structure
            cur.execute("DESCRIBE appointments")
            columns = [col[0] for col in cur.fetchall()]
            print(f"📊 Existing table columns: {columns}")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error checking table: {str(e)}")
        return False

def save_appointment_to_db(appointment_data: Dict[str, Any]) -> int:
    """Save appointment to TiDB using EXISTING table structure"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            # Use EXISTING column names from your table
            cur.execute("""
                INSERT INTO appointments (patient_name, doctor_name, appointment_time, notes)
                VALUES (%s, %s, %s, %s)
            """, (
                appointment_data['citizen_name'],  # maps to patient_name
                f"Dr. for {appointment_data['service']}",  # maps to doctor_name
                appointment_data['appointment_time'],
                f"Service: {appointment_data['service']}, Contact: {appointment_data['contact']}"  # maps to notes
            ))
            appointment_id = cur.lastrowid
            conn.commit()
        conn.close()
        return appointment_id
    except Exception as e:
        raise Exception(f"Failed to save appointment: {str(e)}")

def generate_local_confirmation(citizen_name: str, service: str, appointment_time: str, appointment_id: int) -> str:
    """Generate confirmation message"""
    return (
        f"Hello {citizen_name}, your appointment for {service} has been booked successfully!\n"
        f"Appointment ID: {appointment_id}\n"
        f"Date & Time: {appointment_time}\n"
        f"Please arrive 10 minutes early.\n"
        "Thank you for using Medicura-AI!"
    )

def send_confirmation(contact: str, message: str):
    """Simulate sending confirmation"""
    print(f"\n=== CONFIRMATION ===\n{message}\n===================\n")

def book_appointment(citizen_name: str, service: str, contact: str) -> Tuple[Dict[str, Any], str]:
    """Book appointment and save to EXISTING database table"""
    try:
        # Generate appointment time
        appointment_time = datetime.now() + timedelta(
            days=random.randint(1, 7),
            hours=random.randint(9, 16)
        )
        appointment_time_str = appointment_time.strftime("%Y-%m-%d %H:%M:%S")

        # Create appointment data
        appointment_data = {
            "citizen_name": citizen_name,
            "service": service,
            "contact": contact,
            "appointment_time": appointment_time_str
        }

        # Save to database (using existing table structure)
        appointment_id = save_appointment_to_db(appointment_data)
        
        # Generate confirmation
        confirmation = generate_local_confirmation(citizen_name, service, appointment_time_str, appointment_id)
        
        # Add ID to response
        appointment_data["appointment_id"] = appointment_id
        appointment_data["status"] = "scheduled"

        # Send confirmation
        send_confirmation(contact, confirmation)

        return appointment_data, confirmation

    except Exception as e:
        raise Exception(f"Booking failed: {str(e)}")

def view_all_appointments():
    """View all appointments in database"""
    try:
        conn = get_db_connection()
        with conn.cursor(pymysql.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM appointments ORDER BY created_at DESC")
            appointments = cur.fetchall()
        conn.close()
        
        print("\n=== ALL APPOINTMENTS ===")
        for apt in appointments:
            print(f"ID: {apt['id']}, Patient: {apt['patient_name']}, "
                  f"Doctor: {apt['doctor_name']}, Time: {apt['appointment_time']}")
        print("=======================\n")
        return appointments
    except Exception as e:
        print(f"Error viewing appointments: {e}")
        return []

# Initialize and check table
if init_appointments_table():
    print("✅ Appointments table is ready!")

# Test
if __name__ == "__main__":
    print("=== Booking Agent (Using Existing Table) ===\n")
    
    # Test booking
    try:
        name = input("Enter citizen name: ").strip() or "Test Patient"
        service = input("Enter service: ").strip() or "General Checkup"
        contact = input("Enter contact: ").strip() or "0300-1234567"
        
        print(f"\n--- Booking for {name} ---")
        form, msg = book_appointment(name, service, contact)
        print("✅ Booking Successful!")
        print(f"Appointment ID: {form['appointment_id']}")
        
        # View all appointments
        view_all_appointments()
        
    except Exception as e:
        print(f"❌ Error: {e}")
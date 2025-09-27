import pymysql
import os

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

def test_db_connection():
    """Test database connection and table structure"""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print("✅ Database connection successful")
        
        with conn.cursor() as cur:
            # Check if appointments table exists
            cur.execute("SHOW TABLES LIKE 'appointments'")
            table_exists = cur.fetchone()
            
            if table_exists:
                print("✅ Appointments table exists")
                # Check table structure
                cur.execute("DESCRIBE appointments")
                columns = cur.fetchall()
                print("📊 Table structure:")
                for col in columns:
                    print(f"  {col[0]} - {col[1]}")
            else:
                print("❌ Appointments table does not exist")
                # Create the table
                cur.execute("""
                    CREATE TABLE appointments (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        citizen_name VARCHAR(255) NOT NULL,
                        service VARCHAR(255) NOT NULL,
                        contact VARCHAR(255) NOT NULL,
                        appointment_time DATETIME NOT NULL,
                        status VARCHAR(50) DEFAULT 'scheduled',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                print("✅ Appointments table created successfully")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_db_connection()
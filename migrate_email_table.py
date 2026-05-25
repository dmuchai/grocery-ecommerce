import pymysql
from config import Config
import sys

def migrate_email_queue():
    print("🚀 Starting Email Queue Migration...")
    
    # Connect to database using PyMySQL directly to handle schema changes
    try:
        # Parse connection details from Config or .env
        # Simple parsing for standard URI: mysql+pymysql://user:pass@host/db
        db_user = Config.DATABASE_USER
        db_password = Config.DATABASE_PASSWORD
        db_host = Config.DATABASE_HOST
        db_name = Config.DATABASE_NAME
        
        print(f"Connecting to {db_host}/{db_name} as {db_user}...")
        
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with conn.cursor() as cursor:
            # Check if table exists
            cursor.execute("SHOW TABLES LIKE 'email_queue'")
            result = cursor.fetchone()
            
            if result:
                print("⚠️ Table 'email_queue' already exists. Skipping creation.")
            else:
                print("Creating 'email_queue' table...")
                sql = """
                CREATE TABLE email_queue (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    order_id INT NOT NULL,
                    email_type VARCHAR(50) NOT NULL,
                    recipient VARCHAR(255) NOT NULL,
                    status VARCHAR(20) DEFAULT 'pending',
                    attempts INT DEFAULT 0,
                    last_error TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    sent_at DATETIME,
                    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
                cursor.execute(sql)
                print("✅ Table 'email_queue' created successfully.")
                
        conn.commit()
        conn.close()
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_email_queue()

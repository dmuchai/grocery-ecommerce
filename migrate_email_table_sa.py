from app import app
from models import db
from sqlalchemy import text

def migrate_email_queue_sqlalchemy():
    print("🚀 Starting Email Queue Migration (SQLAlchemy)...")
    
    with app.app_context():
        try:
            # Create connection from the existing engine
            with db.engine.connect() as conn:
                # Check if table exists
                result = conn.execute(text("SHOW TABLES LIKE 'email_queue'"))
                if result.fetchone():
                    print("⚠️ Table 'email_queue' already exists. Skipping.")
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
                    conn.execute(text(sql))
                    conn.commit()
                    print("✅ Table 'email_queue' created successfully.")
                    
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    migrate_email_queue_sqlalchemy()

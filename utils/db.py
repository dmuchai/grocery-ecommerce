def get_db_connection():
    conn = sqlite3.connect('instance/grocery.db')
    conn.row_factory = sqlite3.Row
    return conn

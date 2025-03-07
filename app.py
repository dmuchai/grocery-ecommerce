from flask import Flask, render_template, request, jsonify
import pymysql
import os

app = Flask(__name__)

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "Denncathy@1078")  # Replace with a secure env variable
DB_NAME = os.getenv("DB_NAME", "grocery_db")

# Ensure the database connection is established per request
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_products():
    query = request.args.get('q', '').strip().lower()

    # Open a new database connection per request
    try:
        with get_db_connection() as db:
            with db.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM products WHERE name LIKE %s OR description LIKE %s",
                    (f"%{query}%", f"%{query}%")
                )
                results = cursor.fetchall()

        return jsonify({"products": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return an error message if the query fails

if __name__ == "__main__":
    app.run(debug=True)

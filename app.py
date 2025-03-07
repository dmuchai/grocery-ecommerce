from flask import Flask, render_template, request, jsonify
import pymysql

app = Flask(__name__)

# Database connection
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Denncathy@1078",
    database="grocery_db",
    cursorclass=pymysql.cursors.DictCursor  # Ensures results are dictionaries
)
cursor = db.cursor()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET"])
def search_products():
    query = request.args.get('q', '').strip().lower()
    
    # Execute raw SQL query using pymysql
    cursor.execute("SELECT * FROM products WHERE name LIKE %s OR description LIKE %s", (f"%{query}%", f"%{query}%"))
    results = cursor.fetchall()  # Fetch results as a list of dictionaries

    return jsonify({"products": results})  # Return an OBJECT `{ "products": [...] }`

if __name__ == "__main__":
    app.run(debug=True)

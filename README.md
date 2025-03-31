🛒 Denncathy Fresh Basket
An API-driven grocery e-commerce platform built with Flask & MySQL

📌 The Story Behind This Project
It all started with a simple question:
❝ Why is it so hard to buy fresh groceries online in local markets? ❞

Most online grocery platforms are either too expensive or don't cater to everyday shoppers who just need affordable, fresh, and locally sourced produce. As a software engineer, I wanted to explore how an API-driven web service could power a simple, fast, and efficient grocery shopping experience.

This project is part of my ALX Software Engineering Portfolio—a chance to build something real while deepening my skills in backend development, database management, and front-end integration.

🎯 Goals & Technical Challenges
🔹 Seamless Cart Experience: No page reloads when adding/removing items 🛒
🔹 Dynamic Search & Filtering: Instant product suggestions from a MySQL-powered API 🔍
🔹 Efficient Order Management: Orders persist across user sessions
🔹 Responsive UI: Accessible across desktop and mobile devices 📱💻
🔹 Scalable Backend: Built with Flask + SQLAlchemy to handle future growth

One of the biggest challenges was session management for guest users. Since users don’t need to log in to shop, I had to uniquely track carts per session while allowing future authentication.

🚀 Tech Stack
🔹 Backend: Flask (Python) + Flask-RESTful for API
🔹 Database: MySQL + SQLAlchemy ORM
🔹 Frontend: HTML, CSS (Bootstrap), JavaScript (jQuery)
🔹 API & AJAX: Fetching product data dynamically using fetch()
🔹 Session Handling: Flask-Session with UUID-based session tracking
🔹 Hosting & Deployment: GitHub Pages (Landing Page) & Render.com (Backend API)

📸 Screenshots & Walkthrough
🛍️ Homepage: Browse Groceries

🛒 Cart: Instant Updates (No Page Reloads!)

📝 Order History: Track Past Purchases

💡 Architecture & Data Flow
This project follows an MVC (Model-View-Controller) pattern, ensuring separation of concerns:

1️⃣ Frontend (View): Handles user interactions with Bootstrap & JavaScript.
2️⃣ API (Controller): Flask routes process requests and return JSON data.
3️⃣ Database (Model): MySQL stores products, cart items, and orders.

🗂️ Database Schema (Simplified)
sql
Copy
Edit
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10,2),
    image_url VARCHAR(255),
    stock INT
);

CREATE TABLE cart (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id VARCHAR(36),
    product_id INT,
    quantity INT,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    total_price DECIMAL(10,2),
    status ENUM('pending', 'completed', 'canceled'),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
🔄 API Endpoints
Method	Endpoint	Description
GET	/api/products	Fetch all products
POST	/api/cart/add	Add an item to cart
GET	/api/cart	Retrieve cart contents
POST	/api/order	Place an order
GET	/api/orders	View order history
All endpoints return JSON responses, enabling a fully dynamic user experience.

🛠️ Local Setup & Installation
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/yourusername/grocery-ecommerce.git
cd grocery-ecommerce
2️⃣ Set Up a Virtual Environment
sh
Copy
Edit
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate  # Windows
3️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
4️⃣ Set Up the Database
sh
Copy
Edit
flask db upgrade
5️⃣ Run the Application
sh
Copy
Edit
flask run
Your app will be live at:

cpp
Copy
Edit
http://127.0.0.1:5000
⚡ Challenges & Lessons Learned
🚧 Cart Synchronization: Keeping cart items persistent across different sessions was tricky.
💡 Solution: Used Flask-Session to store cart data per session and migrate it once a user logs in.

🚧 AJAX + Flask Integration: Had issues where the API was returning HTML instead of JSON.
💡 Solution: Ensured API routes used @app.route('/cart/', methods=['GET']) with return jsonify(cart_data).

🚧 Deployment Bugs: Flask static files weren’t loading on Render.com due to caching issues.
💡 Solution: Appended a UUID query string (?v={{ uuid }}) to force cache refresh.

🎯 Next Steps & Future Features
✅ Mobile Optimization: Improve UI for better mobile shopping experience 📱
✅ Authentication & User Profiles: Enable user accounts with saved addresses 🏠
✅ Payment Gateway Integration: Add M-Pesa and Stripe support for real transactions 💳
✅ Product Recommendations: Implement AI-based recommendations based on user history 🤖

📜 License
This project is licensed under the MIT License – Feel free to fork, modify, and contribute!

🤝 Contributing
Want to make this project even better? 🎉

Fork the repository

Create a feature branch (git checkout -b feature-xyz)

Commit your changes (git commit -m "Added xyz feature")

Push to GitHub (git push origin feature-xyz)

Submit a Pull Request! 🚀

📢 Connect With Me
💼 LinkedIn: Dennis Muchai
📂 GitHub: @dmuchai
📝 Blog Post: Read about this project here

🎉 Thank You for Checking Out Denncathy Fresh Basket!
If you found this project helpful, please give it a ⭐ on GitHub! 🚀

import requests 
import os
print(os.listdir())

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import create_tables

# ---------------- APP INIT ----------------
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
    return response

# ---------------- DB ----------------
create_tables()

def connect_db():
    return sqlite3.connect("food.db")

# ---------------- TEST ROUTE (IMPORTANT) ----------------
@app.route('/')
def home():
    return "Server Working ✅"

# ---------------- AUTH ----------------

@app.route('/register', methods=['POST','OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (name, email, password, role)
    VALUES (?, ?, ?, ?)
    """, (data['name'], data['email'], data['password'], data['role']))

    conn.commit()
    conn.close()

    return jsonify({"message": "Registered Successfully"})


@app.route('/login', methods=['POST','OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return '', 200

    data = request.json

    email = data.get("email")
    password = data.get("password")

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Login Success",
            "role": user[4]
        })

    return jsonify({"message": "Invalid Credentials"}), 401

# ---------------- FOOD ----------------

@app.route('/add_food', methods=['POST'])
def add_food():
    data = request.json
    location = data.get('location', 'Unknown')
    data = request.json

    lat, lng = None, None  # safe default

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO food (name, quantity, location, expiry, lat, lng)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (data['name'], data['quantity'], data['location'], data['expiry'], lat, lng))

    conn.commit()
    conn.close()

    return jsonify({"message": "Food Added"})


@app.route('/get_food', methods=['GET'])
def get_food():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food")
    data = cursor.fetchall()

    food_list = []
    for row in data:
        food_list.append({
            "id": row[0],
            "name": row[1],
            "quantity": row[2],
            "location": row[3],
            "expiry": row[4],
            "lat": row[5],
            "lng": row[6]
        })

    conn.close()
    return jsonify(food_list)


@app.route('/delete_food/<int:id>', methods=['DELETE'])
def delete_food(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM food WHERE id=?", (id,))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Food Deleted"})


@app.route('/filter_food/<location>', methods=['GET'])
def filter_food(location):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM food WHERE location=?", (location,))
    rows = cursor.fetchall()

    conn.close()
    return jsonify(rows)

# ---------------- NGO REQUEST ----------------

@app.route('/request_food', methods=['POST'])
def request_food():
    data = request.json

    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO requests (food_id, ngo_name, status)
    VALUES (?, ?, ?)
    """, (data['food_id'], data['ngo_name'], "Pending"))

    conn.commit()
    conn.close()

    return jsonify({"message": "Request Sent"})


@app.route('/get_requests', methods=['GET'])
def get_requests():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM requests")
    data = cursor.fetchall()

    conn.close()
    return jsonify(data)


@app.route('/approve/<int:id>', methods=['POST'])
def approve(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE requests SET status='Approved' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Approved"})

# ---------------- CHATBOT ----------------

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_msg = data.get('message', '').lower()

    if "hello" in user_msg or "hi" in user_msg:
        reply = "Hello 👋 I am Waste2Worth AI Assistant. How can I help you?"

    elif "food" in user_msg and "available" in user_msg:
        reply = "🍱 You can view available food in the Available Food page."

    elif "food" in user_msg:
        reply = "You can request food using the button."

    elif "ngo" in user_msg:
        reply = "🤝 NGOs can request food using the Request Food button."

    elif "expiry" in user_msg:
        reply = "⏳ Food is prioritized based on expiry time."

    elif "map" in user_msg:
        reply = "📍 You can view food locations in the Map section."

    elif "deliver" in user_msg:
        reply = "✅ Click Delivered button to mark as completed."

    elif "help" in user_msg:
        reply = "🆘 Ask me about food, NGO, expiry, or map."

    else:
        reply = "🤖 Sorry, I didn't understand."

    return jsonify({"reply": reply})

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(debug=True)
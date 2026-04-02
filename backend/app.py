from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3, jwt, pickle

app = Flask(__name__)
CORS(app)

SECRET = "secret123"

# Load AI model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# DB init
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users(email TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS history(email TEXT, message TEXT, result TEXT)")
    conn.commit()
    conn.close()

init_db()

# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)", (data['email'], data['password']))
    conn.commit()
    conn.close()
    return jsonify({"msg": "User created"})

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (data['email'], data['password']))
    user = c.fetchone()

    if user:
        token = jwt.encode({"email": data['email']}, SECRET, algorithm="HS256")
        return jsonify({"token": token})

    return jsonify({"error": "Invalid login"})

# Predict
@app.route("/predict", methods=["POST"])
def predict():
    token = request.headers.get("Authorization")
    user = jwt.decode(token, SECRET, algorithms=["HS256"])

    msg = request.json['message']
    vec = vectorizer.transform([msg])
    pred = model.predict(vec)[0]

    result = "Spam 🚨" if pred == 1 else "Not Spam ✅"

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (?,?,?)", (user['email'], msg, result))
    conn.commit()
    conn.close()

    return jsonify({"result": result})

# History
@app.route("/history", methods=["GET"])
def history():
    token = request.headers.get("Authorization")
    user = jwt.decode(token, SECRET, algorithms=["HS256"])

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT message, result FROM history WHERE email=?", (user['email'],))
    data = c.fetchall()
    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
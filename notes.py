from flask import Flask, jsonify, request
import pymysql.cursors
import ssl
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Set up the MySQL connection
ssl_context = ssl.create_default_context(
    cafile="path/to/BaltimoreCyberTrustRoot.crt.pem"
)
db = pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl=ssl_context,
    cursorclass=pymysql.cursors.DictCursor,
)

# Read operation
@app.route("/data", methods=["GET"])
def get_data():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM table_name")
        result = cursor.fetchall()
        cursor.close()
        data = []
        for row in result:
            data.append({"id": row["id"], "name": row["name"], "age": row["age"]})
        return jsonify(data), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


# Insert operation
@app.route("/data", methods=["POST"])
def add_data():
    try:
        cursor = db.cursor()
        data = request.get_json()
        name = data["name"]
        age = data["age"]
        query = "INSERT INTO table_name (name, age) VALUES (%s, %s)"
        values = (name, age)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return jsonify({"status": "success"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


# Delete operation
@app.route("/data/<int:id>", methods=["DELETE"])
def delete_data(id):
    try:
        cursor = db.cursor()
        query = "DELETE FROM table_name WHERE id = %s"
        value = (id,)
        cursor.execute(query, value)
        db.commit()
        cursor.close()
        return jsonify({"status": "success"}), 204
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


# Update operation
@app.route("/data/<int:id>", methods=["PUT"])
def update_data(id):
    try:
        cursor = db.cursor()
        data = request.get_json()
        name = data["name"]
        age = data["age"]
        query = "UPDATE table_name SET name = %s, age = %s WHERE id = %s"
        values = (name, age, id)
        cursor.execute(query, values)
        db.commit()
        cursor.close()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

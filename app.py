from flask import Flask, jsonify, request
import pymysql
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Set up logging
logging.basicConfig(filename="app.log", level=logging.INFO)

# Set up the MySQL connection
db = pymysql.connect(
    host=os.environ.get("DB_HOST"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    database=os.environ.get("DB_NAME"),
    ssl={"ca": "./DigiCertGlobalRootCA.crt.pem"},
    cursorclass=pymysql.cursors.DictCursor,
)


@app.route("/")
def index():
    return jsonify({"message": "Welcome to the 'My Library' API"}), 200


# Read operation (get all records)
@app.route("/books", methods=["GET"])
def get_books():
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM books")
        result = cursor.fetchall()
        cursor.close()
        books = []
        for row in result:
            books.append(
                {
                    "book_id": row["book_id"],
                    "library_user": row["library_user"],
                    "title": row["title"],
                    "author": row["author"],
                    "pages": row["pages"],
                    "isbn": row["isbn"],
                    "book_type": row["book_type"],
                    "date_read": row["date_read"],
                    "genre": row["genre"],
                    "format": row["format"],
                    "source": row["source"],
                    "evaluation": row["evaluation"],
                    "created_date": row["created_date"],
                    "modified_date": row["modified_date"],
                }
            )
        logging.info("Successfully retrieved data from database")
        return jsonify(books), 200
    except Exception as e:
        db.rollback()
        logging.error("Error occurred while retrieving data from database: %s", str(e))
        return jsonify({"error": str(e)}), 500


# Read operation (get one record)
@app.route("/book/<int:id>", methods=["GET"])
def get_book(id):
    try:
        cursor = db.cursor()
        query = "SELECT * FROM books WHERE book_id = %s"
        value = (id,)
        cursor.execute(query, value)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500


# Insert operation
@app.route("/books", methods=["POST"])
def add_book():
    try:
        cursor = db.cursor()
        book = request.get_json()

        library_user = book["library_user"]
        title = book["title"]
        author = book["author"]
        pages = book["pages"]
        isbn = book["isbn"]
        book_type = book["book_type"]
        date_read = book["date_read"]
        genre = book["genre"]
        format = book["format"]
        source = book["source"]
        evaluation = book["evaluation"]

        query = "INSERT INTO books (library_user, title, author, pages, isbn, book_type, date_read, genre, format, source, evaluation ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            library_user,
            title,
            author,
            pages,
            isbn,
            book_type,
            date_read,
            genre,
            format,
            source,
            evaluation,
        )
        cursor.execute(query, values)

        db.commit()
        cursor.close()
        logging.info("Successfully inserted data into database")
        return jsonify({"status": "success"}), 201

    except Exception as e:
        db.rollback()
        logging.error("Error occurred while inserting data into database: %s", str(e))
        return jsonify({"error": str(e)}), 500


# # Delete operation
# @app.route("/data/<int:id>", methods=["DELETE"])
# def delete_data(id):
#     try:
#         cursor = db.cursor()
#         query = "DELETE FROM table_name WHERE id = %s"
#         value = (id,)
#         cursor.execute(query, value)
#         db.commit()
#         cursor.close()
#         logging.info("Successfully deleted data from database")
#         return jsonify({"status": "success"}), 204
#     except Exception as e:
#         db.rollback()
#         logging.error("Error occurred while deleting data from database: %s", str(e))
#         return jsonify({"error": str(e)}), 500


# # Update operation
# @app.route("/data/<int:id>", methods=["PUT"])
# def update_data(id):
#     try:
#         cursor = db.cursor()
#         data = request.get_json()
#         name = data["name"]
#         age = data["age"]
#         query = "UPDATE table_name SET name = %s, age = %s WHERE id = %s"
#         values = (name, age, id)
#         cursor.execute(query, values)
#         db.commit()
#         cursor.close()
#         logging.info("Successfully updated data in database")
#         return jsonify({"status": "success"}), 200
#     except Exception as e:
#         db.rollback()
#         logging.error("Error occurred while updating data in database: %s", str(e))
#         return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

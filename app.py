from flask import Flask, jsonify, request
import pymysql
from dotenv import load_dotenv
import os

# import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

# Set up logging
# logging.basicConfig(filename="app.log", level=logging.INFO)

# Get environment varaibles
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_password = os.environ.get("DB_PASSWORD")
db_database = os.environ.get("DB_NAME")

# Set up MySQL connection config
db_config = {
    "host": db_host,
    "user": db_user,
    "password": db_password,
    "db": db_database,
    "ssl_ca": "./DigiCertGlobalRootCA.crt.pem",
    "cursorclass": pymysql.cursors.DictCursor,
}


@app.route("/api/v1/")
def index():
    return jsonify({"message": "Welcome to the 'My Library' API"}), 200


# Read operation (get all records)
@app.route("/api/v1/book", methods=["GET"])
def get_books():
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        cur.execute("SELECT * FROM books;")
        result = cur.fetchall()
        cur.close()

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
        # logging.info("Successfully retrieved data from database")

        return jsonify(books), 200
    except Exception as e:
        conn.rollback()
        # logging.error("Error occurred while retrieving data from database: %s", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            cur.close()
            print("MySQL cursor is closed")
            conn.close()
            print("MySQL connection is closed")


# Read operation (get one record)
@app.route("/api/v1/book/<int:id>", methods=["GET"])
def get_book(id):
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

        query = "SELECT * FROM books WHERE book_id = %s"
        value = (id,)

        cur.execute(query, value)
        result = cur.fetchone()
        cur.close()

        if result:
            return jsonify(result), 200
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            cur.close()
            print("MySQL cursor is closed")
            conn.close()
            print("MySQL connection is closed")


# Insert operation
@app.route("/api/v1/book", methods=["POST"])
def add_book():
    try:
        conn = pymysql.connect(**db_config)
        cur = conn.cursor()

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
        cur.execute(query, values)

        conn.commit()
        cur.close()
        # logging.info("Successfully inserted data into database")
        return jsonify({"status": "success"}), 201

    except Exception as e:
        db.rollback()
        # logging.error("Error occurred while inserting data into database: %s", str(e))
        return jsonify({"error": str(e)}), 500

    finally:
        if conn:
            cur.close()
            print("MySQL cursor is closed")
            conn.close()
            print("MySQL connection is closed")


# Delete operation
@app.route("/api/v1/book/<int:id>", methods=["DELETE"])
def delete_book(id):
    if id is None:
        print("No book ID provided")
        return jsonify({"error": "Book ID is required"}), 400
    if request.method == "DELETE":
        print("Processing delete request")
        # logging.info("Deleting book_id: " + id)
        try:
            conn = pymysql.connect(**db_config)
            cur = conn.cursor()

            query = "DELETE FROM books WHERE book_id = %s"
            book_id = id
            # logging.info(query + value)
            print(query, book_id)

            cur.execute(query, (book_id,))
            conn.commit()
            # cur.close()
            print("Record deleted successfully.")
            # logging.info("Successfully deleted data from database")
            return jsonify({"status": "success"}), 204

        except Exception as e:
            conn.rollback()
            print("error in delete")
            print(str(e))
            # logging.error(
            #     "Error occurred while deleting data from database: %s", str(e)
            # )
            return jsonify({"error": str(e)}), 500

            # except mysql.connector.Error as error:
            #     print("Failed to Delete record from table: {}".format(error))
        finally:
            if conn:
                cur.close()
                print("MySQL cursor is closed")
                conn.close()
                print("MySQL connection is closed")
    else:
        print("Method not allowed")
        return jsonify({"error": "Method not allowed"}), 405

    # TODO: implment update operation
    # TODO: change to mysql.connector?
    # TODO: add finally to close cursor and connection to other methods
    # TODO: change to conn = pymysql.connect(**db_config)
    # TODO: add logging & figure out how to view them


# # Update operation
# @app.route("/api/v1/book/<int:id>", methods=["PUT"])
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

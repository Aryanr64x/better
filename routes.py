# routes.py
from flask import Blueprint, jsonify, request
from auth import generate_token, is_authenticated
import sqlite3

app = Blueprint('routes', __name__)

@app.route('/auth', methods=['POST'])
def login():
    token = generate_token()
    return jsonify({"token": token})

@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    if request.method == 'GET':
        search = request.args.get('search', '') 
        page = int(request.args.get('page', 1))  
        items_per_page = 10                      

        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()

        if search:
            query = """
            SELECT * FROM books 
            WHERE title LIKE ? OR author LIKE ? 
            LIMIT ? OFFSET ?;
            """
            print(search)
            params = (f"%{search}%", f"%{search}%", items_per_page, (page - 1) * items_per_page)
        else:
            query = "SELECT * FROM books LIMIT ? OFFSET ?;"
            params = (items_per_page, (page - 1) * items_per_page)

        cursor.execute(query, params)
        books = cursor.fetchall()
        conn.close()

        result = [
            {"id": row[0], "title": row[1], "author": row[2], "available": row[3]}
            for row in books
        ]
        return jsonify(result)
    elif request.method == 'POST':
        if not is_authenticated(request.headers.get('Authorization')):
            return jsonify({"error": "Unauthorized"}), 403

        data = request.json
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author) VALUES (?, ?)', (data['title'], data['author']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Book added successfully"}), 201

@app.route('/books/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def book_operations(id):
    if not is_authenticated(request.headers.get('Authorization')):
        return jsonify({"error": "Unauthorized"}), 403

    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()

    if request.method == 'GET':
        cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = cursor.fetchone()
        conn.close()
        if book:
            return jsonify(book)
        return jsonify({"error": "Book not found"}), 404

    elif request.method == 'PUT':
        data = request.json

        cursor.execute('SELECT * FROM books WHERE id = ?', (id,))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            return jsonify({"error": "Book not found"}), 404 
        
        cursor.execute('UPDATE books SET title = ?, author = ?, available = ? WHERE id = ?',
                    (data['title'], data['author'], data['available'], id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Book updated successfully"}), 200

    elif request.method == 'DELETE':
        cursor.execute('DELETE FROM books WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "Book deleted successfully"})

@app.route('/members', methods=['GET', 'POST'])
def manage_members():
    if request.method == 'GET':
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members')
        members = cursor.fetchall()
        conn.close()
        return jsonify(members)

    elif request.method == 'POST':
        data = request.json
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO members (name, email) VALUES (?, ?)', (data['name'], data['email']))
        conn.commit()
        conn.close()
        return jsonify({"message": "Member added successfully"}), 201

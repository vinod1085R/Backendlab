from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# SQLite database
DATABASE = os.path.join(os.path.dirname(__file__), "students.db")


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# CREATE - Add Student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()

    name = data['name']
    email = data['email']
    course = data['course']

    conn = get_db_connection()

    conn.execute(
        "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
        (name, email, course)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student added successfully"
    }), 201


# READ - Get All Students
@app.route('/students', methods=['GET'])
def get_students():
    conn = get_db_connection()

    students = conn.execute(
        "SELECT * FROM students"
    ).fetchall()

    conn.close()

    result = []

    for student in students:
        result.append({
            "id": student["id"],
            "name": student["name"],
            "email": student["email"],
            "course": student["course"]
        })

    return jsonify(result), 200


# UPDATE - Update Student
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    data = request.get_json()

    name = data['name']
    email = data['email']
    course = data['course']

    conn = get_db_connection()

    conn.execute(
        """UPDATE students
           SET name = ?, email = ?, course = ?
           WHERE id = ?""",
        (name, email, course, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student updated successfully"
    }), 200


# DELETE - Delete Student
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    conn = get_db_connection()

    conn.execute(
        "DELETE FROM students WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Student deleted successfully"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)
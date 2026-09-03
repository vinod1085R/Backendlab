from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vinodR1085'
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)


# ---------------- UPDATE STUDENT ----------------
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "message": "Request body is required."
            }), 400

        name = data.get("name")
        email = data.get("email")
        phone = data.get("phone")

        if not name or not email or not phone:
            return jsonify({
                "success": False,
                "message": "Name, Email and Phone are required."
            }), 400

        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cur.fetchone()

        if not student:
            cur.close()
            return jsonify({
                "success": False,
                "message": "Student not found."
            }), 404

        cur.execute("""
            UPDATE students
            SET name=%s, email=%s, phone=%s
            WHERE id=%s
        """, (name, email, phone, id))

        mysql.connection.commit()

        cur.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cur.fetchone()
        cur.close()

        return jsonify({
            "success": True,
            "message": "Student updated successfully.",
            "data": {
                "id": student[0],
                "name": student[1],
                "email": student[2],
                "phone": student[3]
            }
        }), 200

    except Exception as e:
        mysql.connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ---------------- DELETE STUDENT ----------------
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM students WHERE id=%s", (id,))
        student = cur.fetchone()

        if not student:
            cur.close()
            return jsonify({
                "success": False,
                "message": "Student not found."
            }), 404

        cur.execute("DELETE FROM students WHERE id=%s", (id,))
        mysql.connection.commit()

        cur.close()

        return jsonify({
            "success": True,
            "message": "Student deleted successfully."
        }), 200

    except Exception as e:
        mysql.connection.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
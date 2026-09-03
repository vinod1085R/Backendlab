from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vinodR1085'
app.config['MYSQL_DB'] = 'flask_crud'

mysql = MySQL(app)


# ---------------- GET ALL STUDENTS ----------------

@app.route('/students', methods=['GET'])
def get_students():
    try:
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM students")

        students = cur.fetchall()

        cur.close()

        data = []

        for student in students:
            data.append({
                "id": student[0],
                "name": student[1],
                "email": student[2],
                "phone": student[3]
            })

        return jsonify({
            "success": True,
            "message": "Students retrieved successfully.",
            "count": len(data),
            "data": data
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------- INSERT STUDENT ----------------

@app.route('/students', methods=['POST'])
def insert_student():
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

        cur.execute(
            "INSERT INTO students(name,email,phone) VALUES(%s,%s,%s)",
            (name, email, phone)
        )

        mysql.connection.commit()

        student_id = cur.lastrowid

        cur.execute(
            "SELECT * FROM students WHERE id=%s",
            (student_id,)
        )

        student = cur.fetchone()

        cur.close()

        return jsonify({
            "success": True,
            "message": "Student added successfully.",
            "data": {
                "id": student[0],
                "name": student[1],
                "email": student[2],
                "phone": student[3]
            }
        }), 201

    except Exception as e:
        mysql.connection.rollback()

        print(str(e))

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500


# ---------------- RUN ----------------

if __name__ == '__main__':
    app.run(debug=True)
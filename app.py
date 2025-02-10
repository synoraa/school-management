from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Connect to MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",  # Change this if your MySQL user is different
    password="Enroll@2527",
    database="school_management"
)
cursor = db.cursor(dictionary=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/students')
def students_page():
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    return render_template('students.html', students=students)

@app.route('/teachers')
def teachers_page():
    cursor.execute("SELECT * FROM teachers")
    teachers = cursor.fetchall()
    return render_template('teachers.html', teachers=teachers)

@app.route('/courses')
def courses_page():
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    return render_template('courses.html', courses=courses, students=students)

@app.route('/assign_student', methods=['POST'])
def assign_student():
    student_id = request.form['student_id']
    course_id = request.form['course_id']

    try:
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (%s, %s)", (student_id, course_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    return redirect('/courses')

@app.route('/assign_batch', methods=['POST'])
def assign_batch():
    teacher_id = request.form['teacher_id']
    batch_name = request.form['batch_name']

    try:
        cursor.execute("INSERT INTO batches (teacher_id, batch_name) VALUES (%s, %s)", (teacher_id, batch_name))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return redirect('/teachers')

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']

    try:
        cursor.execute("INSERT INTO students (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return redirect('/students')

@app.route('/add_course', methods=['POST'])
def add_course():
    name = request.form['name']
    description = request.form['description']
    teacher_id = request.form['teacher_id'] if request.form['teacher_id'] else None

    try:
        cursor.execute("INSERT INTO courses (name, description, teacher_id) VALUES (%s, %s, %s)",
                       (name, description, teacher_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return redirect('/courses')

@app.route('/add_teacher', methods=['POST'])
def add_teacher():
    name = request.form['name']
    email = request.form['email']

    try:
        cursor.execute("INSERT INTO teachers (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

    return redirect('/teachers')



if __name__ == '__main__':
    app.run(debug=True)

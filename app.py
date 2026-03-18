from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    attendance = request.form['attendance']
    fees = request.form['fees']

    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    # Table create
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        name TEXT,
        email TEXT,
        attendance INTEGER,
        fees TEXT
    )
    """)

    # Insert data
    cur.execute("INSERT INTO students VALUES (?, ?, ?, ?)",
                (name, email, attendance, fees))

    conn.commit()
    conn.close()

    return "Student Added Successfully ✅"


@app.route('/students')
def show_students():
    conn = sqlite3.connect('students.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM students")
    data = cur.fetchall()

    conn.close()

    return render_template('students.html', students=data)

app.run(debug=True)
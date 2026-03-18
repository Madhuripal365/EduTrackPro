import smtplib
from email.mime.text import MIMEText




from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def send_email(to_email, name):
    sender_email = "palmadhuri784@gmail.com"
    password = "ovuxkltzeipxwyps"

    subject = "Student Added Successfully"
    body = f"Hello {name},\n\nYou have been successfully added to EduTrackPro."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error:", e)



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
    send_email(email, name)

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

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

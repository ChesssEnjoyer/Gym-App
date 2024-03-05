from flask import Flask, render_template
import mysql.connector

app = Flask(__name__)

# Function to fetch data from MySQL database
def get_options_from_database():
    # Connect to MySQL database
    conn = mysql.connector.connect(host='localhost', user='root', password='', database='exercises')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT Ex_name FROM exercises")
    options = cursor.fetchall()

    # Close database connection
    cursor.close()
    conn.close()

    return options

@app.route('/')
def index():
    options = get_options_from_database()

    return render_template('index.html', options=options)

if __name__ == '__main__':
    app.run(debug=True)

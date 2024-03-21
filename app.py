from flask import Flask, render_template, request, jsonify
import mysql.connector
from joblib import load
import numpy as np

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

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    #load ai models
    train_split = load('models/training_split.sav')
    day = load('models/actual_days.sav')

    #load informations from form
    gender = request.form.get('gender')
    workout_days = request.form.get('daysPerWeek')
    experience = request.form.get('experienceLevel')
    exercises = request.form.getlist('options')

    #create data for ai model to work
    data = [[]]
    data[0].append(workout_days)    
    data[0].append(experience)    

    #Use ai model to get split that satisfies requirements 
    train_result = train_split.predict(data)
    splits = []
    if train_result == 0:
        splits.append('Fullbody')
        print(splits[0])
        data[0].append('0')
    elif train_result == 1:
        splits.append('PPl-Arnold')
        print(splits[0])
        data[0].append('1')
    elif train_result == 2:
        splits.append('Push-Pull-Legs')
        print(splits[0])
        data[0].append('2')
    else: 
        splits.append('Upper-Lower')
        print(splits[0])
        data[0].append('3')

    #create data for ai model to work
    day_data = [[]]
    day_data[0].append(data[0][0])
    day_data[0].append(data[0][2])
    
    #Use ai model to get actuall working days that satisfies requirements
    day_result = day.predict(day_data)
    if day_result == 1:
        data[0].append('1')
    elif day_result == 2:
        data[0].append('2')
    elif day_result == 3:
        data[0].append('3')
    elif day_result == 4:
        data[0].append('4')
    elif day_result == 5:
        data[0].append('5')
    elif day_result == 6:
        data[0].append('6')
    print(data)

    return render_template('generated.html', splits = splits, day_result = data[0][3])
if __name__ == '__main__':
    app.run(debug=True)

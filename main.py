from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)

# SQLite3 database connection
# conn = sqlite3.connect('./db.sqlite3')
# print("Opened database successfully")

# # Create users table if it does not exist
# conn.execute('''CREATE TABLE IF NOT EXISTS users (
#    userid INTEGER PRIMARY KEY,
#    email TEXT UNIQUE,
#    name TEXT,
#    password TEXT
# );''')
# print("Users table created successfully")

# # Create applications table if it does not exist
# conn.execute('''CREATE TABLE IF NOT EXISTS applications (
#    email_code TEXT PRIMARY KEY,
#    company_name TEXT,
#    position_name TEXT,
#    status TEXT,
#    userid INTEGER,
#    FOREIGN KEY (userid) REFERENCES users(userid)
# );''')
print("Applications table created successfully")

# API endpoint for user registration
@app.route('/register', methods=['POST'])
@cross_origin()
def register():
    
    conn = sqlite3.connect('./db.sqlite3')
    print("Opened database successfully")
    data = request.get_json()
    email = data['email']
    name = data['name']
    password = data['password']
    
    try:
        conn.execute("INSERT INTO users (email, name, password) VALUES (?, ?, ?)", (email, name, password))
        conn.commit()
        response = jsonify({'message': 'Registration successful.','email':email,'name':name}), 201
        return response
    except sqlite3.IntegrityError as e:
         response = jsonify({'error': 'User with this email already exists.'}), 400
         return response

# API endpoint for user login
@app.route('/login', methods=['POST'])
@cross_origin()
def login(): 
    conn = sqlite3.connect('./db.sqlite3')
    print("Opened database successfully")
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    cursor = conn.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = cursor.fetchone()
    print(user)
    
    if user:
        response = jsonify({'message': 'Login successful.','email':email,'name':user[2]}), 200
        return response
    else:
        response = jsonify({'error': 'Invalid email or password.'}), 401
        return response
    
@app.route('/get_applications', methods=['POST'])
@cross_origin()
def get_applications():
    # Retrieve the email address from the request body
    email = request.json['email']
    
    # Connect to the database
    conn = sqlite3.connect('./db.sqlite3')
    c = conn.cursor()
    
    # Retrieve the user ID based on the email address
    c.execute('SELECT userid FROM users WHERE email=?', (email,))
    result = c.fetchone()
    
    if not result:
        # If the user does not exist, return a 404 error
        response = jsonify({'error': 'User not found'}), 404
        return response
    
    # Retrieve the applications data based on the user ID
    userid = result[0]
    c.execute('SELECT company_name, position_name, status FROM applications WHERE userid=?', (userid,))
    applications = c.fetchall()
    
    # Close the database connection
    conn.close()
    
    # Return the applications data as JSON
    response = jsonify({'applications': applications})
    return response

if __name__ == '__main__':
    app.run(debug=True)

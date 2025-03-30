from flask import Flask, render_template, request, redirect,session,url_for
import mysql.connector
from datetime import date


today = date.today()



app = Flask(__name__)

# Database connection function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="leave_db"
    )

# Home Page (Display Users)
@app.route("/")
def index():
    return render_template("index.html")



# Add User
@app.route("/add_user", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    emp_number = request.form["emp_number"]
    password = request.form["password"]
    birthday = request.form["birthday"]
    

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (name, email,emp_number,password,date_birth) VALUES (%s, %s, %s, %s, %s)", (name, email, emp_number, password, birthday))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return redirect("/")

@app.route("/login_user", methods=["POST", "GET"])

def login_user():
    if request.method == "POST":
        username_input = request.form.get("emp_number").strip()  # Strip spaces from the input
        password_input = request.form.get("password").strip()  # Strip spaces from the input
        
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
    
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.execute("SELECT * FROM leaves ")
        leaves = cursor.fetchall()
        
        query = """
                SELECT leaves.*, users.name, users.emp_number
                FROM leaves
                JOIN users ON leaves.user_id = users.id
                """
        cursor.execute(query)
        leve_info = cursor.fetchall()
        today = date.today()

        
    
        for user in users:
            if username_input == user['emp_number'] and password_input == user['password']:
               
                cursor.execute("SELECT * FROM leaves where user_id= %s",( user["id"],))
                leaves = cursor.fetchall()
                
                cursor.close()
                conn.close()
                return render_template("dashboard.html",  name =user["name"], user_id= user["id"],leaves=leaves,date_birth=user["date_birth"],users=users,today=today,leve_info=leve_info,emp_number = user["emp_number"])  # Make sure the path is correct for your template
                
        # If no match found, return to the login page
        cursor.close()
        conn.close()
        return redirect("/")  # Redirect to the login page if credentials are incorrect
    
    return "Invalid method. Please use POST."

@app.route("/add_leave", methods=["POST", "GET"])    
def add_leave():
    user_id = request.form["user_id"]
    leave_type = request.form["leave_type"]
    leave_catogory = request.form["leave_catogory"]
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    reason = request.form["reason"]
    

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO leaves (user_id,leave_type, leave_catogory,start_date,end_date,reason) VALUES (%s, %s, %s, %s, %s, %s)", (user_id,leave_type, leave_catogory,start_date,end_date,reason))
    conn.commit()
    
    cursor.close()
    conn.close()
    
    return redirect("/")


@app.route("/log_out", methods=["POST"])
def log_out():

    return redirect(url_for('index'))  # Redirect to the homepage or index page

# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)

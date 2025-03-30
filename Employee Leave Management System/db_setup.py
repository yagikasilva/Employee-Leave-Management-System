import mysql.connector

# Connect to MySQL (XAMPP)
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # Default XAMPP MySQL user
    password=""   # No password for XAMPP by default
)

cursor = conn.cursor()

# Create database
cursor.execute("CREATE DATABASE IF NOT EXISTS leave_db")
cursor.execute("USE leave_db")

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100),
        emp_number VARCHAR(10),
        password VARCHAR(50),
        date_birth DATE,
        created_TIME TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    );
    CREATE TABLE IF NOT EXISTS leaves (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        leave_type VARCHAR(50) NOT NULL,
        leave_catogory VARCHAR(50) NOT NULL,
        reason VARCHAR(255) NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE NOT NULL,
        status VARCHAR(20) DEFAULT 'Pending', -- e.g., Pending, Approved, Rejected
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
""")

print("Database and table created successfully!")

# Close connection
cursor.close()
conn.close()

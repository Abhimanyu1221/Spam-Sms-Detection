import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

DB_HOST = "192.168.16.1"
DB_NAME = "ty55"
DB_USER = "your_db_user"
DB_PASSWORD = "your_db_password"

def connect_db():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def register_user(username, email, password):
    """Registers a new user with hashed password."""
    conn = connect_db()
    cur = conn.cursor()
    hashed_pw = generate_password_hash(password)
    try:
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                    (username, email, hashed_pw))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False
    finally:
        cur.close()
        conn.close()

def validate_user(email, password):
    """Validates login credentials."""
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT id, username, password FROM users WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    
    if user and check_password_hash(user[2], password):
        return {"id": user[0], "username": user[1]}
    return None


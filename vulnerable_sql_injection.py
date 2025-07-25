import sqlite3

# Create a connection to the database
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

# Create a users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Insert some dummy data
cursor.execute("INSERT INTO users (username, password, email) VALUES ('admin', 'password1', 'admin@email.com')")
cursor.execute("INSERT INTO users (username, password, email) VALUES ('user', 'password2', 'user@email.com')")
conn.commit()

def register(username, password, email):
    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{password}', '{email}')"
    try:
        cursor.execute(query)
        conn.commit()
        print("User registered successfully!")
    except sqlite3.IntegrityError:
        print("User registration failed. Username might already exist.")

def login(username, password):
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print("Login successful!")
    else:
        print("Invalid username or password.")

def update_email(username, new_email):
    query = f"UPDATE users SET email = '{new_email}' WHERE username = '{username}'"
    cursor.execute(query)
    conn.commit()
    print("Email updated successfully!")

def search_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        print(f"User found: {result}")
    else:
        print("User not found.")

if __name__ == "__main__":
    while True:
        print("\n1. Register\n2. Login\n3. Update Email\n4. Search User\n5. Exit")
        choice = input("Enter your choice: ")
        
        if choice == '1':
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            email = input("Enter email: ")
            register(user, pwd, email)
        elif choice == '2':
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            login(user, pwd)
        elif choice == '3':
            user = input("Enter username: ")
            new_email = input("Enter new email: ")
            update_email(user, new_email)
        elif choice == '4':
            user = input("Enter username to search: ")
            search_user(user)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

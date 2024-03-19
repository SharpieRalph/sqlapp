import psycopg2
from psycopg2 import sql

# Function to establish a connection to the database
def connect():
    try:
        conn = psycopg2.connect(
            host= "localhost",
            database= "assignment3",
            user= "postgres",
            password= 1112,
            port= 5432
        )
        print("Connection to PostgreSQL database successful!")
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL database:", error)
        return None

# Function to insert initial data into the students table
def populateTable(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
            """, ('John', 'Doe', 'john.doe@example.com', '2023-09-01'))
            cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, ('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'))
            cursor.execute("""
            INSERT INTO students (first_name, last_name, email, enrollment_date)
            VALUES (%s, %s, %s, %s)
        """, ('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02'))
            connection.commit()
    except Error as e:
        print("Error inserting initial data:", e)

# Function to get all students from the students table
def get_all_students(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            records = cursor.fetchall()

            # Print the records
            for record in records:
                print(record)
    except Error as e:
        print("Error fetching students:", e)

# Function to add a new student to the students table
def add_student(connection, first_name, last_name, email, enrollment_date):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id, first_name, last_name, email, enrollment_date;
            """, (first_name, last_name, email, enrollment_date))

            # Fetch the newly inserted record
            new_student = cursor.fetchone()

            # Print the new student record
            print('\nNew Student:', new_student)

            connection.commit()
    except Error as e:
        print("Error adding student:", e)

# Function to update a student's email by student_id
def update_student_email(connection, student_id, new_email):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE students
                SET email = %s
                WHERE student_id = %s
                RETURNING student_id, first_name, last_name, email, enrollment_date;
            """, (new_email, student_id))

            # Fetch the updated student record
            updated_student = cursor.fetchone()

            # Print the updated student record
            print('\nUpdated Student:', updated_student)

            connection.commit()
    except Error as e:
        print("Error updating student email:", e)

# Function to delete a student by student_id
def delete_student(connection, student_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE student_id = %s RETURNING student_id, first_name, last_name, email, enrollment_date;", (student_id,))

            # Fetch the deleted student record
            deleted_student = cursor.fetchone()

            # Print the deleted student record
            print('\nDeleted Student:', deleted_student)

            connection.commit()
    except Error as e:
        print("Error deleting student:", e)


connection = connect()
populateTable(connection)
   

# Function to validate the email format
def is_valid_email(email):
    # Implement your email validation logic here
    return '@' in email  # Example: Basic validation

# Define the switch-like function to handle user commands based on numeric choice
def handle_command(choice, connection):
    try:
        if choice == 1:
            print("All students:")
            get_all_students(connection)
        elif choice == 2:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            email = input("Enter email: ")
            if not is_valid_email(email):
                raise ValueError("Invalid email format")
            enrollment_date = input("Enter enrollment date (YYYY-MM-DD): ")
            add_student(connection, first_name, last_name, email, enrollment_date)
            print("Student added successfully.")
        elif choice == 3:
            student_id = input("Enter student ID: ")
            new_email = input("Enter new email: ")
            if not is_valid_email(new_email):
                raise ValueError("Invalid email format")
            update_student_email(connection, student_id, new_email)
            print("Email updated successfully.")
        elif choice == 4:
            student_id = input("Enter student ID to delete: ")
            delete_student(connection, student_id)
            print("Student deleted successfully.")
        elif choice == 5:
            return False
        else:
            print("Invalid choice. Please try again.")
    except ValueError as ve:
        print("Error:", ve)
    except Exception as e:
        print("An error occurred:", e)
    return True

def main(connection):
    while True:
        print("\nAvailable commands:")
        print("1 -> Get all students")
        print("2 -> Add a new student")
        print("3 -> Update student email")
        print("4 -> Delete a student")
        print("5 -> Exit")

        try:
            choice = int(input("\nEnter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # Handle user command
        if not handle_command(choice, connection):
            break

# Call the main function with the database connection
main(connection)

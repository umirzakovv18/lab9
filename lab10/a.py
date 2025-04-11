import psycopg2
import csv

def connect():
    return psycopg2.connect(
        dbname="umirzakovvayat",
        user="postgres",
        password="rootroot", 
        host="localhost"
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (row['name'], row['phone']))
    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from CSV.")

def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, phone) VALUES (%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("Data inserted from console.")

def update_entry():
    field = input("What do you want to update? (name/phone): ")
    if field == "name":
        old_phone = input("Enter phone to identify user: ")
        new_name = input("Enter new name: ")
        query = "UPDATE phonebook SET name = %s WHERE phone = %s"
        values = (new_name, old_phone)
    elif field == "phone":
        old_name = input("Enter name to identify user: ")
        new_phone = input("Enter new phone: ")
        query = "UPDATE phonebook SET phone = %s WHERE name = %s"
        values = (new_phone, old_name)
    else:
        print("Invalid field.")
        return
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, values)
    conn.commit()
    cur.close()
    conn.close()
    print("Data updated.")

def query_data():
    print("1 - Show all\n2 - Filter by name\n3 - Filter by phone (starts with)")
    choice = input("Your choice: ")
    conn = connect()
    cur = conn.cursor()
    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        name = input("Enter name: ")
        cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
    elif choice == "3":
        phone_start = input("Enter starting digits: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (phone_start + "%",))
    else:
        print("Invalid choice.")
        return
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_entry():
    method = input("Delete by (name/phone): ")
    conn = connect()
    cur = conn.cursor()
    if method == "name":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
    elif method == "phone":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid method.")
        return
    conn.commit()
    cur.close()
    conn.close()
    print("Data deleted.")

def main():
    create_table()
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1 - Insert from CSV")
        print("2 - Insert from console")
        print("3 - Update entry")
        print("4 - Query data")
        print("5 - Delete entry")
        print("0 - Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "2":
            insert_from_console()
        elif choice == "3":
            update_entry()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_entry()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
import psycopg2

# --- Connection ---
def connect():
    return psycopg2.connect(
        dbname="umirzakovvayat",
        user="postgres",
        password="rootroot1",
        host="localhost"
    )

# --- Search by pattern ---
def search_by_pattern(pattern):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_phonebook(%s)", (pattern,))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# --- Insert or update single user ---
def insert_or_update_user(name, phone):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("User inserted or updated.")

# --- Bulk insert with validation ---
def bulk_insert_users(users):
    names = [user[0] for user in users]
    phones = [user[1] for user in users]
    conn = connect()
    cur = conn.cursor()

    # Use a DO block to call the procedure and capture the OUT parameter
    cur.execute("""
        DO $$
        DECLARE
            result text[];
        BEGIN
            CALL bulk_insert_users(%s, %s, result);
            RAISE NOTICE '%%', result;
        END
        $$;
    """, (names, phones))

    print("Bulk insert called. Check pgAdmin NOTICE logs for invalid entries.")
    conn.commit()
    cur.close()
    conn.close()

# --- Get paginated data ---
def get_paginated(limit, offset):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM get_paginated_data(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)
    cur.close()
    conn.close()

# --- Delete by name or phone ---
def delete_by(name=None, phone=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute("CALL delete_user(%s, %s)", (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print("User deleted if existed.")

# --- Main menu to test ---
def main():
    while True:
        print("\n--- PhoneBook Advanced Menu ---")
        print("1 - Search by pattern")
        print("2 - Insert or update user")
        print("3 - Bulk insert")
        print("4 - Get paginated data")
        print("5 - Delete by name or phone")
        print("0 - Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            pattern = input("Enter pattern to search: ")
            search_by_pattern(pattern)

        elif choice == "2":
            name = input("Enter name: ")
            phone = input("Enter phone: ")
            insert_or_update_user(name, phone)

        elif choice == "3":
            n = int(input("How many users to insert? "))
            users = []
            for _ in range(n):
                name = input("Name: ")
                phone = input("Phone: ")
                users.append((name, phone))
            bulk_insert_users(users)

        elif choice == "4":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            get_paginated(limit, offset)

        elif choice == "5":
            name = input("Enter name (leave blank if deleting by phone): ") or None
            phone = input("Enter phone (leave blank if deleting by name): ") or None
            delete_by(name, phone)

        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()

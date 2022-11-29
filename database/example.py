import sqlite3
import re

con = sqlite3.connect('details.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS users (userId text primary key, name text, email text, salary int, edited int)")

con.close()

def add_new_details(userId, name, email, salary, edited):
    con = sqlite3.connect('details.db')
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
        (userId, name, email, salary, edited ))
    # cur.execute("INSERT INTO TABLE_NAME VALUES (value1, value2, value3, value4)")
    con.commit()
    con.close()

def get_user_details(email):
    try:
        con = sqlite3.connect('details.db')
        cur = con.cursor()
        cur.execute('''
            SELECT * FROM users WHERE email=?''',
            (email,))
        row = cur.fetchall()
        print(len(row))
        if row is None:
            return True
        else:
            return row
    finally:
        con.close()

def update_details(email, val):
    try:
        con = sqlite3.connect('details.db')
        cur = con.cursor()
        cur.execute('''
            UPDATE users SET edited = edited + ?, name = ?  WHERE email=?''',
            (10, "TG", email))
        con.commit()
        row = cur.fetchall()
        print(len(row))
        if row is None:
            return True
        else:
            return row
    finally:
        con.close()



# add_new_details(1, 'shivani', 'sks@lmu.edu', 1000, 1000)
# add_new_details(2, 'Gowda', 'sks@lmu.edu', 2000, 2000)
update_details('sks@lmu.edu', 20)
# add_new_details(3, 'tg', 'tg@lmu.edu', 'mars')
print(get_user_details('sks@lmu.edu'))
# table_name_pattern = re.compile(r"(?<=into )(.*)(?= values)")
# matches = table_name_pattern.finditer("INSERT INTO users(userId, name, email, salary) VALUES (1, Shivani, sks@lmu.edu, 100 )")
# for match in matches:
#     table_name_match = match
#     print(table_name_match.group(0))

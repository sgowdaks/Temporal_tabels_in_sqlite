import sqlite3

from excecute import execute

class Database:
    def __init__(self, query):
        self.con = sqlite3.connect('details.db')
        self.cur = self.con.cursor()
        self.query = query
        self.input(self.query)

    def input(self, query):
        execute(query, self.cur, self.con)


# k = execute("CREATE TABLE users (userId text primary key, name text, email text, salary text save)", cur, con)
# k = execute("INSERT INTO users VALUES (1, 'sherry', 'sks@lion.lmu.edu', 1000)", cur, con)
# k = execute("INSERT INTO users VALUES (2, 'shivani', 's@lion.lmu.edu', 2000)", cur, con)        
# k = execute("UPDATE INTO users SET salary = 2000, name = 'TG' WHERE email = 'sks@lion.lmu.edu'", cur, con)
# k = execute("UPDATE INTO users SET salary = 3000 WHERE email = 'sks@lion.lmu.edu'", cur, con)
# k = execute("DELETE FROM users WHERE email = 'sks@lion.lmu.edu'", cur, con) 
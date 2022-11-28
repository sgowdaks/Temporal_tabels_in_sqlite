import sqlite3

con = sqlite3.connect('user_details.db')
cur = con.cursor()

from datetime import date

class execute:
    def __init__(self, query, con, cur):
        self.query = query
        self.con = con
        self.editing_key = ""
        self.dicti = {}
        self.index = 0
        self.cur = cur
        self.check_for_the_action(self.query)

    def check_for_the_action(self, query):
        print(query)
        query_ = query.split(" ")
        if "CREATE" in query_:
            self.create(query)

        elif "INSERT" in query_:
            self.insert(query)

        elif "UPDATE" in query_:
            self.update(query)
        
        # elif "SELECT" in query:
        #     self.select(query_)

        elif "DELETE" in query_:
            self.delete(query_)

        # elif "VIEW" in query_:
        #     self.view(query_)

    def create(self, query):
        #query = "CREATE TABLE users (userId text primary key, name text, email text, salary text save)"
        query_brackets = query.split("(")
        first_part = query_brackets[0]
        second_part = query_brackets[1]
        tabel_name = first_part.split(" ")[2]
        extra_tabel_name = tabel_name + "_extra"
        extra = first_part.split(" ")
        extra = extra[:len(extra)-2]
        extra = " ".join(extra) + " " + extra_tabel_name
        second_part = second_part.strip(")")
        arr = second_part.split(" ")
        arr = second_part.split(" ")
        if "save" in arr:
            editing_key = arr[len(arr) - 2]
            new_col =  self.editing_key+ "_update text " 
            new = "," + new_col
            arr.append(new)
            arr = " ".join(arr)
            arr_ = first_part + "(" + arr + ")"
            self.con.execute(arr_)
            arr_ = extra + "(" + arr + ")"
            self.con.execute(extra + "(" + arr + ")")
            #create_extra_database(arr)
        else:
            print("handel the error")
        # self.con.close()

    def insert(self, query, bo = False):
        if bo == True:
            print("hello")
        query = query.split("(")
        tabel_name = query[0].split(" ")[2]
        second = query[1].strip(")").strip('"').strip(" ").split(",")
        

        n = len(second)
        question = ""
        tup = []
        extra = ""
        for i in range(n):
            if question == "":
                question += "?"
                tup.append(eval(second[i]))
            else:
                question += ", ?"
                if i == n - 1:
                   tup.append(second[i])
                else:
                    tup.append(eval(second[i]))
            if i == n-1:
                extra = second[i]
        if bo == False:
            question += ", ?"
            today = date.today()
            d1 = today.strftime("%d/%m/%Y")
            tup.append(extra +":" + d1 + "|")
        str_ = "INSERT INTO " + tabel_name + " VALUES (" + question + ")" 
        self.con.execute(str_, tuple(tup))
        self.cur.commit()
       
    def update(self, query):
        # cur.execute("UPDATE users set salary = ? WHERE email=?", (int(amount), email))
        #"UPDATE INTO users set salary = 2000 WHERE email='sks@lion.lmu.edu')"
        query = query.split(" ")
        q = "select * from " + query[2]
        cursor = con.execute(q)
        names = list(map(lambda x: x[0], cursor.description))
        target = names[-2]
        target_update = names[-1]

        #if there are updating last to second column
        where  = query.index("WHERE")
        set_ = query.index("SET")
        set_part = query[set_+ 1: where]
        where_part = query[where+1:]

        def make_dicti(dicti, updated, list1):
            prev = ""
            e = ""
            keys = ""
            for col in updated:
                if prev == "" and e == "":
                    prev = col
                    if keys == "":
                        keys = col + " = " + " ? " 
                    else:
                        keys += " , " + col + " = " + " ? "  
                elif prev != "" and col == "=":
                    e = "="
                elif prev != "" and e == "=":
                    col = col.strip(',')
                    dicti[prev] = col.strip(',')
                    prev = ""
                    e = ""
                    list1.append(eval(col))
            return dicti, keys, list1

        dicti1 = {}
        dicti1, keys1, list1 = make_dicti(dicti1, set_part, list1 = [])
        dicti2 = {}
        dicti2, keys2, list1 = make_dicti(dicti2, where_part, list1)
                
        if target in dicti1.keys():
            #the main key is modified
            keys1 += ", " + target_update + " = " +  target_update + "|| ?"
            q = "UPDATE " + query[2] + " SET " + keys1 + " WHERE " + keys2 
            new = str(dicti1['salary'])
            today = date.today()
            new = new + ":" + str(today.strftime("%d/%m/%Y")) + "|"
            list1.insert(len(dicti1), new)
            print(q, tuple(list1))
            self.con.execute(q, tuple(list1))

        else: 
            #the main key is not modified
            q = "UPDATE " + query[2] + " SET " + keys1 + " WHERE " + keys2 
            self.con.execute(q, tuple(list1))

        self.cur.commit()
        # self.cur.close()
        
    def delete(self, query):
        #delete the key
        #DELETE FROM users WHERE email='sks@lion.lmu.edu')"
        #cur.execute("DELETE FROM users WHERE email=?", (int(amount),))
        tabel_name = query[2]
        where  = query.index("WHERE")
        where_part = query[where+1:]

        def make_dicti(dicti, updated, list1):
            prev = ""
            e = ""
            keys = ""
            for col in updated:
                if prev == "" and e == "":
                    prev = col
                    if keys == "":
                        keys = col + " = " + " ? " 
                    else:
                        keys += " , " + col + " = " + " ? "  
                elif prev != "" and col == "=":
                    e = "="
                elif prev != "" and e == "=":
                    dicti[prev] = col
                    prev = ""
                    e = ""
                    list1.append(eval(col))
            return dicti, keys, list1
        
        dicti1 = {}
        dicti1, keys1, list1 = make_dicti(dicti1, where_part, list1 = [])

        q = "SELECT * FROM " + tabel_name + " WHERE " + keys1
        self.insert_into_extra_database(q, list1, tabel_name)

        q = "DELETE FROM " + tabel_name + " WHERE " + keys1 
        cur.execute(q, tuple(list1))
        self.cur.commit()
        # self.cur.close()

    def insert_into_extra_database(self, q, vals, tabel_name):
        extra_tabel_name = tabel_name + "_extra"
        cur.execute(q, tuple(vals))
        con.commit()
        rows = cur.fetchall()
        one = cur.fetchone()
        query = "INSERT INTO " + extra_tabel_name + " VALUES " 
        list1 = []
        for row in rows:
            for i, val in enumerate(row):
                list1.append(val.strip(" "))
            list1[-1] = list1[-1].strip(",")
            query = query + str(tuple(list1))
            self.insert(query, True)
            
    # def view(self, query):
        
k = execute("CREATE TABLE users (userId text primary key, name text, email text, salary text save)", cur, con)
k = execute("INSERT INTO users VALUES (1, 'sherry', 'sks@lion.lmu.edu', 1000)", cur, con)
k = execute("INSERT INTO users VALUES (2, 'shivani', 's@lion.lmu.edu', 2000)", cur, con)        
k = execute("UPDATE INTO users SET salary = 2000, name = 'TG' WHERE email = 'sks@lion.lmu.edu'", cur, con)
k = execute("UPDATE INTO users SET salary = 3000 WHERE email = 'sks@lion.lmu.edu'", cur, con)
k = execute("DELETE FROM users WHERE email = 'sks@lion.lmu.edu'", cur, con) 




    



    

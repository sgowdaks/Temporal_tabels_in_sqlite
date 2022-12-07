# Temporal_tabels_in_sqlite
Implementing temporal tabels in sqlite 

* To start the project do `git clone git@github.com:sgowdaks/Temporal_tabels_in_sqlite.git`.
* Open python shell by typing `python`.
* Import Database class from main `from main import Database`.
* Enter the query.ex: `Database("CREATE TABLE users (userId text primary key, name text, email text, salary text save)")`

### Things to note:
* The project is in the primitive state, and only work for CREATE, INSERT, UPDATE and DELETE. You have to follow the exact syntax as listed below 
  * 
    * CREATE: Database("CREATE TABLE users (userId text primary key, name text, email text, salary text save)")
  * INSERT: Database("INSERT INTO users VALUES (1, 'sherry', 'sks@lion', 1000)")
  * UPDATE: Database("UPDATE INTO users SET salary = 2000, name = 'sherry' WHERE email = 'sks@lion'")
  * DELETE: Database("DELETE FROM users WHERE email = 'sks@lion'")
  
 



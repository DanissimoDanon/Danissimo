import sqlite3

from sqlite3 import Error
con = sqlite3.connect('database.db')

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE IF NOT EXISTS employees(id integer PRIMARY KEY, name text, salary int)")


    con.commit()
def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM employes')

    rows = cursorObj.fetchall()

    for row in rows:

        print(row)


sql_table(con)
for i in range (10,15):
    t = int(i)
    con.cursor().execute(f"INSERT INTO employees VALUES(?, ?, ?)",(t,"user",9))
    con.commit()

import sqlite3

con=sqlite3.connect("jarvis.db")
cursor = con.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(100))"
cursor.execute(query)



# query = "INSERT INTO sys_command VALUES (null, , )"
# cursor.execute(query)
# con.commit()

query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(100))"
cursor.execute(query)

query = "INSERT INTO sys_command VALUES (null,'perplexity' ,'https://www.perplexity.ai' )"
cursor.execute(query)
con.commit()
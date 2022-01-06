import sqlite3

connection = sqlite3.connect('./data/data.sqlite') # no dir atual cria ou conecta
cur = connection.cursor() # como se fosse o open dos arquivos normais

cur.execute('DROP TABLE IF EXISTS Subjects') # Linguagem SQL, Remove Tracks se já existir
cur.execute('CREATE TABLE Subjects (name TEXT, type TEXT)') # Column 1, column 2

cur.execute('DROP TABLE IF EXISTS Types')
cur.execute('CREATE TABLE Types (name TEXT)')

connection.close()

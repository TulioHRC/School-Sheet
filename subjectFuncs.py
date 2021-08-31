import sqlite3
import pandas as pd
from tkinter import messagebox

def seeSubjects():
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        data = {
            'name': [],
            'type': [],
        }

        cur.execute('SELECT name, type FROM Subjects')
        for row in cur:
            data['name'].append(row[0])
            data['type'].append(row[1])
        
        df = pd.DataFrame(data=data)

        cur.close()

        return df
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Não foi possível vizualizar as matérias do banco de dados. \nErro: {e}')
        return 'Error'

def addSubject(name, type):
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        cur.execute('INSERT INTO Subjects (name, type) VALUES (?, ?)', (name, type))
        con.commit()  

        cur.close()
        messagebox.showinfo('Succeed', f'A matéria "{name}" de {type} foi salva!\nPara atualizar os dados reinicie o applicativo.')
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Houve um erro ao tentar inserir a matéria "{name}" no banco de dados. \nErro: {e}')


def removeSubject(name):
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        cur.execute('DELETE FROM Subjects WHERE name=?',  (name,))
        con.commit()  

        cur.close()
        messagebox.showinfo('Succeed', f'A matéria "{name}" foi removida!\nPara atualizar os dados reinicie o applicativo.')
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Houve um erro ao tentar remover a matéria "{name}" do banco de dados. \nErro: {e}')
import sqlite3
import os
import sys
import pandas as pd
from tkinter import messagebox

def seeTypes():
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        data = {
            'name': [],
        }

        cur.execute('SELECT * FROM Types')
        for row in cur:
            data['name'].append(row[0])

        df = pd.DataFrame(data=data)

        cur.close()

        return df
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Não foi possível vizualizar os tipos do banco de dados. \nErro: {e}')
        return {}

def addType(name, app, main):
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        cur.execute('INSERT INTO Types (name) VALUES (?)', (name,))
        con.commit()

        cur.close()
        messagebox.showinfo('Succeed', f'O tipo "{name}" foi salvo!\nPara atualizar os dados reinicie o applicativo.')

        app.master.destroy()
        main()
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Houve um erro ao tentar inserir o tipo "{name}" no banco de dados. \nErro: {e}')


def removeType(name, app, main):
    try:
        con = sqlite3.connect('./data/data.sqlite')
        cur = con.cursor()

        cur.execute('DELETE FROM Types WHERE name=?',  (name,))
        con.commit()

        cur.close()
        messagebox.showinfo('Succeed', f'O tipo "{name}" foi removido!\nPara atualizar os dados reinicie o applicativo.')
        app.master.destroy()
        main()
    except Exception as e:
        print(e)
        messagebox.showerror('Erro', f'Houve um erro ao tentar remover o tipo "{name}" do banco de dados. \nErro: {e}')

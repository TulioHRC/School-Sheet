import pandas as pd
from datetime import date
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import *
from pandas import ExcelWriter
# Own Functions
from functions.excel import *
from functions.subjects import *

def application():
    df = seeSubjects()
    subs_norm = df[df["type"] == 'Médio'].name.values
    subs_tec = df[df["type"] == 'Técnico'].name.values

    class MainApp():
        def __init__(self, master):
            self.master = master
            self.master.title('Planilha de para casas')
            self.master.iconbitmap('./images/alarm.ico')

            self.title = Label(text="Para casas")
            self.title.configure(font=("Arial", 22))
            self.title.grid(row=0, column=1)

            Button(self.master, text="Config", command=config).grid(row=0, column=2, pady=5)

            self.tabs = ttk.Notebook(self.master)
            self.tabs.grid(row=1, column=0, columnspan=3)

            self.medio = Frame(self.tabs, width=465, height=200)
            self.tec = Frame(self.tabs, width=465, height=200)
            self.nothing = Frame(self.tabs, width=465, height=200)

            self.medio.pack(fill='both', expand=True)
            self.tec.pack(fill='both', expand=True)
            self.nothing.pack(fill='both', expand=True)

            self.tabs.add(self.medio, text="Ensino Médio")
            self.tabs.add(self.tec, text="Ensino Técnico")
            self.tabs.add(self.nothing, text="")

            self.load_sheet(self.medio)
            self.load_sheet(self.tec)

            Button(self.master, text="Novo :(", command=newLevel).grid(row=2, column=0, pady=5)
            Button(self.master, text="Deletar :)", command=delLevel).grid(row=2, column=2, pady=5)

        def load_sheet(self, frame):
            med, tec = load_excel()

            if frame == self.medio: df = med.copy()
            else: df = tec.copy()

            # Referencee: https://gist.github.com/RamonWill/0686bd8c793e2e755761a8f20a42c762
            tv1 = ttk.Treeview(frame)
            # set the height and width of the widget to 100% of its container (frame1).
            tv1.place(relheight=1, relwidth=1)

            # command means update the yaxis view of the widget
            treescrolly = Scrollbar(frame, orient="vertical", command=tv1.yview)
            # command means update the xaxis view of the widget
            treescrollx = Scrollbar(frame, orient="horizontal", command=tv1.xview)
            # assign the scrollbars to the Treeview Widget
            tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
            # treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
            # make the scrollbar fill the y axis of the Treeview widget
            treescrolly.pack(side="right", fill="y")

            tv1["column"] = list(df.columns)
            tv1["show"] = "headings"
            for column in tv1["columns"]:
                # let the column heading = column name
                tv1.heading(column, text=column)
                tv1.column(column, minwidth=90, width=90, stretch=NO)

            df_rows = df.to_numpy().tolist()  # turns the dataframe into a list of lists
            for row in df_rows:
                # inserts each list into the treeview. For parameters see https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Treeview.insert
                tv1.insert("", "end", values=row)

        def reload_sheets(self):
            self.medio.destroy()
            self.tec.destroy()
            self.nothing.destroy()

            self.medio = Frame(self.tabs, width=450, height=200)
            self.tec = Frame(self.tabs, width=450, height=200)
            self.nothing = Frame(self.tabs, width=450, height=200)

            self.medio.pack(fill='both', expand=True)
            self.tec.pack(fill='both', expand=True)
            self.nothing.pack(fill='both', expand=True)

            self.tabs.add(self.medio, text="Ensino Médio")
            self.tabs.add(self.tec, text="Ensino Técnico")
            self.tabs.add(self.nothing, text="")

            self.load_sheet(self.medio)
            self.load_sheet(self.tec)


    class config(MainApp):
        def __init__(self):
            self.newScreen = Toplevel()
            self.newScreen.title("Configurações")
            self.newScreen.iconbitmap('./images/alarm.ico')

            self.tabs = ttk.Notebook(self.newScreen)
            self.tabs.grid(row=0, column=0, pady=2, columnspan=3)

            self.subjects = Frame(self.tabs, width=450, height=300)
            self.killSubjects = Frame(self.tabs, width=450, height=300)

            self.subjects.pack(fill='both', expand=True)
            self.killSubjects.pack(fill='both', expand=True)

            self.tabs.add(self.subjects, text="Adicionar Matérias")
            self.tabs.add(self.killSubjects, text="Remover Matérias")

            self.subjectsFrame()
            self.killSubjectsFrame()

        def subjectsFrame(self):
            Label(self.subjects, text="Name: ").grid(row=0, column=0, pady=5, padx=5)
            self.name = Entry(self.subjects)
            self.name.grid(row=0, column=1, pady=5, padx=5)

            Label(self.subjects, text="Type: ").grid(row=1, column=0, padx=2, pady=2)
            self.type = StringVar()
            self.type.set('Médio')
            self.t = OptionMenu(self.subjects, self.type, *["Médio", "Técnico"])
            self.t.grid(row=1, column=1)

            Button(self.subjects, text="Add Subject", command=lambda: addSubject(self.name.get(
            ), self.type.get(), app, application)).grid(row=2, column=0, columnspan=2, pady=5, padx=5)

        def killSubjectsFrame(self):
            materias = seeSubjects()

            Label(self.killSubjects, text="Name: ").grid(row=0, column=0, pady=5, padx=5)
            self.namek = StringVar()
            self.nk = OptionMenu(self.killSubjects, self.namek, *materias["name"].values)
            self.nk.grid(row=0, column=1)

            Button(self.killSubjects, text="Remove Subject", command=lambda: removeSubject(
                self.namek.get(), app, application)).grid(row=1, column=0, columnspan=2, pady=5, padx=5)


    class delLevel(MainApp):
        def __init__(self):
            self.newScreen = Toplevel()
            self.newScreen.title("Deletar para-casa")
            self.newScreen.iconbitmap('./images/alarm.ico')

            materias = seeSubjects()
            Label(self.newScreen, text="Matéria: ").grid(row=0, column=0, padx=2, pady=2)
            self.subject = StringVar()
            self.Options = OptionMenu(self.newScreen, self.subject, *materias["name"].values, command=self.changeL)
            self.Options.grid(row=0, column=1)

            Label(self.newScreen, text="Nome: ").grid(row=0, column=2, padx=2, pady=2)
            self.name = StringVar()
            self.n = OptionMenu(self.newScreen, self.name, "")
            self.n.grid(row=0, column=3)

            Button(self.newScreen, text="Deletar", command=self.delete).grid(row=1, column=1, padx=2, pady=2)

        def changeL(self, value):
            df = pd.read_excel(r"./Homework.xlsx")
            lista = df[df["Matéria"] == self.subject.get()]["Nome"].values
            self.n.destroy()
            self.n = OptionMenu(self.newScreen, self.name, *lista)
            self.n.grid(row=0, column=3)

        def delete(self):
            try:
                nome = self.name.get()
                materia = self.subject.get()

                df = pd.read_excel(r"./Homework.xlsx")
                df["Valor"] = df["Valor"].fillna("0")

                df = df[(df["Nome"] != nome) | (df["Matéria"] != materia)]

                writer = ExcelWriter('Homework.xlsx')
                df.to_excel(writer, header=True, index=False)
                writer.save()
                self.save()

                app.reload_sheets()
                self.newScreen.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror(
                    "Error", "Houve um erro na criação do para casa.")

        def save(self):
            nome = self.name.get()
            materia = self.subject.get()

            df = pd.read_excel(r"./Homework Did.xlsx")

            new_row = {'Nome': nome, 'Matéria': materia}
            df = df.append(new_row, ignore_index=True)

            writer = ExcelWriter('Homework Did.xlsx')
            df.to_excel(writer, header=True, index=False)
            writer.save()

            app.reload_sheets()


    class newLevel(MainApp):
        def __init__(self):
            self.newScreen = Toplevel()
            self.newScreen.title("Novo para-casa")
            self.newScreen.iconbitmap('./images/alarm.ico')

            Label(self.newScreen, text="Nome: ").grid(row=0, column=0, padx=2, pady=2)
            self.name = Entry(self.newScreen)
            self.name.grid(row=0, column=1, padx=2, pady=2)

            Label(self.newScreen, text="Tipo: ").grid(row=1, column=0, padx=2, pady=2)
            self.type = StringVar()
            self.type.set('Medio')
            self.types = OptionMenu(self.newScreen, self.type, *["Medio", "Tecnico"], command=self.changeOps)
            self.types.grid(row=1, column=1)

            Label(self.newScreen, text="Matéria: ").grid(row=2, column=0, padx=2, pady=2)
            self.subject = StringVar()
            self.Options = OptionMenu(self.newScreen, self.subject, *subs_norm)
            self.Options.grid(row=2, column=1)

            Label(self.newScreen, text="Valor: ").grid(row=0, column=2, padx=2, pady=2)
            self.val = Entry(self.newScreen)
            self.val.grid(row=0, column=3, padx=2, pady=2)

            Label(self.newScreen, text="Grupo: ").grid(row=1, column=2, padx=2, pady=2)
            self.group = StringVar()
            self.group.set('Nao')
            self.g = OptionMenu(self.newScreen, self.group, *["Nao", "Sim"])
            self.g.grid(row=1, column=3)

            act_date = str(date.today()).split("-")
            Label(self.newScreen, text="Prazo: ").grid(row=2, column=2, padx=2, pady=2)
            self.date = Calendar(self.newScreen, selectmode="day", year=int(
                act_date[0]), month=int(act_date[1]), day=int(act_date[2]))
            self.date.grid(row=2, column=3, padx=2, pady=2)

            Button(self.newScreen, text="Criar", command=self.create, width=20).grid(row=3, column=1)

        def changeOps(self, value):
            self.Options.destroy()
            if value == "Medio":
                self.Options = OptionMenu(self.newScreen, self.subject, *subs_norm)
                self.Options.grid(row=2, column=1)
            else:
                self.Options = OptionMenu(self.newScreen, self.subject, *subs_tec)
                self.Options.grid(row=2, column=1)

        def create(self):
            try:
                nome = self.name.get()
                tipo = self.type.get()
                materia = self.subject.get()
                try:
                    valor = int(self.val.get())
                except:
                    valor = 0

                grupo = self.group.get()
                if grupo == "Sim": grupo = "1"
                else: grupo = "0"

                prazo = str(self.date.get_date()).split("/")

                if len(prazo[1]) <= 1:prazo[1] = "0" + prazo[1]
                if len(prazo[0]) <= 1:prazo[0] = "0" + prazo[0]
                prazo = f"20{prazo[2]}-{prazo[0]}-{prazo[1]} 00:00:00"

                df = pd.read_excel(r"./Homework.xlsx")
                df["Valor"] = df["Valor"].fillna("0")

                new_row = {'Nome': nome, 'Matéria': materia, 'Prazo': prazo, 'Valor': valor,
                        'Grupo': grupo, 'Tipo': tipo, 'Hoje': ""}

                df = df.append(new_row, ignore_index=True)

                writer = ExcelWriter('Homework.xlsx')
                df.to_excel(writer, header=True, index=False)
                writer.save()

                app.reload_sheets()
                self.newScreen.destroy()
            except Exception as e:
                print(e)
                messagebox.showerror("Error", "Houve um erro na criação do para casa.")

    root = Tk()
    app = MainApp(root)
    root.mainloop()

from datetime import datetime
from datetime import date
import pandas as pd

# Load excel dataframe function
def load_excel():
	hj = date.today()

	df = pd.read_excel(r"./Homework.xlsx", engine='openpyxl')

	df = df.replace(to_replace=0, value="Nao")
	df = df.replace(1, "Sim")
	df["Alerta"] = 0

	tempo = []

	for n in range(len(df["Prazo"].values)):
		day = str(df["Prazo"].values[n]).split("-")
		birthday = datetime(int(day[0]), int(day[1]), int(day[2][:2]), 0, 0, 0)
		diff = datetime.now() - birthday
		if not "day" in str(diff):
			diff = "-0 days"
		if str(diff)[0] != "-":
			diff = int(str(diff).split(" ")[0]) * -1
			df["Alerta"][n] = diff
			tempo.append(diff)
		else:
			tempo.append(diff)
			df["Alerta"][n] = int(str(tempo[n]).split(" ")[0][1:])

	df["Valor"] = df["Valor"].fillna("0")
	df = df.sort_values(by=["Alerta"], ascending=True)

	medio = df[df["Tipo"] == "Medio"]
	tec = df[df["Tipo"] == "Tecnico"]

	return medio[["Nome", "Matéria", "Valor", "Grupo", "Alerta"]], tec[["Nome", "Matéria", "Valor", "Grupo", "Alerta"]]

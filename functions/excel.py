from datetime import date, datetime
import pandas as pd

# Load excel dataframe function
def load_excel():
	hj = date.today()

	df = pd.read_excel(r"./Homework.xlsx", engine='openpyxl')
	df = df.replace(to_replace=0, value="Nao")
	df = df.replace(1, "Sim")
	df["Prazo restante"] = 0

	tempo = []

	pd.options.mode.chained_assignment = None

	for n in range(len(df["Prazo"].values)):
		day = str(df["Prazo"].values[n]).split("-")
		alarmDay = datetime(int(day[0]), int(day[1]), int(day[2][:2]), 0, 0, 0)
		diff = datetime.now() - alarmDay
		if not "day" in str(diff):
			diff = "-0 days"
		if str(diff)[0] != "-":
			diff = int(str(diff).split(" ")[0]) * -1
			df["Prazo restante"][n] = diff
			tempo.append(diff)
		else:
			tempo.append(diff)
			df["Prazo restante"][n] = int(str(tempo[n]).split(" ")[0][1:])

	df["Valor"] = df["Valor"].fillna("0")
	df = df.sort_values(by=["Prazo restante"], ascending=True)

	medio = df[df["Tipo"] == "Medio"]
	tec = df[df["Tipo"] == "Tecnico"]

	return medio[["Nome", "Matéria", "Valor", "Grupo", "Prazo restante"]], tec[["Nome", "Matéria", "Valor", "Grupo", "Prazo restante"]]

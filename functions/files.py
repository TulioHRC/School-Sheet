from tkinter import filedialog as fd
from tkinter import messagebox
import shutil

def exportSheet(path):
    # This will copy the actual excel sheet and save it in other path selected
    try:
        toPath = fd.askdirectory()
        shutil.copy(path, toPath)
        messagebox.showinfo("File Exported", "The homework excel sheet was exported!")
    except Exception as e:
        messagebox.showerror("Error", f"The homework excel sheet was not exported!\nError: {e}")

def importSheet(toPath, app, restartFunction):
    # This will copy the selected excel sheet and save it in the actual path
    try:
        file = fd.askopenfilename()
        shutil.copy(file, toPath)
        messagebox.showinfo("File Imported", "The homework excel sheet was imported!\n\nRestarting the app...")

        # Restarting app
        app.master.destroy()
        restartFunction()
    except Exception as e:
        messagebox.showerror("Error", f"The homework excel sheet was not imported!\nError: {e}")

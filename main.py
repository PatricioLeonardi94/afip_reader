import Classes as classes
from tkinter import *
from tkinter import Tk, filedialog
import json

root = Tk()
root.withdraw()

file_path = filedialog.askdirectory()

print(file_path)

# guiController = classes.GUI()

f = open('info.json',)
data = json.load(f)

rarReader = classes.rarReader(data["month"], data["year"])

rarReader.loopFolder(file_path)


#  01/11/2021
#  30/11/2021
# Noviembre
# 2021
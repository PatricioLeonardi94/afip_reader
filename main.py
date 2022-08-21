import Classes as classes
from tkinter import *
from tkinter import Tk, filedialog
import json


{
    "dateIni":"01/05/2022",
    "dateEnd":"31/05/2022",
    "month":"febrero",
    "year":"2022"
}

root = Tk()
root.withdraw()

file_path = filedialog.askdirectory()

print(file_path)

# guiController = classes.GUI()

f = open('info.json',)
data = json.load(f)

rarReader = classes.rarReader(data["month"], data["year"])

rarReader.loopFolder(file_path)


#  01/01/2022
#  31/01/2022
# enero
# 2022
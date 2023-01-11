import pandas as pd
from tkinter import *
import pyautogui as gui
import numpy as np
from tkinter.filedialog import askopenfilename, asksaveasfile, askdirectory
import json
import os



class AfipController:

    def __init__(self, dataPath):
        f = open('files.json',)
        data = json.load(f)
        dfModels = pd.read_excel(data["modelos"][0]["name"], sheet_name=data["modelos"][0]["sheet"], header=0)
        dfSpecialModels = pd.read_excel(data["modelos"][1]["name"], sheet_name=data["modelos"][1]["sheet"], header=0)
        dfTiposFacturas = pd.read_excel(data["facturas"][0]["name"], sheet_name=data["facturas"][0]["sheet"], header=0)
        dfData = pd.read_csv(dataPath+data["archivos"][0]["name"], delimiter = "\n", header=None, encoding='latin-1')
        dfData = dfData.transpose()
        dfOut = pd.DataFrame()
        self.excelReader = ExcelReader(dfModels, dfData, dfSpecialModels, dfTiposFacturas, dfOut)


class ExcelReader:
    
    def __init__(self, models, data, specialModel, tiposFacturas, output):
        self.dfModels = models
        self.dfSpecialModels = specialModel
        self.dfTiposFacturas = tiposFacturas
        self.dfData = data
        self.dfOut = output

        
    def getOutPutData(self):
        rows = self.dfData.columns.size
        for column in self.dfData.columns: 
            dfRow = pd.DataFrame()
            row = self.dfData.columns.get_loc(column)
            if row < rows-1:
                self.normalRow(column, dfRow)
            else:
                self.specialRow(column, dfRow)


    def normalRow(self, column, dfRow):
        valorVenta = 0
        for col_name in self.dfModels.columns: 
            factura = self.getTipoDeFactura(column)
            valorVenta = self.getValorVenta(column)
            
            start = self.dfModels[col_name].astype('int64').values[0]
            end = self.dfModels[col_name].astype('int64').values[1]

            if col_name == "Tipo de Factura":
                dfRow.insert(self.dfModels.columns.get_loc(col_name),col_name,[factura])
            else:
                outputString = self.dfData[column].str.slice(start=start, stop=end).values[0]
                dfRow.insert(self.dfModels.columns.get_loc(col_name),col_name,[outputString])

        self.rowAdapterFinal(dfRow, valorVenta)
        self.dfOut = self.dfOut.append(dfRow, ignore_index=True)

    def specialRow(self, column, dfRow):
        for col_name in self.dfSpecialModels.columns: 
            start = self.dfSpecialModels[col_name].astype('int64').values[0]
            end = self.dfSpecialModels[col_name].astype('int64').values[1]
            outputString = self.dfData[column].str.slice(start=start, stop=end).values[0]
            dfRow.insert(self.dfSpecialModels.columns.get_loc(col_name),col_name,[outputString])
        self.rowAdapterFinal(dfRow, 1)
        self.dfOut = self.dfOut.append(dfRow, ignore_index=True)


    def rowAdapterFinal(self, df, valorVenta):
        grabado = "Grabado Entero"
        grabadoD = "Grabado Decimal"
        iva = "IVA Entero"
        ivaD = "IVA Decimal"
        total = "Total Entero"
        totalD = "Total Decimal"
        df[grabado] = float(df[grabado] + "." + df[grabadoD]) * valorVenta
        df[iva] = float(df[iva] + "." + df[ivaD]) * valorVenta
        df[total] = float(df[total] + "." + df[totalD]) * valorVenta
        del df[grabadoD]
        del df[ivaD]
        del df[totalD]       

    def getTipoDeFactura(self, colName):
        outputString = self.dfData[colName].str.slice(start=9, stop=12).values[0]
        col  = self.dfTiposFacturas["Tipo de Factura"]
        rowInModelos = self.dfTiposFacturas.loc[col == int(outputString)]
        nombreDeFactura = rowInModelos["Nombre de Factura"]
        return nombreDeFactura.values[0]

    def getValorVenta(self, colName):
        outputString = self.dfData[colName].str.slice(start=9, stop=12).values[0]
        col  = self.dfTiposFacturas["Tipo de Factura"]
        rowInModelos = self.dfTiposFacturas.loc[col == int(outputString)]
        valorParaVenta = rowInModelos["Ventas"].astype('int64')
        return valorParaVenta.values[0]

        

    def returnExcel(self):
        root = Tk()  # this is to close the dialogue box later
        try:
            with asksaveasfile(mode='w', defaultextension=".xlsx") as file:
                self.dfOut.to_excel(file.name)
        except AttributeError:
            print("The user cancelled save")
        root.destroy() # close the dialogue box

    def returnExcelInSameFolder(self, name):
        self.dfOut.to_excel(name)



class rarReader:

    def __init__(self, month, year):
        self.month = month
        self.year = year

    def loopFolder(self, folder):
        f = open('files.json',)
        data = json.load(f)

        with os.scandir(folder) as it:
            for entry in it:
                if entry.path.endswith(data["fileExtension"][0]["name"]) and entry.is_file():
                    folderName = entry.path[:-len(entry.name)]
                    patoolib.extract_archive(entry.path, outdir=folderName)
                
                    fileName = folderName + str(self.year) + " " + self.month + ".xlsx"
                    afip = AfipController(folderName)
                    afip.excelReader.getOutPutData()
                    afip.excelReader.returnExcelInSameFolder(fileName)
                elif entry.is_dir():
                    self.loopFolder(entry.path)





class GUI():
    def __init__(self):
        self.months =["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
        self.month = gui.prompt(text='Ingrese Mes', title='' , default='')
        self.year = gui.prompt(text='Ingrese Año', title='' , default='')
        confirmMessage = "El mes ingresado es " + self.month + ". El año ingresado es " + self.year
        self.confirm = gui.confirm(text=confirmMessage, title='', buttons=['Confirmar', 'Cancelar'])
        if self.confirm == "Confirmar" and self.month in self.months and len(self.year) == 4:
            self.month = self.month.lower()
            self.year = int(self.year)
            gui.alert(text='Realizando el proceso', title='', button='OK')
        else:
            gui.alert(text='Por favor valide los datos ingresado', title='', button='OK')






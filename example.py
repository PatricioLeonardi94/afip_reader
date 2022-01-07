import pandas as pd 
from tkinter import *
from tkinter.filedialog import askopenfilename
import json

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
f = open('files.json',)
data = json.load(f)
# df = pd.read_excel("modelos.xlsx", sheet_name='Sheet1', header=0)
# tipoDeFactura = 11
# col  = df["Tipo de Factura"]
# rowInModelos = df.loc[col == tipoDeFactura]

# nombreDeFactura = rowInModelos["Nombre de Factura"].astype(str)
# valorParaVenta = rowInModelos["Ventas"].astype('int64')

# print(nombreDeFactura.values[0])
# print(valorParaVenta.values[0])


# df = pd.read_csv(filename, delimiter = "\n", header=None)



# print(df.head())
print(data["modelos"][0]["name"], data["modelos"][0]["sheet"])

dfModels = pd.read_excel(data["modelos"][0]["name"], sheet_name=data["modelos"][0]["sheet"], header=0)
dfData = pd.read_csv(filename, delimiter = "\n", header=None)
dfData = dfData.transpose()
dfOut = pd.DataFrame()



for column in dfData.columns: 
    dfRow = pd.DataFrame()
    print(dfData.columns.get_loc(column))
    print(dfData.columns.size)
    # for col_name in dfModels.columns: 
    #     print(dfModels.columns.size)
        # start = dfModels[col_name].astype('int64').values[0]
        # end = dfModels[col_name].astype('int64').values[1]
        # outputString = dfData[column].str.slice(start=start, stop=end).values[0]
        # dfRow.insert(dfModels.columns.get_loc(col_name),col_name,[outputString])
    # dfOut = dfOut.append(dfRow, ignore_index=True)


# dfOut.to_excel("output.xlsx")  


# print("Nombre de Factura", nombreDeFactura)
# print("Ventas", valorParaVenta)


# dfExit = pd.DataFrame([[nombreDeFactura, valorParaVenta], []],
#                     index=['Tipo de Factura', 'Ventas'],
#                    columns=['col 1', 'col 2'])

# dfExit.to_excel("output.xlsx") 


#   def createDataFrame(df, data, row):
#         dfFinal = pd.DataFrame(
#             {
#                 "fecha": data.str.slice(start=1, stop=9),
#                 "tipoFactura": data.str.slice(start=9, stop=12),
#                 "puntoDeVenta": data.str.slice(start=12, stop=16),
#                 "numeroFactura": data.str.slice(start=16, stop=24),
#                 "numeroComprobanteRegistrado": data.str.slice(start=24, stop=32),
#                 "cantidadDeHojas": data.str.slice(start=1, stop=9),
#                 "cuitDni": data.str.slice(start=1, stop=9),
#                 "razonSocial": data.str.slice(start=1, stop=9),
#                 "importeGrabados": data.str.slice(start=1, stop=9),
#                 "totalIva": data.str.slice(start=1, stop=9),
#                 "total": data.str.slice(start=1, stop=9),                
#             }
#         )

#         for col_name in df.columns: 
#             print(col_name)


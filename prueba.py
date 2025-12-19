import pandas as pd

xls = pd.ExcelFile("./listado/listado.xlsx")
print(xls.sheet_names)
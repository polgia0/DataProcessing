from PyQt5 import QtWidgets
from config import DOE,DS
import xlwings as xw
import pandas as pd
def doesave(self):  
    if not DOE.getdoe():
        QtWidgets.QMessageBox.critical(self,'Error',"No Results.Build a Model first!",QtWidgets.QMessageBox.Ok)
        return()
    Lc=DS.getLc()
    Lcy=Lc[DS.getGc()]
    Lcx=Lc[-DS.getGc()]
    data=DS.getData()
    Y=data[Lcy]
    X=data[Lcx]             
    Y=Y.values.astype('float')
    X=X.values.astype('float')
    X=pd.DataFrame(X,columns=Lcx)
    Y=pd.DataFrame(Y,columns=Lcy)
    self.appExcel=xw.App()
    wb=xw.books.active
    sht=wb.sheets[0]
    sht.name='DataSet'
    sht.range('A1').value=X.join(Y)
    sht=wb.sheets[1]
    sht.name='Coefficient'
    sht.range('A1').value=DOE.getres().params[1:]
    sht=wb.sheets[2]
    sht.name='Residual'
    sht.range('A1').value=DOE.getres().resid
    wb.sheets.add(name='Fitted')
    sht=wb.sheets['Fitted']
    sht.range('A1').value=DOE.getres().fittedvalues

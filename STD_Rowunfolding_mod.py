from PyQt5 import QtWidgets
from config import DS
import xlwings as xw
import pandas as pd
def rowunfolding(self):
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Gr=DS.Gr[DS.Ir]
#    if data.isnull().all().all():
#        QtWidgets.QMessageBox.critical(self,'Error','NAs are present.\n Remove them before binding',\
#                                       QtWidgets.QMessageBox.Ok)
#        return()       
    Grg=pd.Series(Gr).groupby(Gr)
    if Grg.ngroups<2:
        QtWidgets.QMessageBox.critical(self,'Error','No enough groups.\n Groups must be > 1',\
                                       QtWidgets.QMessageBox.Ok)
        return()
    pn=int(len(Gr)/Grg.ngroups)
    sdata=pd.DataFrame()
    for name,group in data.groupby(Gr):
        nr,nc=group.shape
        if(nr != pn):
            QtWidgets.QMessageBox.critical(self,'Error','Groups must have the same lenght',\
                                       QtWidgets.QMessageBox.Ok)
            return()
        line=[]
        for x in group.columns:
            line=line+group[x].values.tolist()
        sdata[name]=line
    sdata=sdata.T
    line=[]
    for lc in DS.Lc.tolist():
        for i in range(1,nr+1):
            line.append(lc+'_'+str(i))
    sdata.columns=line
    sdata.index=Grg.groups.keys()
    self.appExcel=xw.App()
    wb=xw.books.active
    sht=wb.sheets[0]
    sht.range('A1').value=sdata

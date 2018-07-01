from PyQt5 import QtWidgets
from config import DS
import xlwings as xw
import numpy as np
import pandas as pd
def getexcel(self):
    try:
        wb=xw.books.active
        sht=wb.sheets[0]
        Raw=sht.range('F6').options(pd.DataFrame,index=False,header=False,expand='table').value
    except:
        QtWidgets.QMessageBox.critical(self,'Data Set Warning', 
        'The Excel is in Input!\n Click on Excel bar and hit Return \n Then try again',
        QtWidgets.QMessageBox.Ok)
        return()
    nr,nc=Raw.shape
    DS.Ty=Raw.dtypes.values
    DS.Gc=np.array(sht.range((2,6),(2,nc+5)).value,dtype=bool)
    DS.Lc=np.array(sht.range((3,6),(3,nc+5)).value,dtype='<U25')
    DS.Ic=np.array(sht.range((4,6),(4,nc+5)).value,dtype=bool)
    DS.Cc=np.array(sht.range((5,6),(5,nc+5)).value,dtype='<U25')
    DS.Cr=np.array(sht.range((6,5),(nr+5,5)).value,dtype='<U25')
    DS.Gr=np.array(sht.range((6,1),(nr+5,1)).value,dtype=int)
    DS.Ts=np.array(sht.range((6,2),(nr+5,2)).value,dtype=bool)
    DS.Lr=np.array(sht.range((6,3),(nr+5,3)).value,dtype='<U25')
    DS.Ir=np.array(sht.range((6,4),(nr+5,4)).value,dtype=bool)
    DS.Raw.index=DS.Lr
    DS.Raw.columns=DS.Lc
    wb.close()
    self.appExcel.quit()

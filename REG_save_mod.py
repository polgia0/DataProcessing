from config import REG,DS
import xlwings as xw
import numpy as np
def regsave(self):  
    self.appExcel=xw.App()
    wb=xw.books.active
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Ts=DS.Ts[DS.Ir]
    Lr=DS.Lr[DS.Ir]
    Lc=DS.Lc[DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Lcx=Lc[-Gc]
    Lcy=Lc[Gc]
    X=data.loc[:,-Gc]
    Y=data.loc[:,Gc]
    Xtrain=X[-Ts]
    Lrt=Lr[-Ts]
    Xtest=X[Ts]
    Ytest=Y[Ts]
    Lrs=Lr[Ts]
    Yfit=REG.lr.predict(Xtrain)
    sht=wb.sheets[0]
    sht.name='Coefficient'
    sht.range('A1').value='Intercept'
    sht.range('B1').value=REG.lr.intercept_
    sht.range('A2').value='Coefficients'
    sht.range('B2').value=Lcx
    sht.range('B3').value=REG.lr.coef_
    if(DS.Cl!=None):
        sht.range('B4').value=range(len(DS.Cl))  
        sht.range('A5').value='Group Class'
        sht.range('B5').value=DS.Cl  
    if len(Ytest)>0:
        sht.range('A6').value='Score'
        sht.range('B6').value=REG.lr.score(Xtest,Ytest)
    sht=wb.sheets[1]
    sht.name='Fitted'
    sht.range('B1').value=Lcy
    sht.range('A2').value=Lrt[np.newaxis].T
    sht.range('B2').value=Yfit[np.newaxis].T
    try:
        wb.sheets.add(name='CV original')
        sht=wb.sheets['CV original']
        sht.range('B1').value=Lcy
        sht.range('A2').value=Lr[np.newaxis].T
        sht.range('B2').value=REG.Ycv
    except:
        pass
    try:
        wb.sheets.add(name='Additional')
        sht=wb.sheets['Additional']
        sht.range('B1').value=Lcy
        sht.range('A2').value=Lrs[np.newaxis].T
        sht.range('B2').value=REG.TXt
    except:
        pass


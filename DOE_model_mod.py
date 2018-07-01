from PyQt5 import QtWidgets
from config import DS,DOE
from itertools import combinations
def doemodel(self):
    Lc=DS.Lc[DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Lcx=Lc[-Gc]
    Lcy=Lc[Gc]
    ncx=len(Lcx)
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Y=data[Lcy] 
    X=data[Lcx]             
    Ynan=Y.isnull().sum().sum()
    Xnan=X.isnull().sum().sum()
    if Ynan>0:
        QtWidgets.QMessageBox.critical(self,'Error',                          \
        "There are {}  nan in Responce. \n Remove them.".format(Ynan),        \
                   QtWidgets.QMessageBox.Ok)
        return()
    if Xnan>0:
        QtWidgets.QMessageBox.critical(self,'Error',                          \
        "There are {}  nan in Factor Matrix. \n Remove them.".format(Xnan),   \
                   QtWidgets.QMessageBox.Ok)
        return()
    DOE.lfac=[]
    fac=range(1,ncx+1)
    for i in fac:
        DOE.lfac=DOE.lfac+[j for j in combinations(fac,i)]
    if(sum((X==0).sum())+sum((X==-1).sum())+sum((X==1).sum())!=X.shape[0]*X.shape[1]):
        DOE.coded=True
    else:
        DOE.coded=False
    return()
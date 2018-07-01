from PyQt5 import QtWidgets
from config import DS
import numpy as np
import pandas as pd
import scipy.stats as stats
from matout_mod import matoutDlg
def summary(self):
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    nr,nc=data.shape
    sTable=pd.DataFrame(columns=DS.Lc)
    vc=data.count(axis=0)
    vm=data.mean(axis=0,skipna=True)
    vvar=data.var(axis=0,skipna=True)
    vsd=data.std(axis=0,skipna=True)
    vt=stats.t.ppf(0.95,vc-1)
    vm_min=vm-vt*vsd
    vm_max=vm+vt*vsd
    vchi1=stats.chi2.ppf(0.975,vc-1)
    vchi2=stats.chi2.ppf(0.025,vc-1)
    vvar_min=vvar*(vc-1)/vchi1
    vvar_max=vvar*(vc-1)/vchi2
    vmd=data.median(axis=0,skipna=True)
    vmd=np.array(vmd)
    vmd=vmd.T
    vmo=np.array(data)
    vmo=stats.mode(vmo)[0]
    corr=data.corr(method='pearson')
    corr=np.array(corr)
    sTable.loc['Index',:]=range(1,nc+1)
    sTable.loc['Number',:]=vc
    sTable.loc['Minimum',:]=data.min(axis=0,skipna=True)
    sTable.loc['Maximum',:]=data.max(axis=0,skipna=True)
    sTable.loc['Sum',:]=data.sum(axis=0,skipna=True)
    sTable.loc['Mean',:]=vm
    sTable.loc['Mean.min',:]=vm_min
    sTable.loc['Mean.max',:]=vm_max
    sTable.loc['Standard Dev.',:]=vsd
    sTable.loc['Std Dev. Min.',:]=np.sqrt(vvar_min)
    sTable.loc['Std Dev.Max',:]=np.sqrt(vvar_max)
    sTable.loc['Variance',:]=vvar
    sTable.loc['Var.Min.',:]=vvar_min
    sTable.loc['Var.Max.',:]=vvar_max
    sTable.loc['Median',:]=vmd
    sTable.loc['Mode',:]=vmo
    for i in range(nc):
        sTable.loc[str(i),:]=corr[i,:]
    sTable=sTable.round(3)
    matout=QtWidgets.QDialog()
    matout=matoutDlg(parent=self,dataframe=sTable,bH=True,bV=True)
    matout.exec_()
    matout.show()
    return()

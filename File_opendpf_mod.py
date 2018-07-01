from PyQt5 import QtWidgets
from config import DS
import numpy as np
import pandas as pd
import re
def opendpf(self):
    def parsebool(l_str):
        l_str=l_str.values.tolist()
        if type(l_str[0])!=bool:
            l_str=[re.sub(r'^FALSO\b','False',w) for w in l_str]
            l_str=[re.sub(r'^FALSE\b','False',w) for w in l_str]
            l_str=[re.sub(r'^Falso\b','False',w) for w in l_str]
            l_str=[re.sub(r'^F\b','False',w) for w in l_str]
            l_str=[re.sub(r'^VERO\b','True',w) for w in l_str]
            l_str=[re.sub(r'^Vero\b','True',w) for w in l_str]
            l_str=[re.sub(r'^TRUE\b','True',w) for w in l_str]
            l_str=[re.sub(r'^T\b','True',w) for w in l_str]
            l_str=[eval(w) for w in l_str]
        return(np.array(l_str,dtype=bool))
    fname=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '','*.csv *.xls *.xlsx')
    fname=fname[0]
    if fname=='':return(0)
    if fname[-3:]=='csv':
        DSR=pd.read_csv(fname,header=None,index_col=None,delimiter=';',
                        decimal=',',na_values='NA',
                        false_values=['FALSO','Falso','FALSE','False','F'],
                        true_values=['VERO','Vero','TRUE','True','T'])
    else:
        DSR=pd.read_excel(fname,sheetname=0,header=None,index_col=None,na_values='NA')
    DS.setGc(parsebool(DSR.iloc[0,5:]))
    DS.setLc(np.array(DSR.iloc[1,5:],dtype=object))
    DS.setIc(parsebool(DSR.iloc[2,5:]))
    DS.setCc(pd.Series(DSR.iloc[3,5:].values))
    if fname[-3:]=='csv':
        DSR=pd.read_csv(fname,header=None,index_col=None,delimiter=';',
                        decimal=',',skiprows=4,na_values='NA',
                        false_values=['FALSO','False','FALSE','False'],
                        true_values=['VERO','Vero','TRUE','True'])
        Raw=DSR.ix[:,5:]
        Gr=pd.Series(DSR.iloc[:,0],dtype=int)
        DS.setGr(Gr.values)
        DS.setTs(np.array(DSR.iloc[:,1],dtype=bool))
        DS.setLr(np.array(DSR.iloc[:,2],dtype=object))
        DS.setIr(np.array(DSR.iloc[:,3],dtype=bool))
        DS.setCr(pd.Series(DSR.iloc[:,4].values,name=None))
        Raw=pd.DataFrame(Raw.values,index=DS.Lr,columns=DS.Lc)
    else:
        Gr=pd.Series(DSR.iloc[4:,0],dtype=int)
        DS.setGr(Gr.values)
        DS.setTs(np.array(DSR.iloc[4:,1],dtype=bool))
        DS.setLr(np.array(DSR.iloc[4:,2],dtype=object))
        DS.setIr(np.array(DSR.iloc[4:,3],dtype=bool))
        DS.setCr(pd.Series(DSR.iloc[4:,4].values,name=None))
        Raw=pd.DataFrame(DSR.ix[4:,5:].values,index=DS.Lr,columns=DS.Lc)
    Ty=[type(Raw.ix[DS.Lr[0],DS.Lc[i]]) for i in range(Raw.shape[1])]
    DS.setTy(np.array(Ty,dtype=object))
    DS.setRaw(Raw)
    DS.setNrRaw(Raw.shape[0])
    DS.setNcRaw(Raw.shape[1])
    DS.getData()
    DS.getNr()
    DS.getNc()
    DS.getN()
    return(1)

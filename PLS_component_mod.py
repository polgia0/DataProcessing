from config import DS
from PLS_model_mod import pls_model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn as sk
def plscomp(self):
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Xtrain=data[-DS.Ts[DS.Ir]]
    Y=Xtrain.loc[:,DS.Gc[DS.Ic]]
    X=Xtrain.loc[:,-DS.Gc[DS.Ic]]
    nr=X.shape[0]
    ncy=Y.shape[1]
    ncx=X.shape[1]
    ncpmax=ncx
    if(ncpmax>20):
        ncpmax=20
    if(ncpmax>20):
        ncpmax=20
    X0=X-X.mean(axis=0)
    X0=X0/X0.std(axis=0)
    Y0=Y-Y.mean(axis=0)
    Y0=Y0/Y0.std(axis=0)
    SS=sum((Y0**2).sum())
    X0=pd.DataFrame(X0)
    Y0=pd.DataFrame(Y0)
    vQ2=np.zeros(ncpmax)
    vR2=np.zeros(ncpmax)
    np.random.seed(nr)
    for ncp in range(ncpmax): 
        kf=sk.model_selection.KFold(shuffle=True)
        Ycv=pd.DataFrame(0,index=range(nr),columns=range(ncy))
        Yp=pd.DataFrame(0,index=range(nr),columns=range(ncy))
        for train, test in kf.split(X0):
             X=X0.iloc[train,:]
             Y=Y0.iloc[train,:]
             Xm,Ym,Sx,Sy,Xc,Yc,SSX,SSY,P,C,U,T,Q,W,WS,B,Ysc,Ys,R2,SPEX,SPEY,HT2,VIP,T95,T99=pls_model(X,Y,ncp+1,False,False,False)
             X_test=X0.iloc[test,:]
             Ycv.iloc[test,:]=np.dot(X_test,B)
             Yp.iloc[train,:]=np.dot(X,B)
        press=sum(pd.DataFrame((Ycv.values-Y0.values)**2).sum())
        sse=sum(pd.DataFrame((Yp.values-Y0.values)**2).sum())
        vQ2[ncp]=(SS-press)/SS
        vR2[ncp]=(SS-sse)/SS
    fig,ax=plt.subplots()
    ind=range(1,ncpmax+1)
    ax.plot(ind,vQ2,color='blue')
    ax.set_xlabel('Component Number')
    ax.set_ylabel('Q2',color='blue')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.set_xlim([1,ncpmax+1])
    ax.set_title('Q^2 and R^2 vs. Component Number')
    ax1=ax.twinx()
    ax1.plot(ind,vR2,color='red')
    ax1.set_ylabel('R2',color='red') 
    fig.show()

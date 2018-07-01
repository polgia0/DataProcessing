from config import DS
from PCA_model_mod import pca_model
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import sklearn as sk
def pcacomp(self):
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Xtrain=data[-DS.Ts[DS.Ir]]
    nr,nc=Xtrain.shape
    ncpmax=nc
    if(ncpmax>20):
        ncpmax=20
    Xc=Xtrain-Xtrain.mean(axis=0)
    Xc=Xc/Xc.std(axis=0)
    SS=sum((Xc**2).sum())
    Xc=pd.DataFrame(Xc)
    vQ2=np.zeros(ncpmax)
    np.random.seed(nr)
    for ncp in range(ncpmax):                
        kf=sk.model_selection.KFold(shuffle=True)
        Xcv=pd.DataFrame(0,index=range(nr),columns=range(nc))
        for train, test in kf.split(Xc):
            Xt=Xc.iloc[train,:]
            T,P,LAM,SSX,RV,X,SPE,SSE,R2X,HT2,Res,Xm,Xstd,MQ,MT,Q95,T95,Q99,T99=pca_model(Xt,ncp+1,False,False,False)
            X_test=Xc.iloc[test,:]
            T_test=np.dot(X_test,P)
            Xcv.iloc[test,:]=np.dot(T_test,P.T)
        press=sum(pd.DataFrame((Xcv.values-Xc.values)**2).sum())
        vQ2[ncp]=(SS-press)/SS
    vR2=RV.cumsum()
    fig,ax=plt.subplots()
    ind=range(1,len(vQ2)+1)
    ax.plot(ind,vQ2,color='blue')
    ax.set_xlabel('Component Number')
    ax.set_ylabel('Q2',color='blue')
    ax.xaxis.grid()
    ax.yaxis.grid()
    ax.set_xlim([1,len(vQ2)+1])
    ax.set_ylim([0,1.1])
    ax.set_title('Q^2 and R^2 vs. Component Number')
    ax1=ax.twinx()
    ax1.plot(ind,vR2,color='red')
    ax1.set_ylabel('R2',color='red') 
    ax1.set_ylim([0,1.1])
    fig.show()
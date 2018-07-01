from config import DS,PLS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
def plsaddata(self):
    Ts=DS.Ts[DS.Ir]
    nr=len(Ts)
    Lr=DS.Lr[DS.Ir]
    Lrt=Lr[Ts]
    Lc=DS.Lc[DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Lcy=Lc[Gc]
    Lcx=Lc[-Gc]
    Y=DS.Raw[Lcy]
    X=DS.Raw[Lcx]
    Xt=X[Ts].values
    Yt=Y[Ts].values
    Xt=Xt.astype('float')
    if(PLS.bp):
        Xmt=Xt.mean(axis=1)
        Xt=Xt.T-Xmt
        Xt=Xt.T
    if(PLS.bc):
        Xt=Xt-PLS.Xm
    if(PLS.bs):
        Xt=Xt/PLS.Sx
    PLS.Ysc=np.dot(Xt,PLS.B)
    PLS.TXt=PLS.Ysc
    if(PLS.bs):
        PLS.TXt=PLS.Ysc*PLS.Sy
    if(PLS.bc):
        PLS.TXt=PLS.TXt+PLS.Ym
    fig=plt.figure()
    ax=fig.add_subplot(111)
    if(Yt[0]is not None):
        Yt=Yt.astype(float)      
        if(PLS.bc):
            Yt=Yt-PLS.Ym
        if(PLS.bs):
            Yt=Yt/PLS.Sy
        color=plt.cm.rainbow(np.linspace(0,1,Yt.shape[1]))
        for i in range(Yt.shape[1]):
            ax.scatter(Yt[:,i],PLS.Ysc[:,i],color=color[i])
        ax.set_xlabel('Measured Data')
        ax.set_ylabel('Predicted Data')
        Dmin=np.array([Yt.min(),PLS.Ysc.min()]).min()
        Dmax=np.array([Yt.max(),PLS.Ysc.max()]).max()
        ax.set_xlim([Dmin,Dmax])
        ax.set_ylim([Dmin,Dmax])
        ax.set_title('Measured vs. Predicted Data')
        ax.add_line(Line2D([Dmin,Dmax],[Dmin,Dmax],color='red')) 
    if(Yt[0] is None):
        nr,nc=PLS.Ysc.shape
        color=plt.cm.rainbow(np.linspace(0,1,nc))
        if(nc>1):
            ind=range(1,nr+1)
            for i in range(nc):
                ax.plot(ind,PLS.Ysc[:,i],color=color[i])
                ax.set_ylim([min(PLS.Ysc.min()),max(PLS.Ysc.max())])
        else:
            ind=range(nr)
            ax.scatter(ind,PLS.TXt,color='r')
            for i in range(nr):
                ax.annotate(Lrt[i],(ind[i],PLS.TXt[i]),rotation=45)
            ax.set_xlim([0,nr])
        ax.set_xlabel('n.Point')
        ax.set_ylabel('Predicted Data')
        ax.set_title('Predicted Data')
    ax.xaxis.grid()
    ax.yaxis.grid()
    fig.show()


from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import PCA,DS
import math
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
Ui_pcaaddataDialog,QDialog=loadUiType('pcaaddata.ui')
class pcaaddataDlg(QtWidgets.QDialog,Ui_pcaaddataDialog):
    def __init__(self,parent=None):
        super(pcaaddataDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        for x in range(PCA.ncp):
            self.XcomboBox.addItem(str(x+1))
            self.YcomboBox.addItem(str(x+1))
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
        self.accepted.connect(self.addata)
    def addata(self):
        c1=self.XcomboBox.currentIndex()-1
        c2=self.YcomboBox.currentIndex()-1
        Lr=DS.Lr[DS.Ir]
        nr=len(Lr)
        Lc=DS.Lc[DS.Ic]
        nc=len(Lc)
        Ts=DS.Ts[DS.Ir]
        Lrt=Lr[Ts]
        st2=PCA.rv*nc
        X=DS.Raw.loc[DS.Ir,DS.Ic]
        Xt=X[Ts]
        if(PCA.bp):
            Xtm=Xt.mean(axis=1)
            Xt=Xt.T-Xtm
            Xt=Xt.T
        if(PCA.bc):
            Xt=Xt-PCA.Xm
        if(PCA.bs):
            Xt=Xt/PCA.Xstd
        PCA.TXt=np.dot(Xt,PCA.lo[:,[c1,c2]])
        alpha=(100-self.alphaspinBox.value())/100
        fn=np.array(range(1,(PCA.ncp+1)))
        fd=(nr+1)-fn
        fn =tuple(fn)
        fd =tuple(fd)
        fa=sp.stats.f.ppf(alpha,fn,fd)
        fig=plt.figure()
        ax=fig.add_subplot(111)
        ax.scatter(PCA.sco[:,c1],PCA.sco[:,c2],alpha=0.3,color='green',s=30,marker='o')
        ax.scatter(0,0,color='black',s=60,marker='+')
        ax.scatter(PCA.TXt[:,0],PCA.TXt[:,1],color='red',marker='o')
        if self.VcheckBox.isChecked():
            for i,txt in enumerate(Lrt):
                ax.annotate(txt,(PCA.TXt[i,0],PCA.TXt[i,1]),color='red')
        lim=[PCA.sco.min(),0,PCA.sco.max(),PCA.TXt.min(),PCA.TXt.max()]
        vlim=max(abs(np.array(lim)))*1.2
        ax.set_xlim([math.copysign(vlim,lim[0]),math.copysign(vlim,lim[2])])
        ax.set_ylim([math.copysign(vlim,lim[0]),math.copysign(vlim,lim[2])])
        ax.set_title('Score Plot ('+str(round(PCA.rv[c1]+PCA.rv[c2],2))+'%),Training green,Test red')
        ax.set_xlabel('Comp.'+self.XcomboBox.currentText()+' ('+str(round(PCA.rv[c1],2))+'%)')
        ax.set_ylabel('Comp.'+self.YcomboBox.currentText()+' ('+str(round(PCA.rv[c2],2))+'%)')
        ax.xaxis.grid()
        ax.yaxis.grid()
        ell=Ellipse(xy=(0,0),width=2*math.sqrt(fa[PCA.ncp-1]*st2[c1]),height=2*math.sqrt(fa[PCA.ncp-1]*st2[c2]),color='red')
        ell.set_facecolor('none')
        ax.add_artist(ell)
        alpha=alpha*100
        ax.annotate(str(round(alpha,0))+'%',xy=(0,-math.sqrt(fa[PCA.ncp-1]*st2[c2])),color='red')
        fig.show()
       

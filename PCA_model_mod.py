from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from config import DS,PCA
import numpy as np
import scipy as sp
import sklearn as sk
Ui_pcamodel,QDialog=loadUiType('pcamodel.ui')
class pcamodelDlg(QtWidgets.QDialog,Ui_pcamodel):
    def __init__(self,parent=None):
        super(pcamodelDlg,self).__init__(parent)
        self.setupUi(self)
        self.spinBox.setMaximum(DS.Raw.shape[1])
        XYname=DS.Lc[DS.Ic]
        self.VlistWidget.addItems(DS.Lc[-np.in1d(DS.Lc,XYname)])
        Yname=XYname[DS.Gc[DS.Ic]]
        self.VlistWidget.addItems(DS.Lc[np.in1d(DS.Lc,Yname)])
        Xname=XYname[-DS.Gc[DS.Ic]]
        self.XlistWidget.addItems(DS.Lc[np.in1d(DS.Lc,Xname)])
        self.XpushButton.clicked.connect(self.addX)
        self.XradioButton.clicked.connect(self.allX)
        self.XlistWidget.doubleClicked.connect(self.removeX)
        self.accepted.connect(self.pcamodel)
    def addX(self):
        nrow=self.VlistWidget.currentRow()
        item_str=self.VlistWidget.item(nrow).text()
        self.VlistWidget.takeItem(nrow)
        self.XlistWidget.addItem(item_str)
    def removeX(self):
        nrow=self.XlistWidget.currentRow()
        item_str=self.XlistWidget.item(nrow).text()
        self.XlistWidget.takeItem(nrow)
        self.VlistWidget.addItem(item_str)        
        self.VlistWidget.setCurrentRow(0)
    def allX(self):
        for i in range(self.VlistWidget.count()):
            self.XlistWidget.addItem(self.VlistWidget.item(i).text())
        self.VlistWidget.clear()
    def pcamodel(self):
        PCA.ncp=self.spinBox.value()
        Lcx=[]
        for i in range(self.XlistWidget.count()):
            Lcx.append(self.XlistWidget.item(i).text())
        ncx=len(Lcx)
        if ncx < 1:
            QtWidgets.QMessageBox.critical(self,'Error',"Wrong X Choice",\
                                           QtWidgets.QMessageBox.Ok)
            self.reject()
            return
        Ic=np.in1d(DS.Lc,Lcx)
        if PCA.ncp>len(Lcx): PCA.ncp=len(Lcx)
        DS.Ic=Ic
        X=DS.Raw.loc[DS.Ir,DS.Ic]
        X=X[-DS.Ts[DS.Ir]]
        Xnan=X.isnull().isnull().all().all()
        if Xnan:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  nan in Factor Matrix. \n Remove them.".format(Xnan),\
                                           QtWidgets.QMessageBox.Ok)
            self.reject()
            return
        Xstd=X.std(axis=0)
        nXnull=sum(Xstd==0)
        if nXnull!=0:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  identical column(s) in the Matrix. \n Remove them.".format(nXnull),\
                                           QtWidgets.QMessageBox.Ok)
            self.reject()
            return
        PCA.bc=self.centercheckBox.isChecked()
        PCA.bs=self.scalecheckBox.isChecked()
        PCA.bp=self.snvcheckBox.isChecked()
        if self.nipalsradioButton.isChecked():
            PCA.sco,PCA.lo,PCA.ei,PCA.ssx,PCA.rv,PCA.Xc,PCA.Q,PCA.sse,PCA.cres,PCA.ht2, \
            PCA.res,PCA.Xm,PCA.Xstd,PCA.MQ,PCA.MT,PCA.Q95,PCA.T95,PCA.Q99,PCA.T99=    \
            pca_model(X.values,PCA.ncp,PCA.bc,PCA.bs,PCA.bp)
        if self.svdradioButton.isChecked():
            PCA.sco,PCA.lo,PCA.ei,PCA.ssx,PCA.rv,PCA.Xc,PCA.Q,PCA.sse,PCA.cres,PCA.ht2, \
            PCA.res,PCA.Xm,PCA.Xstd,PCA.MQ,PCA.MT,PCA.Q95,PCA.T95,PCA.Q99,PCA.T99=    \
            svd_model(X.values,PCA.ncp,PCA.bc,PCA.bs,PCA.bp)
        return
def pca_model(X,ncp,bc,bs,bp):
    X=X.astype('float')
    nr,nc=X.shape
    if(bp):
        Xm=np.zeros(nr)
        Xm=X.mean(axis=1)
        X=X.T-Xm
        X=X.T
    Xm=np.zeros(nc)
    Xstd=Xm
    if(bc):
        Xm=X.mean(axis=0)
        X=X-Xm
    if(bs):
        Xstd=X.std(axis=0)
        X=X/Xstd
    SSX=(X**2).sum(axis=0)
    Res=X
    T=np.zeros((nr,ncp))
    P=np.zeros((nc,ncp))
    LAM=np.zeros(ncp)
    tolerance = 1E-10
    np.random.seed(nr)
    for a in range(ncp):
        t_a_guess=np.random.rand(nr, 1)*2
        t_a = t_a_guess+1.0
        itern = 0
        while np.linalg.norm(t_a_guess-t_a)>tolerance and itern< 500:
            t_a_guess = t_a
            dt=np.dot(t_a.T,t_a)
            p_a=np.dot(Res.T,t_a)/dt
            p_a=p_a/np.linalg.norm(p_a)
            t_a=np.dot(Res, p_a)/np.dot(p_a.T,p_a)
            itern += 1
        Res=Res-np.dot(t_a, p_a.T)
        T[:, a]=t_a.ravel()
        P[:, a]=p_a.ravel()
        LAM[a] = dt
    RV=LAM/sum(SSX)
    LAM=LAM/np.mean(SSX)
    Res=np.array(Res)
    X=np.array(X)
    SPE=np.sum(Res**2,axis=1)
    SSE=np.sum(Res**2,axis=0)
    R2X=(SSX-SSE)/SSX
    MQ=np.identity(nc)-np.dot(P,P.T)
    Q=np.diag(np.dot(np.dot(X,MQ),X.T))
    MT=np.dot(np.dot(P,np.diag(1/T.var(axis=0))),P.T)
    HT2=np.diag(np.dot(np.dot(X,MT),X.T))
    LQ=np.log10(np.abs(Q))
    Q95=10**(LQ.mean()+sp.stats.t.ppf(0.95,nr-1)*LQ.std())
    # from http://www.itl.nist.gov/div898/handbook/pmc/section5/pmc543.htm
    T95=(nr-1)*ncp/(nr-ncp)*sp.stats.f.ppf(0.95,ncp,nr-ncp)
    Q99=10**(LQ.mean()+sp.stats.t.ppf(0.99,nr-1)*LQ.std())
    T99=(nr-1)*ncp/(nr-ncp)*sp.stats.f.ppf(0.99,ncp,nr-ncp)
    return T,P,LAM,SSX,RV,X,SPE,SSE,R2X,HT2,Res,Xm,Xstd,MQ,MT,Q95,T95,Q99,T99
def svd_model(X,ncp,bc,bs,bp):
    X=X.astype('float')
    nr,nc=X.shape
    if(bp):
        Xm=np.zeros(nr)
        Xm=X.mean(axis=1)
        X=X.T-Xm
        X=X.T
    Xm=np.zeros(nc)
    Xstd=Xm
    if(bc):
        Xm=X.mean(axis=0)
        X=X-Xm
    if(bs):
        Xstd=X.std(axis=0)
        X=X/Xstd
    SSX=(X**2).sum(axis=0)
    pca=sk.decomposition.pca.PCA(n_components=ncp)
    pca.fit(X)
    T=pca.transform(X)
    P=pca.components_
    P=P.T
    LAM=pca.explained_variance_
    RV=pca.explained_variance_ratio_
    Res=X-pca.inverse_transform(T)
    Res=np.array(Res)
    X =np.array(X)
    SPE=np.sum(Res**2, axis=1)
    SSE=np.sum(Res**2, axis=0)
    R2X=(SSX-SSE)/SSX
    MQ=np.identity(nc)-np.dot(P,P.T)
    Q=np.diag(np.dot(np.dot(X,MQ),X.T))
    MT=np.dot(np.dot(P,np.diag(1/T.var(axis=0))),P.T)
    HT2=np.diag(np.dot(np.dot(X,MT),X.T))
    Q95=Q.mean()+sp.stats.t.ppf(0.95,nr-1)*Q.std()
    T95=(nr-1)*(nr+1)*ncp/nr/(nr-ncp)*sp.stats.f.ppf(0.95,ncp,nr-ncp)
    Q99=Q.mean()+sp.stats.t.ppf(0.99,nr-1)*Q.std()
    T99=(nr-1)*(nr+1)*ncp/nr/(nr-ncp)*sp.stats.f.ppf(0.99,ncp,nr-ncp)
    return T,P,LAM,SSX,RV,X,SPE,SSE,R2X,HT2,Res,Xm,Xstd,MQ,MT,Q95,T95,Q99,T99


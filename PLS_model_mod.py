from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from config import DS,PLS
import numpy as np
import scipy as sp
Ui_plsmodel,QDialog=loadUiType('plsmodel.ui')
class plsmodelDlg(QtWidgets.QDialog,Ui_plsmodel):
    def __init__(self,parent=None):
        super(plsmodelDlg,self).__init__(parent)
        self.setupUi(self)
        XYname=DS.Lc[DS.Ic]
        self.VlistWidget.addItems(DS.Lc[-np.in1d(DS.Lc,XYname)])
        Xname=XYname[-DS.Gc[DS.Ic]]
        self.XlistWidget.addItems(DS.Lc[np.in1d(DS.Lc,Xname)])
        Yname=XYname[DS.Gc[DS.Ic]]
        self.YlistWidget.addItems(DS.Lc[np.in1d(DS.Lc,Yname)])
        self.XpushButton.clicked.connect(self.addX)
        self.YpushButton.clicked.connect(self.addY)
        self.YradioButton.clicked.connect(self.allY)
        self.XradioButton.clicked.connect(self.allX)
        self.XlistWidget.doubleClicked.connect(self.removeX)
        self.YlistWidget.doubleClicked.connect(self.removeY)
        self.spinBox.setMaximum(len(XYname))
        self.accepted.connect(self.plsmodel)
    def allY(self):
        for i in range(self.VlistWidget.count()):
            self.YlistWidget.addItem(self.VlistWidget.item(i).text())
        self.VlistWidget.clear()
    def allX(self):
        for i in range(self.VlistWidget.count()):
            self.XlistWidget.addItem(self.VlistWidget.item(i).text())
        self.VlistWidget.clear()
    def removeX(self):
        nrow=self.XlistWidget.currentRow()
        item_str=self.XlistWidget.item(nrow).text()
        self.XlistWidget.takeItem(nrow)
        self.VlistWidget.addItem(item_str)        
        self.VlistWidget.setCurrentRow(0)
    def removeY(self):
        nrow=self.YlistWidget.currentRow()
        item_str=self.YlistWidget.item(nrow).text()
        self.YlistWidget.takeItem(nrow)
        self.VlistWidget.addItem(item_str)
        self.VlistWidget.setCurrentRow(0)
    def addX(self):
        nrow=self.VlistWidget.currentRow()
        item_str=self.VlistWidget.item(nrow).text()
        self.VlistWidget.takeItem(nrow)
        self.XlistWidget.addItem(item_str)
    def addY(self):
        nrow=self.VlistWidget.currentRow()
        item_str=self.VlistWidget.item(nrow).text()
        self.VlistWidget.takeItem(nrow)
        self.YlistWidget.addItem(item_str)
    def plsmodel(self):
        PLS.ncp=self.spinBox.value()
        Lcx=[]
        for i in range(self.XlistWidget.count()):
            Lcx.append(self.XlistWidget.item(i).text())
        ncx=len(Lcx)
        if ncx < 1:
            QtWidgets.QMessageBox.critical(self,'Error',"Wrong X Choice",\
                                           QtWidgets.QMessageBox.Ok)
            return
        Lcy=[]
        for i in range(self.YlistWidget.count()):
            Lcy.append(self.YlistWidget.item(i).text())
        ncy=len(Lcy)
        if ncy < 1:
            QtWidgets.QMessageBox.critical(self,'Error',"Wrong Y Choice",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        DS.Ic=np.in1d(DS.Lc,Lcx+Lcy)
        if PLS.ncp>len(Lcx): PLS.ncp=len(Lcx)
        DS.Gc=np.in1d(DS.Lc,Lcy)
        data=DS.Raw[DS.Ir]
        Y=data[Lcy]
        X=data[Lcx]
        Ts=DS.Ts[DS.Ir]
        X=X[-Ts]
        Y=Y[-Ts]
        Ynan=Y.isnull().sum().sum()
        Xnan=X.isnull().sum().sum()
        if Ynan>0:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  nan in Responce. \n Remove them.".format(Ynan),\
                                           QtWidgets.QMessageBox.Ok)
            return()
        if Xnan>0:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  nan in Factor Matrix. \n Remove them.".format(Xnan),\
                                           QtWidgets.QMessageBox.Ok)
            return()
        PLS.bc=self.centercheckBox.isChecked()
        PLS.bs=self.scalecheckBox.isChecked()
        PLS.bp=self.snvcheckBox.isChecked()
        PLS.Xm,PLS.Ym,PLS.Sx,PLS.Sy,PLS.Xc,PLS.Yc,PLS.SSX,PLS.SSY,PLS.P,PLS.C,\
        PLS.U,PLS.T,PLS.Q,PLS.W,PLS.WS,PLS.B,PLS.Ysc,PLS.Ys,PLS.R2,PLS.SPEX,  \
        PLS.SPEY,PLS.HT2,PLS.VIP,PLS.T95,PLS.T99=                             \
        pls_model(X.values,Y.values,PLS.ncp,PLS.bc,PLS.bs,PLS.bp)
        return()
#
#algoirthm taken from: http://statmaster.sdu.dk/courses/ST02
#Department of Statistics
#ST02: Multivariate Data Analysis and Chemometrics
#Bent Jørgensen and Yuri Goegebeur
#Module 8: Partial least squares regression II        
#
def pls_model(X,Y,ncp,bc,bs,bp):
    X=X.astype('float')
    Y=Y.astype('float')
    nr,ncx = X.shape
    nr,ncy = Y.shape
    if(bp):
        Xm=np.zeros(nr)
        Xm=X.mean(axis=1)
        X=X.T-Xm
        X=X.T
    if(bc):
        Xm=X.mean(axis=0)
        Ym=Y.mean(axis=0)
        X=X-Xm
        Y=Y-Ym
    else:
        Xm=np.zeros(ncx)
        Ym=np.zeros(ncy)
    if(bs):
        Sx=X.std(axis=0)
        Sy=Y.std(axis=0)
        X=X/Sx
        Y=Y/Sy
    else:
        Sx=np.zeros(ncx)
        Sy=np.zeros(ncy)
       
    SSX=(X**2).sum(axis=0)
    SSY=(Y**2).sum(axis=0)
    Ex=X
    Ey=Y
    PP=np.zeros((ncx,ncp))
    CC=np.zeros((ncp,ncp))
    UU=np.zeros((nr,ncp))
    TT=np.zeros((nr,ncp))
    QQ=np.zeros((ncy,ncp))
    WW=np.zeros((ncx,ncp))
    tolerance = 1E-10
    np.random.seed(nr)
    for a in range(ncp):
        u_a_guess=np.random.rand(nr, 1)*2
        u_a = u_a_guess + 1.0
        itern = 0
        while np.linalg.norm(u_a_guess - u_a) > tolerance and itern < 5000:
            u_a_guess = u_a
            w_a=np.dot(Ex.T,u_a_guess)
            w_a=w_a/np.linalg.norm(w_a)
            t_a=np.dot(Ex,w_a)
            q_a=np.dot(Ey.T,t_a)
            q_a=q_a/np.linalg.norm(q_a)
            u_a=np.dot(Ey,q_a)
            itern += 1
        tt=np.dot(t_a.T, t_a)
        c_a=np.dot(t_a.T, u_a)/tt
        p_a=np.dot(Ex.T,t_a)/tt
        Ey=Ey-c_a*np.dot(t_a,q_a.T)
        Ex=Ex-np.dot(t_a,p_a.T)
        PP[:,a]=p_a.ravel() # PP matrix of x-loadings
        UU[:,a]=u_a.ravel() # UU matrix of y-scores
        TT[:,a]=t_a.ravel() # TT matrix of x-scores
        QQ[:,a]=q_a.ravel() # QQ matrix of y-loadings
        WW[:,a]=w_a.ravel() # WW matrix of weights
        CC[a,a]=c_a         # CC diagonal matrix of regression coefficients
    PW=np.dot(PP.T,WW)
    PWINV=np.linalg.inv(PW)
    WPW=np.dot(WW,PWINV)
    WS=np.dot(WPW,CC)
    B=np.dot(WS,QQ.T)
    Ysc=np.dot(np.dot(TT,CC),QQ.T)
    R2=(Y-Ysc)**2
    SPEX=(Ex**2).sum(axis=1)
    SPEY=(Ey**2).sum(axis=1)
    T2=np.dot(TT.T,TT)
    U2=np.dot(UU.T,UU)
    inv_covariance=np.linalg.inv(T2/(nr-1))
    HT2=np.zeros((nr, 1))
    for n in range(nr):
        HT2[n]=np.dot(np.dot(TT[n,:],inv_covariance),TT[n,:].T)
    # from http://www.itl.nist.gov/div898/handbook/pmc/section5/pmc543.htm
    if(nr>ncp):
        T95=(nr-1)*ncp/(nr-ncp)*sp.stats.f.ppf(0.95,ncp,nr-ncp)
        T99=(nr-1)*ncp/(nr-ncp)*sp.stats.f.ppf(0.99,ncp,nr-ncp)
    else:
        T95=T99=0
    TU=np.dot(T2,U2)
    Ss=TU.diagonal()/TU.trace()
    VIP=np.sqrt(np.dot(WW**2,Ss)*ncx)
    Ym=Ym[:,np.newaxis]
    if(bs):
        Sy=Sy[:,np.newaxis]
        Ys=Ym+Sy*Ysc.T
    else:
        Ys=Ysc
    Ys=Ys.T
    return Xm,Ym,Sx,Sy,X,Y,SSX,SSY,PP,CC,UU,TT,QQ,WW,WS,B,Ysc,Ys,R2,SPEX,SPEY,HT2,VIP,T95,T99

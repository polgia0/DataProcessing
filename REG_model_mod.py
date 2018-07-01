from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUiType
from config import DS,REG
import sklearn as sk
import pandas as pd
import scipy as sp
import numpy as np
from matout_mod import matoutDlg
Ui_regmodel,QDialog=loadUiType('regmodel.ui')
class regmodelDlg(QtWidgets.QDialog,Ui_regmodel):
    def __init__(self,parent=None):
        super(regmodelDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.YcomboBox.addItem('None')
        self.YcomboBox.addItems(DS.Lc)
        XYname=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        self.variablelistWidget.addItems(DS.Lc[-np.in1d(DS.Lc,XYname)])
        Xname=XYname[-Gc]
        self.selectedlistWidget.addItems(DS.Lc[np.in1d(DS.Lc,Xname)])
        Yname=XYname[Gc]
        if len(Yname)==1: self.YcomboBox.setCurrentText(Yname[0])
        self.previous=self.YcomboBox.currentText()
        self.includeallcheckBox.clicked.connect(self.allX)
        self.YcomboBox.currentTextChanged.connect(self.ychanged)
        self.variablelistWidget.doubleClicked.connect(self.additem_1)
        self.selectedlistWidget.doubleClicked.connect(self.additem_2)
        self.accepted.connect(self.regmodel)
    def allX(self):
        for i in range(self.variablelistWidget.count()):
            self.selectedlistWidget.addItem(self.variablelistWidget.item(i).text())
        self.variablelistWidget.clear()
    def ychanged(self):
        text=self.YcomboBox.currentText()
        try:
            item_point=self.variablelistWidget.findItems(text,QtCore.Qt.MatchExactly)
            nrow=self.variablelistWidget.row(item_point[0])
            self.variablelistWidget.takeItem(nrow)
        except:
            item_point=self.selectedlistWidget.findItems(text,QtCore.Qt.MatchExactly)
            nrow=self.selectedlistWidget.row(item_point[0])
            self.selectedlistWidget.takeItem(nrow)
        if self.previous != 'None':
            self.variablelistWidget.addItem(self.previous)
        self.previous=text
    def additem_1(self):
        nrow=self.variablelistWidget.currentRow()
        item_str=self.variablelistWidget.item(nrow).text()
        self.variablelistWidget.takeItem(nrow)
        self.selectedlistWidget.addItem(item_str)
    def additem_2(self):
        nrow=self.selectedlistWidget.currentRow()
        item_str=self.selectedlistWidget.item(nrow).text()
        self.variablelistWidget.addItem(item_str)
        self.selectedlistWidget.takeItem(nrow)
    def regmodel(self):
        variables=[]
        for i in range(self.selectedlistWidget.count()):
            variables.append(self.selectedlistWidget.item(i).text())
        ncx=len(variables)
        if ncx<1:
            QtWidgets.QMessageBox.critical(self,'Error',"Too few variables selected!",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        variables.append(self.YcomboBox.currentText())
        REG.normalize=self.normalizecheckBox.isChecked()
        REG.seed=int(self.seedlineEdit.text())
        REG.maxiter=int(self.iterspinBox.value())
        REG.alpha=self.alphadoubleSpinBox.value()
        np.random.seed(REG.seed)
        DS.Ic=np.in1d(DS.Lc,variables)
        DS.Gc=DS.Lc==variables[-1]
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        Y=data[variables[-1]]
        X=data[variables[0: -1]]
        Ts=DS.Ts[DS.Ir]
        Y=Y[-Ts]
        X=X[-Ts]
        Ynan=Y.isnull().sum().sum()
        Xnan=X.isnull().sum().sum()
        if Ynan>0:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  nan in Responce. \n Remove them.".format(Ynan),QtWidgets.QMessageBox.Ok)
            return()
        if Xnan>0:
            QtWidgets.QMessageBox.critical(self,'Error',"There are {}  nan in Factor Matrix. \n Remove them.".format(Xnan),QtWidgets.QMessageBox.Ok)
            return()
        if self.lsqradioButton.isChecked():
            REG.lr=sk.linear_model.LinearRegression(normalize=self.normalizecheckBox.isChecked()).fit(X,Y)
            REG.model='lsq'
        if(self.ridgeradioButton.isChecked()):
            REG.lr=sk.linear_model.Ridge(alpha=self.alphadoubleSpinBox.value(),
            normalize=self.normalizecheckBox.isChecked(),max_iter=REG.getmaxiter()).fit(X,Y)
            REG.model='ridge'
        if self.lassoradioButton.isChecked():
            REG.lr=sk.linear_model.Lasso(alpha=self.alphadoubleSpinBox.value(),
                max_iter=1e5*self.iterspinBox.value(),
                normalize=self.normalizecheckBox.isChecked()).fit(X,Y)
            REG.model='lasso'
        nr,p=X.shape
        Y=Y.values.flatten()
        Ym=np.mean(Y)
        Yhat=REG.lr.predict(X)
        X=np.hstack((np.ones((nr,1)),X))
        #SSR=np.dot(Yhat,Yhat)-nr*Ym**2=np.sum((Yhat-Ym)**2)
        SSR=np.dot(Yhat,Yhat)-nr*Ym**2
        #SSE=SSM=np.dot((Y-Yhat),Y)=np.sum((Yhat-Y)**2)
        SSE=np.dot((Y-Yhat),Y) 
        #SSTO=np.dot(Y,Y)-nr*Ym**2=np.sum((Y-Ym)**2)
        SSTO=np.dot(Y,Y)-nr*Ym**2
        # MSR=MSreg=SSReg/dfreg=SSR/dfreg
        MSR=SSR/p
        # MSE=MSM=SSM/(nr-p)=SSE/(nr-p)
        MSE=SSE/(nr-p-1)
        #F=MSR/MSE=MSreg/MSM
        F=MSR/MSE
        pval=1-sp.stats.f.cdf(F,p,nr-p-1)
        S2=np.dot(Yhat,Y)-nr*Ym**2
        R2=1-SSE/SSTO
        R2adj=R2-(1-R2)*p/(nr-p-1)
        S=np.sqrt(MSE)
        dism=np.linalg.inv(np.dot(X.T,X))
        REG.dism=dism[1:,1:]
        se=S*np.sqrt((dism).diagonal())
        se=np.ravel(se)
        tS=np.insert(REG.lr.coef_,0,REG.lr.intercept_)/se
        REG.dB=S/np.sqrt(nr)*tS
        REG.pS=2*(1-sp.stats.t.cdf(abs(tS),nr-p-1))
        # Coefficients
        #             coef     SE-coef  T-value  P-value
        #              b0      se(0)    tS(0)     pS(0)     
        #              b1      se(1)    tS(1)     pS(1)
        #              df      SS       MS
        # Model summary
        #               S      R-sq     R-sq(adj)
        #               S       R2       R2 adj
        # Analysis of variance
        # Source       DF      SS        MS   F-value P-value        
        # Regression   p       SSR      MSR   F   p
        # Residual     n-(p+1) SSE      MSE
        # Total        n-1     SSTO
        data = np.array([
                        ['Source','DF','SS','MS','F-value','p-value'],
                        ['Regression',str(round(p,0)),str(round(SSR,2)),str(round(MSR,2)),str(round(F,2)),str(round(pval,3))],
                        ['Residual',str(round(nr-(p+1),0)),str(round(SSE,2)),str(round(MSE,2)),'',''],
                        ['Total',str(round(nr-1,0)),str(round(SSTO,2)),'','',''],
                        ['Model','','','','',''],
                        ['','S','R-sq','R-sq(adj)','',''],
                        ['',str(round(S,2)),str(round(R2,2)),str(round(R2adj,2)),'',''],
                        ['Coefficients','','','','',''],
                        ['','Coef.','SE-coef','t-value','p-value','']
                        ])
        data=np.vstack([data,['Intercept',str(round(REG.lr.intercept_,3)),str(round(se[0],2)),str(round(tS[0],2)),str(round(REG.pS[0],3)),'']])
        for i in range(p):
            data=np.vstack([data,[variables[i],str(round(REG.lr.coef_ [i],3)),str(round(se[i+1],2)),str(round(tS[i+1],2)),str(round(REG.pS[i+1],3)),'']])
        dataframe=pd.DataFrame(data)
        matout=QtWidgets.QDialog()
        matout=matoutDlg(parent=self,dataframe=dataframe,bH=False,bV=False)
        matout.exec_()
        matout.show()
        return()

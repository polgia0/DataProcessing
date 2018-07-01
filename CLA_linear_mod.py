from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
import matplotlib.pyplot as plt
import mglearn
import numpy as np
import pandas as pd
from config import DS
Ui_linear,QDialog=loadUiType('linear.ui')
class linearDlg(QtWidgets.QDialog,Ui_linear):
    def __init__(self,parent=None):
        super(linearDlg,self).__init__(parent)
        self.setupUi(self)
        self.XcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.accepted.connect(self.linear)
    def linear(self):
        nx=self.XcomboBox.currentIndex()
        ny=self.YcomboBox.currentIndex()
        if self.l1radioButton.isChecked():
            pen='l1'
        elif self.l2radioButton.isChecked(): 
            pen='l2'
        if self.logisticradioButton.isChecked():
            model=LogisticRegression(penalty=pen)
        elif self.svcradioButton.isChecked():
            model=LinearSVC(penalty=pen)
        y=DS.Gr[DS.Ir]
        X=DS.Raw.iloc[DS.Ir,DS.Ic]
        Ts=DS.Ts[DS.Ir]
        fig,ax=plt.subplots()
        if(nx<0)&(ny<0):
            if y.all()!=None :
                if np.all(DS.Ts==False):
                    QtWidgets.QMessageBox.critical(self,'Error',"There is not any Test Set",QtWidgets.QMessageBox.Ok)
                    return()
                Xtrain=X.iloc[-Ts,:]
                Xtest=X.iloc[Ts,:]
                ytrain=y.iloc[-Ts]
                ytest=y.iloc[Ts]
                clf=model.fit(Xtrain,ytrain.tolist())
                yf=clf.predict(Xtest)
                mask=ytest==yf
                ax.matshow(mask.reshape(1,-1),cmap='gray_r')
                fig.suptitle('Test Set Score {:.2f}'.format(clf.score(Xtest,ytest.tolist())))
                ax.set_xlabel('Sample Index')
            else:
                Lr=DS.Lr[DS.Ir]
                Lr=Lr[pd.isnull(y)]
                Xtest=X[pd.isnull(y),:]
                Xtrain=X[-pd.isnull(y),:]
                ytrain=y[-pd.isnull(y)]
                clf=model.fit(Xtrain,ytrain.tolist())
                ytest=clf.predict(Xtest)
                ind=range(1,len(ytest)+1)
                ax.scatter(ind,ytest,marker='o')
                ax = plt.gca()
                ax.set_xticks(ind)
                ax.set_xticklabels(map(str, Lr.tolist()),rotation='vertical')
                ax.xaxis.grid(True)
                ax.yaxis.grid(True)
        elif ((nx>=0)&(ny<0))|((nx>=0)&(ny<0))|(nx==ny):
            QtWidgets.QMessageBox.critical(self,'Error','Both variables must be choosed and different',QtWidgets.QMessageBox.Ok)
            return()
        else:
            X=X.iloc[:,(nx,ny)]
            clf=model.fit(X,y.tolist())
            mglearn.plots.plot_2d_classification(clf,X.values,ax=ax,fill=False,alpha=0.7)
            mglearn.discrete_scatter(X.iloc[:,0],X.iloc[:,1],y,ax=ax)
            ax.set_title("{}".format(clf.__class__.__name__))
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
        fig.show()

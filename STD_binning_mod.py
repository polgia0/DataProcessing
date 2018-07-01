from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import math
import numpy as np
import scipy.stats as stats
import pandas as pd
from matout_mod import matoutDlg
Ui_binning,QDialog=loadUiType('binning.ui')
class binningDlg(QtWidgets.QDialog,Ui_binning):
    def __init__(self,parent=None):
        super(binningDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        for x in ["mean","median","count","sum"]:
            self.statisticcomboBox.addItem(x)
        self.variablecomboBox.addItem('All')
        self.variablecomboBox.addItems(DS.Lc[DS.Ic])
        self.variablecomboBox.currentTextChanged.connect(self.change)
        self.groupcheckBox.clicked.connect(self.changeGroup)
        self.buttonBox.accepted.connect(self.binning)
        self.data=DS.Raw.loc[DS.Ir,DS.Ic]
        self.change()
    def changeGroup(self):
        Gr=DS.Gr[DS.Ir]
        Grg=pd.Series(Gr).groupby(Gr)    
        if Grg.ngroups<=1:
            QtWidgets.QMessageBox.critical(self,'Error','Groups must be more than one!',\
                                           QtWidgets.QMessageBox.Ok)
    def change(self):
        if self.variablecomboBox.currentText()!='All':
            x=self.data[self.variablecomboBox.currentText()]
            self.minlineEdit.setText(str(x.min()))
            self.maxlineEdit.setText(str(x.max()))
        else:
            self.minlineEdit.setText('')
            self.maxlineEdit.setText('')
    def binning(self):     
        stat=self.statisticcomboBox.currentText()
        data=self.data
        if self.variablecomboBox.currentText()!='All':
            x=data[self.variablecomboBox.currentText()]
            bmin=float(self.minlineEdit.text())
            bmax=float(self.maxlineEdit.text())
            bnum=int(self.spinBox.value())
            if(sum(x.isnull())>0):
                QtWidgets.QMessageBox.critical(self,'Error',\
                'NAs are present.\n Remove them before binding',\
                                        QtWidgets.QMessageBox.Ok)
                return()           
            vrange=(x.min(),x.max())
            if self.groupcheckBox.isChecked():
                Gr=DS.Gr[DS.Ir]
                dataG=data.groupby(Gr)
                data_bin=pd.DataFrame(columns=data.columns.values)
                index=0
                for gr in dataG.groups.keys():
                    datagr=dataG.get_group(gr)
                    nr,nc=datagr.shape
                    x=datagr[self.variablecomboBox.currentText()]
                    if self.trendcomboBox.currentText()=='Uniform':
                        rn,pn=math.modf(nr/bnum)
                        rn=nr % bnum
                        binnumber=[]
                        for i in range(bnum):
                            for j in range(int(pn)):
                                binnumber.append(i)
                        for i in range(rn):
                            binnumber.append(bnum-1)
                    else:
                        if self.linearadioButton.isChecked():
                            scale=np.linspace(bmin,bmax,len(x))
                        if self.logradioButton.isChecked():
                            scale=np.logspace(bmin,bmax,len(x))
                        if self.smoothcheckBox.isChecked():
                            xsm=np.array(range(nr))
                            A=np.vstack([xsm, np.ones(len(x))]).T
                            m,c=np.linalg.lstsq(A,x)[0]
                            x=m*xsm+c
                        bin_means,bin_edges,binnumber=stats.binned_statistic(x.tolist(),\
                                    scale,statistic=stat,bins=bnum,range=vrange)                    
                    grp_bin=datagr.groupby(binnumber)
                    order=grp_bin.groups.keys()
                    if self.trendcomboBox.currentText()=='Decreasing':
                        order=reversed(list(grp_bin.groups.keys()))
                    for grp in order:
                        data_bin.loc[index]=grp_bin.get_group(grp).mean()
                        index +=1
            else:
                if self.linearadioButton.isChecked():
                    scale=np.linspace(bmin,bmax,len(x))
                if self.logradioButton.isChecked():
                    scale=np.logspace(bmin,bmax,len(x))
                bin_means,bin_edges,binnumber=stats.binned_statistic(x.tolist(),\
                                    scale,statistic=stat,bins=bnum,range=vrange)
                data_bin=pd.DataFrame(bin_means)
        elif self.variablecomboBox.currentText()=='All':
            data_bin=[]
            for ncol in DS.Lc[DS.Ic]:
                x=data[ncol]
                # remove Nan works both for lists and numpy array since v!=v only for NaN
                x=x[x==x]
                bnum=int(self.spinBox.value())
                if self.linearadioButton.isChecked():
                    y=np.array_split(x,bnum)
                if self.logradioButton.isChecked():
                    scale=np.logspace(0,len(x)-1,bnum)
                    y=np.split(x,scale)
                y_m=[]
                for x in y:
                    y_m.append(np.mean(x))
                data_bin.append(y_m)
            data_bin=pd.DataFrame(data_bin,columns=range(1,bnum+1),index=DS.Lc[DS.Ic])
#        self.appExcel=xw.App()
#        wb=xw.books.active
#        sht=wb.sheets[0]
#        sht.range('A1').value=data_bin
#        sht.range('A1').value=None
        matout=QtWidgets.QDialog()
        matout=matoutDlg(parent=self,dataframe=data_bin,bH=True,bV=True)
        matout.exec_()
        matout.show()

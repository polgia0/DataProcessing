from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import pandas as pd
from sklearn.decomposition import PCA as sklPCA
Ui_missing,QDialog=loadUiType('missing.ui')
class missingDlg(QtWidgets.QDialog,Ui_missing):
    def __init__(self,parent=None):
        super(missingDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.CcomboBox.addItem('None')
        self.CcomboBox.addItems(DS.Lc)
        self.componentspinBox.setValue(int(round(DS.Raw.shape[1]*0.75,0)))
        self.buttonBox.accepted.connect(self.missing)
    def missing(self):
        if self.removeradioButton.isChecked():
            if self.rowradioButton.isChecked():
                for i in range(DS.Raw.shape[0]):
                    if(DS.Ir[i]):
                        if not DS.Raw.iloc[i,:].notnull().all():
                            DS.Ir[i]=False
            if self.columnradioButton.isChecked():
                for i in range(DS.Raw.shape[1]):
                    if(DS.Ic[i]):
                        if not DS.Raw.iloc[:,i].notnull().all():
                            DS.Ic[i]=False
        if self.fillradioButton.isChecked():
            if self.forwardradioButton.isChecked():
               if self.CcomboBox.currentText()=='None':
                   DS.Raw=DS.Raw.fillna(method='pad')
               else:
                   try:
                       DS.Raw[self.CcomboBox.currentText()]= \
                       DS.Raw[self.CcomboBox.currentText()].fillna(method='pad')
                   except:
                       QtWidgets.QMessageBox.critical(self,'Error',"I can not make this task",\
                                           QtWidgets.QMessageBox.Ok)
            if self.backwardradioButton.isChecked():
               if self.CcomboBox.currentText()=='None':
                   DS.Raw=DS.Raw.fillna(method='bfill')
               else:
                   try:
                       DS.Raw[self.CcomboBox.currentText()]= \
                       DS.Raw[self.CcomboBox.currentText()].fillna(method='bfill')
                   except:
                       QtWidgets.QMessageBox.critical(self,'Error',"I can not make this task",\
                                           QtWidgets.QMessageBox.Ok)
            if self.constantradioButton.isChecked():
               if self.CcomboBox.currentText()=='None':
                   DS.Raw=DS.Raw.fillna(float(self.lineEdit.text()))
               else:
                   try:
                       DS.Raw[self.CcomboBox.currentText()]= \
                       DS.Raw[self.CcomboBox.currentText()].fillna(float(self.lineEdit.text()))
                   except:
                       QtWidgets.QMessageBox.critical(self,'Error',"I can not make this task",\
                                           QtWidgets.QMessageBox.Ok)
        if self.averageradioButton.isChecked():
            if self.CcomboBox.currentText()=='None':
                DS.Raw=DS.Raw.fillna(DS.Raw.mean())
            else:
                try:
                    DS.Raw[self.CcomboBox.currentText()]= \
                    DS.Raw[self.CcomboBox.currentText()].fillna(DS.Raw[self.CcomboBox.currentText()].mean())
                except:
                    QtWidgets.QMessageBox.critical(self,'Error',"I can not make this task",\
                                       QtWidgets.QMessageBox.Ok)
        if self.interpolateradioButton.isChecked():
            if self.CcomboBox.currentText()=='None':
                DS.Raw=DS.Raw.interpolate()            
            else:
                try:
                    DS.Raw[self.CcomboBox.currentText()]= \
                    DS.Raw[self.CcomboBox.currentText()].interpolate()   
                except:
                    QtWidgets.QMessageBox.critical(self,'Error',"I can not make this task",\
                                       QtWidgets.QMessageBox.Ok)
        if self.pcaradioButton.isChecked():
            bdata=DS.Raw.isnull()
            pdata=DS.Raw.fillna(DS.Raw.mean())
            for n in range(int(self.iterationspinBox.value())):
                mdata=pdata.values
                sklearn_pca=sklPCA(n_components=int(self.componentspinBox.value()))
                datat=sklearn_pca.fit_transform(mdata)
                datat=sklearn_pca.inverse_transform(datat)
                datat=pd.DataFrame(datat,index=pdata.index,columns=pdata.columns)
                pdata[bdata]=datat[bdata]
            DS.Raw=pdata          

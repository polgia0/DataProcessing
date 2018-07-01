from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
Ui_exclude,QDialog=loadUiType('exclude.ui')
class excludeDlg(QtWidgets.QDialog,Ui_exclude):
    def __init__(self,parent=None):
        super(excludeDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.buttonBox.accepted.connect(self.exclude)
    def exclude(self):
        if not (DS.Ty=='float').all():
            QtWidgets.QMessageBox.critical(self,'Error','Dataset not fully numeric. \n Use exclusion by bar menu, after column selection',QtWidgets.QMessageBox.Ok)
            return()
        if self.nullradioButton.isChecked():
            if self.rowradioButton.isChecked():
                c0=(DS.Raw.T==0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not null rows',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ir)):
                        if c0.iloc[i]:
                            DS.Ir[i]=False
            if self.columnradioButton.isChecked():
                c0=(DS.Raw==0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not null columns',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ic)):
                        if c0.iloc[i]:
                            DS.Ic[i]=False
        if self.posradioButton.isChecked():
            if self.rowradioButton.isChecked():
                c0=(DS.Raw.T>0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not positive rows',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ir)):
                        if c0.iloc[i]:
                            DS.Ir[i]=False
            if self.columnradioButton.isChecked():
                c0=(DS.Raw>0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not positive columns',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ic)):
                        if c0.iloc[i]:
                            DS.Ic[i]=False
        if self.negradioButton.isChecked():
            if self.rowradioButton.isChecked():
                c0=(DS.Raw.T<0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not negative rows',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ir)):
                        if c0.iloc[i]:
                            DS.Ir[i]=False
            if self.columnradioButton.isChecked():
                c0=(DS.Raw<0).all()
                if(sum(c0)==0):
                    QtWidgets.QMessageBox.critical(self,'Error','There are not negative columns',QtWidgets.QMessageBox.Ok)
                    return()
                else:
                    for i in range(len(DS.Ic)):
                        if c0.iloc[i]:
                            DS.Ic[i]=False

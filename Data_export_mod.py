from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from config import OSS
Ui_export,QDialog=loadUiType('export.ui')
class exportDlg(QtWidgets.QDialog,Ui_export):
    def __init__(self,parent=None):
        super(exportDlg,self).__init__(parent)
        self.setupUi(self)
        self.lineEdit_1.setText(OSS.d)
        self.lineEdit_2.setText(OSS.s)
        self.lineEdit_3.setText(OSS.f)
        self.lineEdit_4.setText(OSS.t)
        self.accepted.connect(self.export)
    def export(self):
        OSS.d=self.lineEdit_1.Text()
        OSS.s=self.lineEdit_2.Text()
        OSS.f=self.lineEdit_3.Text()
        OSS.t=self.lineEdit_4.Text()
        
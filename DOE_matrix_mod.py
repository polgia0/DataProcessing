from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
import xlwings as xw
from pyDOE import ff2n,fullfact,pbdesign
Ui_doematrix,QDialog=loadUiType('doematrix.ui')
class doematrixDlg(QtWidgets.QDialog,Ui_doematrix):
    def __init__(self,parent=None):
        super(doematrixDlg,self).__init__(parent)
        self.setupUi(self)
        self.accepted.connect(self.doematrix)
    def doematrix(self):
        nf=self.spinBox.value()
        self.appExcel=xw.App()
        wb=xw.books.active
        sht=wb.sheets[0]
        if self.factorialradioButton.isChecked():
            mdoe=ff2n(nf)
        elif self.fullradioButton.isChecked():
            seq=self.lineEdit.text
            seq=seq.split(',')
            factors=len(seq)
            levels=[]
            for i in range(factors):
                levels.extend({int(float(seq[i]))})
            mdoe=fullfact(levels)
        elif self.pbradioButton.isChecked():
            mdoe=pbdesign(nf)
        sht.range('A1').value=mdoe

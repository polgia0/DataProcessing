from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from sklearn.model_selection import train_test_split
from config import DS
Ui_split,QDialog=loadUiType('split.ui')
class splitDlg(QtWidgets.QDialog,Ui_split):
    def __init__(self,parent=None):
        super(splitDlg,self).__init__(parent)
        self.setupUi(self)
        self.accepted.connect(self.split)
    def split(self):
        nr=len(DS.Ts)
        Itrain,Itest=train_test_split(range(nr),
                                      test_size=self.sizespinBox.value()/100,
                                      random_state=self.statespinBox.value())
        DS.Ts[Itrain]=False
        DS.Ts[Itest]=True

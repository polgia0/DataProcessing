from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from config import DS
from sklearn import preprocessing
Ui_groups,QDialog=loadUiType('groups.ui')
class groupsDlg(QtWidgets.QDialog,Ui_groups):
    def __init__(self,parent=None):
        super(groupsDlg,self).__init__(parent)
        self.setupUi(self)
        self.comboBox.addItems(DS.Raw.columns)
        self.accepted.connect(self.groups)
    def groups(self):
        DS.Ic[self.comboBox.currentIndex()]=False
        gr=DS.Raw[self.comboBox.currentText()].copy()
        prep_gr=preprocessing.LabelEncoder().fit(gr[-gr.isnull()])
        gr[gr[-gr.isnull()].index]=prep_gr.transform(gr[-gr.isnull()])
        DS.Gr=gr.values
        DS.Cl=prep_gr.classes_
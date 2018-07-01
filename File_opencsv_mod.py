from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
Ui_openCSV,QDialog=loadUiType('openCSV.ui')
from config import DS,OSS
import pandas as pd
import numpy as np
class opencsvDlg(QtWidgets.QDialog,Ui_openCSV):
    def __init__(self,parent=None):
        super(opencsvDlg,self).__init__(parent)
        self.setupUi(self)
        self.fname=''
        self.openButton.clicked.connect(self.getfile)
        self.okButton.clicked.connect(self.loadfile)
    def getfile(self):
        self.fname=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '','*.csv')
        self.fname=self.fname[0]
        self.sourcelineEdit.setText(self.fname)
    def loadfile(self):
        self.DS=None
        if self.fname=='': return
        if self.EUradioButton.isChecked():
            delimiter=";"
            decimal=","
        if self.USradioButton.isChecked():
            delimiter=","
            decimal="."
        if self.headercheckBox.isChecked():
            header=0
        else:
            header=None
        if self.rownamecheckBox.isChecked():
            index_col=0
        else:
            index_col=None
        try:
            fcsv=pd.read_csv(self.fname,
                            delimiter=delimiter,
                            decimal=decimal,
                            header=header,
                            index_col=index_col,
                            false_values=[OSS.f],
                            true_values=[OSS.t])
            nr,nc=fcsv.shape
            DS.Raw=fcsv
            DS.Ir=np.ones(nr,dtype=bool)
            DS.Ic=np.ones(nc,dtype=bool)
            DS.Gr=np.ones(nr,dtype=int)
            DS.Gc=np.zeros(nc,dtype=bool)
            DS.Lr=np.array(fcsv.index,dtype='<U25')
            DS.Lc=np.array(fcsv.columns,dtype='<U25')
            DS.Cr=np.array(nr*['blue'],dtype='<U25')
            DS.Cc=np.array(nc*['red'],dtype='<U25')
            DS.Ts=np.zeros(nr,dtype=bool)
            DS.Ty=fcsv.dtypes.values
        except:
            pass

from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import pandas as pd
Ui_openXLS,QDialog=loadUiType('openXLS.ui')
class openxlsDlg(QtWidgets.QDialog,Ui_openXLS):
    def __init__(self,parent=None):
        super(openxlsDlg,self).__init__(parent)
        self.setupUi(self)
        self.fname=''
        self.openButton.clicked.connect(self.getfile)
        self.okButton.clicked.connect(self.loadfile)
    def getfile(self):
        self.fname=QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '','*.xls *.xlsx')
        self.fname=self.fname[0]
        self.sourcelineEdit.setText(self.fname)
    def loadfile(self):
        if self.fname=='':return
        if self.headercheckBox.isChecked():
            header=0
        else:
            header=None
        if self.rownamecheckBox.isChecked():
            index_col=0
        else:
            index_col=None
        try:
            fxls=pd.read_excel(self.fname,
                              sheetname=0,
                              header=header,
                              index_col=index_col,
                              na_values='NA')
            nr,nc=fxls.shape
            DS.Raw=fxls
            DS.Ir=np.ones(nr,dtype=bool)
            DS.Ic=np.ones(nc,dtype=bool)
            DS.Gr=np.ones(nr,dtype=int)
            DS.Gc=np.zeros(nc,dtype=bool)
            DS.Lr=np.array(fxls.index,dtype='<U25')
            DS.Lc=np.array(fxls.columns,dtype='<U25')
            DS.Cr=np.array(nr*['blue'],dtype='<U25')
            DS.Cc=np.array(nc*['red'],dtype='<U25')
            DS.Ts=np.zeros(nr,dtype=bool)
            DS.Ty=fxls.dtypes.values
        except:
            pass

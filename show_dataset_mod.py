from PyQt5 import QtCore,QtGui
from config import DS
import numpy as np
import pandas as pd
class FetchingTableModel(QtCore.QAbstractTableModel):
    ROW_BATCH_COUNT=25
    def __init__(self,dataframe,parent=None):
        if DS.Raw.shape[0]<FetchingTableModel.ROW_BATCH_COUNT:
            FetchingTableModel.ROW_BATCH_COUNT=DS.Raw.shape[0]
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data=dataframe.astype('str')
        self.rowsLoaded=FetchingTableModel.ROW_BATCH_COUNT
    def flags(self,index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable
    def rowCount(self,index,parent=None):
        if self._data.shape[0]<=self.rowsLoaded:
            return self._data.shape[0]
        else:
            return self.rowsLoaded
    def columnCount(self,index,parent=None):
        return self._data.shape[1]
    def data(self,index,role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return self._data.values[index.row()][index.column()]
        return None
    def setData(self,index,value,role):
        def ck_ass(value_in,d_type):
            try:
                return np.array([value],dtype=d_type,copy=True)[0]
            except:
                return None
        if not index.isValid():
            return False
        if role != QtCore.Qt.EditRole:
            return False
        row=index.row()
        if row < 0 or row >= len(self._data.values):
            return False
        column=index.column()
        if column < 0 or column >= self._data.columns.size:
            return False
        if row==0 and column>=4:
            value_out=ck_ass(value,type(DS.Ty[0]))
            DS.Ty[column-4]=value_out
        if row==1 and column>=4:
            value_out=ck_ass(value,'bool')
            DS.Gc[column-4]=value_out
        if row==2 and column>=4:
            value_out=ck_ass(value,'str')
            DS.Cc[column-4]=value_out
        if row==3 and column>=4:
            value_out=ck_ass(value,'bool')
            DS.Ic[column-4]=value_out
        if column==0 and row>=4:
            value_out=ck_ass(value,'int')
            value_out=int(value_out)
            DS.Gr[row-4]=value_out
        if column==1 and row>=4:
            value_out=ck_ass(value,'bool')
            DS.Ts[row-4]=value_out
        if column==2 and row>=4:
            value_out=ck_ass(value,'str')
            DS.Cr[row-4]=value_out
        if column==3 and row>=4:
            value_out=ck_ass(value,'bool')
            DS.Ir[row-4]=value_out
        if row>=4 and column>=4:
            value_out=ck_ass(value,DS.Ty[column-4])
            DS.Raw.iloc[row-4,column-4]=value_out
        self._data.values[row][column]=str(value_out)
        self.dataChanged.emit(index,index)
        return True
    def headerData(self,section,orientation,role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[section]
        if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.DisplayRole:
            return str(self._data.index[section])
        if section>3:
            if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.BackgroundRole:
                   if not DS.Ic[section-4]:
                       return QtGui.QBrush(QtCore.Qt.red)
            if orientation == QtCore.Qt.Vertical and role == QtCore.Qt.BackgroundRole:
                   if not DS.Ir[section-4]:
                       return QtGui.QBrush(QtCore.Qt.red)
        return None
    def canFetchMore(self,index):
        if self._data.shape[0] > self.rowsLoaded:
            return True
        else:
            return False
    def fetchMore(self,index):
        reminder=self._data.shape[0]-self.rowsLoaded
        itemsToFetch=min(reminder,FetchingTableModel.ROW_BATCH_COUNT)
        self.beginInsertRows(index,self.rowsLoaded,self.rowsLoaded+itemsToFetch-1)
        self.rowsLoaded += itemsToFetch
        self.endInsertRows()
def prepare_show(self):
    self.view.show()
    self.pushButton_Ir.show()
    self.pushButton_Ic.show()
    self.pushButton_Cr.show()
    self.pushButton_Cc.show()
    self.pushButton_Ts.show()
    self.pushButton_Ty.show()
    self.pushButton_Gc.show()
    self.pushButton_Gr.show()
    self.setGeometry(100,100,800,500)
    self.pushButton_Ir.clicked.connect(self.hide_Ir)
    self.pushButton_Ic.clicked.connect(self.hide_Ic)
    self.pushButton_Cr.clicked.connect(self.hide_Cr)
    self.pushButton_Cc.clicked.connect(self.hide_Cc)
    self.pushButton_Ts.clicked.connect(self.hide_Ts)
    self.pushButton_Ty.clicked.connect(self.hide_Ty)
    self.pushButton_Gc.clicked.connect(self.hide_Gc)
    self.pushButton_Gr.clicked.connect(self.hide_Gr)  
def operate_show(self):
    self.view.hideRow(0)
    self.view.hideRow(1)
    self.view.hideRow(2)
    self.view.hideRow(3)
    self.view.hideColumn(0)
    self.view.hideColumn(1)
    self.view.hideColumn(2)        
    self.view.hideColumn(3)        
def show_dataset(self):
    self.view.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.view.horizontalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.view.verticalHeader().setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.view.customContextMenuRequested.connect(self.show_dataMenu)
    self.view.horizontalHeader().customContextMenuRequested.connect(self.show_barMenu)
    self.view.verticalHeader().customContextMenuRequested.connect(self.show_barMenu)
    MD=np.vstack((DS.Gr.astype('str'),
          DS.Ts.astype('str'),
          DS.Cr.astype('str'),
          DS.Ir.astype('str'))).T
    TM=np.vstack((np.hstack((np.array(['','','','']),DS.Ty.astype('str'))),
                 np.hstack((np.array(['','','','']),DS.Gc.astype('str'))),
                 np.hstack((np.array(['','','','']),DS.Cc.astype('str'))),
                 np.hstack((np.array(['','','','']),DS.Ic.astype('str')))))
    MM=np.concatenate((TM,np.concatenate((MD,DS.Raw.astype('str')),axis=1)),axis=0)
    data=pd.DataFrame(MM,columns=['Group','Test','Color','Include']+DS.Lc.tolist(),
                      index=['Type','Responce','Color','Include']+DS.Lr.tolist())
    self.model=FetchingTableModel(dataframe=data)
    #self.view.horizontalHeader().setStretchLastSection(True)
    self.view.verticalHeader().setFixedWidth(30)
    self.view.setModel(self.model)
    self.timer=QtCore.QBasicTimer()
    self.timerPeriod=100
    self.timer.start(self.timerPeriod,self)
    self.progressBar.setRange(0,DS.Raw.shape[0])
    self.progressBar.setValue(0)
    self.progressBar.show()
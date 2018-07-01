from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.uic import loadUiType
from config import OSS
import numpy as np
Ui_matout,QDialog=loadUiType('matout.ui')
class matoutDlg(QtWidgets.QDialog,Ui_matout):
    def __init__(self,parent=None,dataframe=None,bH=None,bV=None):
        super(matoutDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        rows,columns=dataframe.shape
        model=QtGui.QStandardItemModel()
        for row in range(rows):
            items=[]
            for column in range(columns):
                field =dataframe.iat[row, column]
                text = str(field)
                if isinstance(field, np.number):
                    data = field.item()
                    text=text.replace('.',OSS.d)
                else:
                    data = text
                item = QtGui.QStandardItem(text)
                item.setData(data, QtCore.Qt.UserRole)
                items.append(item)
            model.appendRow(items)
        self.tableView.setShowGrid(False)
        vh=self.tableView.verticalHeader()
        vh.setVisible(False)
        if(bV):vh.setVisible(True)
        hh=self.tableView.horizontalHeader()
        hh.setVisible(False)
        if(bH):hh.setVisible(True)
        hh.setStretchLastSection(True)
        self.tableView.setModel(model)
        if(bH):model.setHorizontalHeaderLabels(dataframe.columns.astype('str'))
        if(bV):model.setVerticalHeaderLabels(dataframe.index.astype('str'))
        self.tableView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.view_dataMenu)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.clip=QtWidgets.QApplication.clipboard()
    def view_dataMenu(self,pos):
        menu=QtWidgets.QMenu()
        copy_action=menu.addAction("Copy Selection")
        all_action=menu.addAction("Copy All")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==copy_action:
            rows=sorted(set(index.row() for index in self.tableView.selectedIndexes()))
            columns=sorted(set(index.column() for index in self.tableView.selectedIndexes()))
            model=self.tableView.model()
            bV=self.tableView.verticalHeader().isVisible()
            bH=self.tableView.horizontalHeader().isVisible()
            data=[]
            if(bH):
                data = [OSS.sep]
                for column in columns:
                  data.append(model.horizontalHeaderItem(column).text())
                  data.append(OSS.sep)
                data.append(OSS.nl)    
            for row in rows:
              if(bV):
                  data.append(model.verticalHeaderItem(row).text())
                  data.append(OSS.sep)
              for column in columns:
                index = model.index(row, column)
                data.append(model.data(index))
                data.append(OSS.sep)
              data.append(OSS.nl)
            self.clip.setText(''.join(data))
        if action==all_action:
            model=self.tableView.model()
            bV=self.tableView.verticalHeader().isVisible()
            bH=self.tableView.horizontalHeader().isVisible()
            data=[]
            if(bH):
                data = [OSS.sep]
                for column in range(model.columnCount()):
                  data.append(model.horizontalHeaderItem(column).text())
                  data.append(OSS.sep)
                data.append(OSS.nl)    
            for row in range(model.rowCount()):
              if(bV):
                  data.append(model.verticalHeaderItem(row).text())
                  data.append(OSS.sep)
              for column in range(model.columnCount()):
                index = model.index(row, column)
                data.append(model.data(index))
                data.append(OSS.sep)
              data.append(OSS.nl)
            self.clip.setText(''.join(data))
    

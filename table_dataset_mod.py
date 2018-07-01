from PyQt5 import QtWidgets,QtCore
from show_dataset_mod import show_dataset
from Data_split_mod import splitDlg
from sklearn import preprocessing
from config import DS
import numpy as np
def show_dataMenu(self,pos):
    if len(self.view.selectedIndexes())>0:
        n_r0=self.view.selectedIndexes()[0].row()
        n_c0=self.view.selectedIndexes()[0].column()
        n_r1=self.view.selectedIndexes()[-1].row()
        n_c1=self.view.selectedIndexes()[-1].column()
    else:
        return()
    menu=QtWidgets.QMenu()
    items_type=('integer','float','boolean','string')
    if n_r0>=4 and n_c0>=4:
        clear_action=menu.addAction("Clear")
        change_action=menu.addAction("Change to...")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==clear_action:
           for index in self.view.selectedIndexes():
               self.view.model().setData(index,'nan',QtCore.Qt.EditRole)
        if action==change_action:
            value_text,ok=QtWidgets.QInputDialog.getText(self,'Input Dialog', 'Enter the value:')
            if ok:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,value_text,QtCore.Qt.EditRole)
    if n_r0==3 and n_r1==3 and n_c0>3:
        change_true=menu.addAction("Change to True")
        change_false=menu.addAction("Change to False")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==change_true:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,True,QtCore.Qt.EditRole)
        if action==change_false:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,False,QtCore.Qt.EditRole)
    if n_c0==3 and n_c1==3 and n_r0>3:
        change_true=menu.addAction("Change to True")
        change_false=menu.addAction("Change to False")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==change_true:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,True,QtCore.Qt.EditRole)
        if action==change_false:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,False,QtCore.Qt.EditRole)
    if n_r0==2 and n_r1==2 and n_c0>3:
        item=QtWidgets.QColorDialog.getColor()
        if item.name()=='#000000': return()
        for index in self.view.selectedIndexes():
            self.view.model().setData(index,item.name(),QtCore.Qt.EditRole)
    if n_c0==2 and n_c1==2 and n_r0>3:
        item=QtWidgets.QColorDialog.getColor()
        if item.name()=='#000000': return()
        for index in self.view.selectedIndexes():
            self.view.model().setData(index,item.name(),QtCore.Qt.EditRole)
    if n_r0==1 and n_r1==1 and n_c0>3:
        change_true=menu.addAction("Change to True")
        change_false=menu.addAction("Change to False")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==change_true:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,'True',QtCore.Qt.EditRole)
        if action==change_false:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,'False',QtCore.Qt.EditRole)
    if n_c0==0 and n_c1==0 and n_r0>3:
        clear_action=menu.addAction("Clear")
        change_action=menu.addAction("Change group")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==clear_action:
           for index in self.view.selectedIndexes():
               self.view.model().setData(index,'nan',QtCore.Qt.EditRole)
        if action==change_action:
            i,ok=QtWidgets.QInputDialog.getInt(self,'Input Dialog', "Group #",1,0,100)
            if ok:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,str(i),QtCore.Qt.EditRole)
    if n_r0==0 and n_r1==0 and n_c0>3:
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for index in self.view.selectedIndexes():
            self.view.selectColumn(index.column())
        item,ok=QtWidgets.QInputDialog.getItem(self,'Input Dialog', "Types",items_type, 0, False)
        if ok:
          if item=='integer':
            for index in sorted(self.view.selectionModel().selectedColumns()):
                self.view.model().setData(index,np.dtype('int'),QtCore.Qt.EditRole)
                try:
                   DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('int')
                except:
                   DS.Raw.iloc[:,index.column()-4]=None
            for index in sorted(self.view.selectionModel().selectedIndexes()):
                if index.row()>=4:
                    self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('int')),QtCore.Qt.EditRole)
          elif item=='float':
            for index in sorted(self.view.selectionModel().selectedColumns()):
                self.view.model().setData(index,np.dtype('float'),QtCore.Qt.EditRole)
                try:
                   DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('float')
                except:
                   DS.Raw.iloc[:,index.column()-4]=None
            for index in sorted(self.view.selectionModel().selectedIndexes()):
                if index.row()>=4:
                    self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('float')),QtCore.Qt.EditRole)
          elif item=='boolean':
            for index in sorted(self.view.selectionModel().selectedColumns()):
                self.view.model().setData(index,np.dtype('bool'),QtCore.Qt.EditRole)
                try:
                   DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('bool')
                except:
                   DS.Raw.iloc[:,index.column()-4]=None
            for index in sorted(self.view.selectionModel().selectedIndexes()):
                if index.row()>=4:
                    self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('bool')),QtCore.Qt.EditRole)
          elif item=='string':
            for index in sorted(self.view.selectionModel().selectedColumns()):
                self.view.model().setData(index,np.dtype('str'),QtCore.Qt.EditRole)
                try:
                   DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('str')
                except:
                   DS.Raw.iloc[:,index.column()-4]=None
            for index in sorted(self.view.selectionModel().selectedIndexes()):
                if index.row()>=4:
                    self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('str')),QtCore.Qt.EditRole)
        self.view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    if n_c0==1 and n_c1==1 and n_r0>3:
        change_true=menu.addAction("Change to True")
        change_false=menu.addAction("Change to False")
        action = menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==change_true:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,True,QtCore.Qt.EditRole)
        if action==change_false:
               for index in self.view.selectedIndexes():
                   self.view.model().setData(index,False,QtCore.Qt.EditRole)
    else:
        return()
def show_barMenu(self,pos):
    ind_row=self.view.selectionModel().selectedRows()
    ind_col=self.view.selectionModel().selectedColumns()
    items_type=('integer','float','boolean','string')
    menu = QtWidgets.QMenu()
    if len(ind_row)>0 and len(ind_col)==0:
        include_action=menu.addAction("Include")
        exclude_action=menu.addAction("Exclude")
        action=menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==include_action:
            for index in sorted(ind_row):
                index_Ir=self.view.model().index(index.row(),3)
                self.view.model().setData(index_Ir,True,QtCore.Qt.EditRole)
            return()
        if action==exclude_action:
            for index in sorted(ind_row):
                index_Ir=self.view.model().index(index.row(),3)
                self.view.model().setData(index_Ir,False,QtCore.Qt.EditRole)
            return()
    if len(ind_row)==0 and len(ind_col)>0:
        menu_ex= QtWidgets.QMenu('Exclude...')
        nan_action=menu_ex.addAction('NA')
        null_action=menu_ex.addAction('0')
        mag_action=menu_ex.addAction('>')
        min_action=menu_ex.addAction('<')
        include_action=menu.addAction("Include")
        exclude_action=menu.addAction("Exclude")
        type_action=menu.addAction("Type...")
        sety_action=menu.addAction("Set...")
        menu.addMenu(menu_ex)
        sort_action=None
        split_action=None
        if len(ind_col)==1:
            sort_action=menu.addAction("Sort...")
            if ind_col[0].column()==1:
                split_action=menu.addAction("Split...")
        action=menu.exec_(self.mapToGlobal(pos))
        if action==None:
            return()
        if action==include_action:
            for index in sorted(ind_col):
                index_Ir=self.view.model().index(3,index.column())
                self.view.model().setData(index_Ir,True,QtCore.Qt.EditRole)
        if action==exclude_action:
            for index in sorted(ind_col):
                index_Ir=self.view.model().index(3,index.column())
                self.view.model().setData(index_Ir,False,QtCore.Qt.EditRole)
        if action==type_action:
            item,ok=QtWidgets.QInputDialog.getItem(self,'Input Dialog', "Types",items_type, 0, False)
            if ok:
                  if item=='integer':
                    for index in sorted(ind_col):
                        self.view.model().setData(index,np.dtype('int'),QtCore.Qt.EditRole)
                        try:
                           DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('int')
                        except:
                           DS.Raw.iloc[:,index.column()-4]=None
                    for index in sorted(self.view.selectionModel().selectedIndexes()):
                        if index.row()>=4:
                            self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('int')),QtCore.Qt.EditRole)
                  elif item=='float':
                    for index in sorted(ind_col):
                        self.view.model().setData(index,np.dtype('float'),QtCore.Qt.EditRole)
                        try:
                           DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('float')
                        except:
                           DS.Raw.iloc[:,index.column()-4]=None
                    for index in sorted(self.view.selectionModel().selectedIndexes()):
                        if index.row()>=4:
                            self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('float')),QtCore.Qt.EditRole)
                  elif item=='boolean':
                    for index in sorted(ind_col):
                        self.view.model().setData(index,np.dtype('bool'),QtCore.Qt.EditRole)
                        try:
                           DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('bool')
                        except:
                           DS.Raw.iloc[:,index.column()-4]=None
                    for index in sorted(self.view.selectionModel().selectedIndexes()):
                        if index.row()>=4:
                            self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('bool')),QtCore.Qt.EditRole)
                  elif item=='string':
                    for index in sorted(ind_col):
                        self.view.model().setData(index,np.dtype('str'),QtCore.Qt.EditRole)
                        try:
                           DS.Raw.iloc[:,index.column()-4]=DS.Raw.iloc[:,index.column()-4].astype('str')
                        except:
                           DS.Raw.iloc[:,index.column()-4]=None
                    for index in sorted(self.view.selectionModel().selectedIndexes()):
                        if index.row()>=4:
                            self.view.model().setData(index,str(DS.Raw.iloc[index.row()-4,index.column()-4].astype('str')),QtCore.Qt.EditRole)
        if action==sety_action:
            item,ok=QtWidgets.QInputDialog.getItem(self,'Input Dialog', "Set as",('Responce','Factor','Group','Label'), 0, False)
            if ok:
                if item=='Responce':
                   for index in sorted(ind_col):
                        index_Gc=self.view.model().index(1,index.column())
                        self.view.model().setData(index_Gc,True,QtCore.Qt.EditRole)
                        DS.Gc[index.column()-4]=True
                if item=='Factor':
                   for index in sorted(ind_col):
                        index_Gc=self.view.model().index(1,index.column())
                        self.view.model().setData(index_Gc,True,QtCore.Qt.EditRole)
                        DS.Gc[index.column()-4]=False
                if item=='Group':
                    if len(ind_col)>1:
                        QtWidgets.QMessageBox.critical(self,'Error',"Please select only one column!",\
                                  QtWidgets.QMessageBox.Ok)
                    else:
                        nc=ind_col[0].column()
                        DS.Ic[nc-4]=False
                        gr=DS.Raw.iloc[:,nc-4].copy()
                        prep_gr=preprocessing.LabelEncoder().fit(gr[-gr.isnull()])
                        gr[gr[-gr.isnull()].index]=prep_gr.transform(gr[-gr.isnull()])
                        DS.Gr=gr.values
                        DS.Cl=prep_gr.classes_
                if item=='Label':
                    if len(ind_col)>1:
                        QtWidgets.QMessageBox.critical(self,'Error',"Please select only one column!",\
                                  QtWidgets.QMessageBox.Ok)
                    else:
                        nc=ind_col[0].column()
                        DS.Ic[nc-4]=False
                        Lr=DS.Raw.iloc[:,nc-4].copy()
                        DS.Lr=Lr.values.astype('str')
                        DS.Raw.index=Lr
        if action==nan_action:
            for index in sorted(ind_col):
                nc=index.column()-4
                for i in range(DS.Raw.shape[0]):
                    if(DS.Ir[i]):
                        if np.isnan(DS.Raw.iloc[i,nc]):
                                    DS.Ir[i]=False
        if action==sort_action:
            item,ok=QtWidgets.QInputDialog.getItem(self,'Input Dialog', "Sort",('Decreasing','Increasing'), 0, False)
            if ok:
                DS.Raw['Ir']=DS.Ir
                DS.Raw['Cr']=DS.Cr
                DS.Raw['Lr']=DS.Lr
                DS.Raw['Ts']=DS.Ts
                DS.Raw['Gr']=DS.Gr
                nc=ind_col[0].column()
                if nc==0: vs='Gr'
                if nc==1: vs='Ts'
                if nc==2: vs='Cr'
                if nc==3: vs='Lr'
                if nc==4: vs='Ir'
                if nc>4: vs=DS.Lc[nc-4]
                if item=='Decreasing':
                    DS.Raw.sort_values(by=vs,axis=0,ascending=False,inplace=True,kind='quicksort', na_position='last')
                if item=='Increasing':
                    DS.Raw.sort_values(by=vs,axis=0,ascending=True,inplace=True,kind='quicksort', na_position='last')
                DS.Ir=DS.Raw['Ir'].values
                DS.Cr=DS.Raw['Cr'].values
                DS.Lr=DS.Raw['Lr'].values
                DS.Ts=DS.Raw['Ts'].values
                DS.Gr=DS.Raw['Gr'].values
                DS.Raw=DS.Raw.loc[:,DS.Lc]
        if action==split_action:
            split=QtWidgets.QDialog()
            split=splitDlg()
            split.exec_()
            split.show()
            for r in range(4,len(DS.Ts)+4):
                self.view.item(r,1).setText(str(DS.Ts[r-4]))
        if action==null_action:
           selection=list(self.view.selectionModel().selection())
           selection.sort()
           n0=selection[0].left()-4
           n1=selection[-1].right()-4
           for ic in range(n0,n1+1):
               c0=DS.Raw.iloc[:,ic]==0
               for i in range(len(DS.Ir)):
                   if c0.iloc[i]:
                       DS.Ir[i]=False
        if action==mag_action:
           value,ok=QtWidgets.QInputDialog.getText(self, 'Input Dialog','Enter the value:')
           if ok:
               selection=list(self.view.selectionModel().selection())
               selection.sort()
               n0=selection[0].left()-4
               n1=selection[-1].right()-4
               for ic in range(n0,n1+1):
                   c0=DS.Raw.iloc[:,ic]>float(value)
                   for i in range(len(DS.Ir)):
                       if c0.iloc[i]:
                           DS.Ir[i]=False
        if action==min_action:
           value,ok=QtWidgets.QInputDialog.getText(self, 'Input Dialog','Enter the value:')
           if ok:
               selection=list(self.view.selectionModel().selection())
               selection.sort()
               n0=selection[0].left()-4
               n1=selection[-1].right()-4
               for ic in range(n0,n1+1):
                   c0=DS.Raw.iloc[:,ic]<float(value)
                   for i in range(len(DS.Ir)):
                       if c0.iloc[i]:
                           DS.Ir[i]=False  
        show_dataset(self)
def hide_Ir(self):
    if self.view.isColumnHidden(3):
        self.view.showColumn(3)
    else:
        self.view.hideColumn(3)        
def hide_Ic(self):
   if self.view.isRowHidden(3):
       self.view.showRow(3)
   else:
       self.view.hideRow(3)      
def hide_Cr(self):
    if self.view.isColumnHidden(2):
        self.view.showColumn(2)
    else:
        self.view.hideColumn(2)        
def hide_Cc(self):
   if self.view.isRowHidden(2):
       self.view.showRow(2)
   else:
       self.view.hideRow(2)      
def hide_Gr(self):
    if self.view.isColumnHidden(0):
        self.view.showColumn(0)
    else:
        self.view.hideColumn(0)        
def hide_Gc(self):
   if self.view.isRowHidden(1):
       self.view.showRow(1)
   else:
       self.view.hideRow(1)      
def hide_Ts(self):
    if self.view.isColumnHidden(1):
        self.view.showColumn(1)
    else:
        self.view.hideColumn(1)        
def hide_Ty(self):
   if self.view.isRowHidden(0):
       self.view.showRow(0)
   else:
       self.view.hideRow(0)      


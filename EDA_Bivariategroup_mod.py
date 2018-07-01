from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import pandas as pd
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_bivariategroup,QDialog=loadUiType('bivariategroup.ui')
class bivariategroupDlg(QtWidgets.QDialog,Ui_bivariategroup):
    def __init__(self,parent=None):
        super(bivariategroupDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItem('Auto')
        self.Y2comboBox.addItem('None')
        self.XcomboBox.addItems(DS.Lc[DS.Ic])
        self.Y1comboBox.addItems(DS.Lc[DS.Ic])
        self.Y2comboBox.addItems(DS.Lc[DS.Ic])
        self.XcomboBox.setCurrentIndex(0)
        self.Y1comboBox.setCurrentIndex(0)
        self.Y2comboBox.setCurrentIndex(0)
        self.PcheckBox.setChecked(True)
        self.XGcheckBox.setChecked(True)
        self.YGcheckBox.setChecked(True)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.ApplyButton.clicked.connect(self.redraw)
        self.ResetButton.clicked.connect(self.reset)
        self.farwardButton.clicked.connect(self.farward)
        self.backwardButton.clicked.connect(self.backward)
        fig=Figure()
        ax=fig.add_subplot(111)
        ax.plot(np.array(0))
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.addmpl(fig)
        self.id_group=0
    def redraw(self):
        if self.XcomboBox.currentText()==self.Y1comboBox.currentText() or   \
            self.XcomboBox.currentText()==self.Y2comboBox.currentText() :
            QtWidgets.QMessageBox.critical(self,'Error',"Variables \n must be different !",QtWidgets.QMessageBox.Ok)
            return()
        groups=pd.Series(DS.Gr)
        if groups.isnull().all():
            QtWidgets.QMessageBox.critical(self,'Error',"Not all groups are defined !",QtWidgets.QMessageBox.Ok)
            return()
        groups=groups.astype('int')
        gr_type=[isinstance(e, (int, np.integer)) for e in groups]
        if sum(gr_type)!=len(groups):
            QtWidgets.QMessageBox.critical(self,'Error',"Groups must be all present \n and must be integers",QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        Lr=DS.Lr[DS.Ir]
        Cr=DS.Cr[DS.Ir]
        fig = Figure()
        color='blue'
        color1='blue'
        Y1=data[self.Y1comboBox.currentText()]
        if self.CcheckBox.isChecked():
             color=DS.Cc[self.Y1comboBox.currentIndex()-1]
        if self.Y2comboBox.currentText()=="None":
            dual=False
            Y2=Y1
        else:
            dual=True
            Y2=data[self.Y2comboBox.currentText()]
            if self.CcheckBox.isChecked():
                 color1=DS.Cc[self.Y2comboBox.currentIndex()-2]
        if self.XcomboBox.currentText()=='Auto':
            auto=True
            X=Y1
        else:
            auto=False
            X=data[self.XcomboBox.currentText()]
        df=pd.DataFrame({'G': groups.values,'X': X,'Y1': Y1,'Y2': Y2,'C':Cr,'L':Lr})
        dfg=df.groupby(['G'])
        ngr=len(dfg)
        if(ngr==1):
            QtWidgets.QMessageBox.critical(self,'Error','Your data have just one group.\n Slide Show needs more than a single group.',QtWidgets.QMessageBox.Ok)
            return()
        groups=df.G.unique()
        if(auto):
            X=[]
            for gr in groups:
                grp=dfg.get_group(gr)
                X=X+list(range(len(grp['X'])))
            df['X']=X
        if(self.slideradioButton.isChecked()):
            if dual:
                ax=fig.add_subplot(1,2,1)
            else:
                ax=fig.add_subplot(1,1,1)
            if(self.id_group>ngr-1):
                QtWidgets.QMessageBox.critical(self,'Error','Highest element of list is reached',QtWidgets.QMessageBox.Ok)
                self.id_group=ngr-1
                return()
            if(self.id_group<0):
                QtWidgets.QMessageBox.critical(self,'Error','Lowest element of list is reached',QtWidgets.QMessageBox.Ok)
                self.id_group=0
                return()
            min_X=df['X'].min()
            max_X=df['X'].max()
            min_Y1=df['Y1'].min()
            max_Y1=df['Y1'].max()
            min_Y2=df['Y2'].min()
            max_Y2=df['Y2'].max()
            M=dfg.get_group(groups[self.id_group])
            ax.set_xlim([min_X,max_X])
            ax.set_ylim([min_Y1,max_Y1])
            if self.PcheckBox.isChecked():
                ax.scatter(M['X'],M['Y1'],marker='o',color=color)
            if self.LcheckBox.isChecked():
                ax.plot(M['X'],M['Y1'],linestyle='-',color=color)
            ax.xaxis.grid()
            ax.yaxis.grid()
            ax.set_ylabel(self.Y1comboBox.currentText())
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_title('Group: '+str(groups[self.id_group]))
            if dual:
                ax1=fig.add_subplot(1,2,2)
                ax1.set_xlim([min_X,max_X])
                ax1.set_ylim([min_Y2,max_Y2])
                if self.PcheckBox.isChecked():
                    ax1.scatter(M['X'],M['Y2'],marker='o',color=color1)
                if self.LcheckBox.isChecked():
                    ax1.plot(M['X'],M['Y2'],linestyle='-',color=color1)
                ax1.xaxis.grid()
                ax1.yaxis.grid()
                ax1.set_title('Group:'+str(groups[self.id_group]))
                ax1.set_xlabel(self.XcomboBox.currentText())
                ax1.set_ylabel(self.Y2comboBox.currentText())
        if(self.conditioningradioButton.isChecked()):
            if dual:
                ax=fig.add_subplot(1,2,1)
            else:
                ax=fig.add_subplot(1,1,1)
            for key, grp in df.groupby(['G']):
                if self.CcheckBox.isChecked():
                    vcol=grp['C']
                else:
                    vcol=cm.viridis.colors[int(len(cm.viridis.colors)/ngr*key)]
                if self.PcheckBox.isChecked():
                    ax.scatter(grp['X'],grp['Y1'],color=vcol,marker='o',label=key)
                if self.LcheckBox.isChecked():
                    ax.plot(grp['X'],grp['Y1'],linestyle='-',color=vcol,label=key)
            ax.xaxis.grid()
            ax.yaxis.grid()
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.Y1comboBox.currentText())
            ax.legend(loc='best')  
            if dual:
                ax1=fig.add_subplot(1,2,2)
                for key, grp in df.groupby(['G']):
                    if self.CcheckBox.isChecked():
                        vcol=grp['C']
                    else:
                        vcol=cm.viridis.colors[int(len(cm.viridis.colors)/ngr*key)]
                    if self.PcheckBox.isChecked():
                        ax1.scatter(grp['X'],grp['Y2'],color=vcol,marker='o',label=key)
                    if self.LcheckBox.isChecked():
                        ax1.plot(grp['X'],grp['Y2'],linestyle='-',color=vcol,label=key)
                ax1.xaxis.grid()
                ax1.yaxis.grid()
                ax1.set_xlabel(self.XcomboBox.currentText())
                ax1.set_ylabel(self.Y2comboBox.currentText())
                ax1.legend(loc='best')  
        if(self.scatteradioButton.isChecked()):
            ax=fig.add_subplot(1,1,1)
            if dual:
                ax1=ax.twinx()
            for key, grp in df.groupby(['G']):
                if self.CcheckBox.isChecked():
                    vcol=grp['C']
                else:
                    vcol=cm.viridis.colors[int(len(cm.viridis.colors)/ngr*key)]
                if self.PcheckBox.isChecked():
                    ax.scatter(grp['X'],grp['Y1'],color=vcol,marker='o',label=key)
                    if dual:
                        ax1.scatter(grp['X'],grp['Y2'],color=vcol,marker='*',label=key)
                if self.LcheckBox.isChecked():
                    ax.plot(grp['X'],grp['Y1'],linestyle='-',color=vcol,label=key)
                    if dual:
                        ax1.plot(grp['X'],grp['Y2'],linestyle='-',color=vcol,label=key)
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.Y1comboBox.currentText())
            if dual:
                ax1.set_ylabel(self.Y2comboBox.currentText())
            ax.legend(loc='best')  
        if self.XcheckBox.isChecked():
            if self.XlineEdit.text():
                ax.set_xlabel(self.XlineEdit.text())
                if dual:
                    ax1.set_xlabel(self.XlineEdit.text())
        else:
            ax.set_xlabel('')
            if dual:
                ax1.set_xlabel('')  
        if self.XGcheckBox.isChecked():
            ax.xaxis.grid(True)
            if dual:
                ax1.xaxis.grid(True)
        else:
            ax.xaxis.grid(False)
            if dual:
                ax1.xaxis.grid(False)
        if self.XGcheckBox.isChecked():
            ax.xaxis.grid(True)
        if self.YGcheckBox.isChecked():
            ax.yaxis.grid(True)
            if dual:
                ax1.yaxis.grid(True)
        if not self.XMcheckBox.isChecked():    
            ax.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
            if dual:
                ax1.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
        if not self.YMcheckBox.isChecked():
            ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
            if dual:
                ax1.tick_params(axis='y',which='both',bottom='off',top='off',labelbottom='off')
        self.rmmpl()
        self.addmpl(fig)        
    def farward(self):
        self.id_group +=1
        self.redraw()
    def backward(self):
        self.id_group -=1
        self.redraw()
    def reset(self):
        self.XcomboBox.setCurrentIndex(0)
        self.Y1comboBox.setCurrentIndex(0)
        self.Y2comboBox.setCurrentIndex(0)
        self.PcheckBox.setChecked(True)
        self.LcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(True)
        self.YGcheckBox.setChecked(True)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.XlineEdit.setText('')
        self.YlineEdit.setText('')
        self.TlineEdit.setText('')
        self.update()        
    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(self.canvas, 
                self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)
    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_univariategroup,QDialog=loadUiType('univariategroup.ui')
class univariategroupDlg(QtWidgets.QDialog,Ui_univariategroup):
    def __init__(self,parent=None):
        super(univariategroupDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.setCurrentIndex(0)
        self.TcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(True)
        self.YGcheckBox.setChecked(True)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.ApplyButton.clicked.connect(self.redraw)
        self.ResetButton.clicked.connect(self.reset)
        fig=Figure()
        ax=fig.add_subplot(111)
        ax.plot(np.array(0))
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.addmpl(fig)
    def redraw(self):
        groups=pd.Series(DS.Gr[DS.Ir],dtype='int')
        gr_type=[isinstance(e, (int,np.integer)) for e in groups]
        if sum(gr_type)!=len(groups):
            QtWidgets.QMessageBox.critical(self,'Error',"Groups must be all present \n and must be integers",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw[DS.Ir]
        data=data[self.YcomboBox.currentText()]
        if data.shape[1]!=1:
            QtWidgets.QMessageBox.critical(self,'Error',"More columns have the same name",\
                                           QtWidgets.QMessageBox.Ok)
            return()    
        YG=pd.DataFrame({'G':groups.values,'Y': data.values,'Cr':DS.Cr[DS.Ir],'Lr':DS.Lr[DS.Ir]})
        YG=YG[~data.isnull().values]
        YGg=YG.groupby(['G'])
        ngr=len(YGg)
        color='blue'
        fig=Figure()
        ax=fig.add_subplot(111)
        if self.CcheckBox.isChecked():
             color=DS.Cc[self.YcomboBox.currentIndex()-1]
        if(self.BoxradioButton.isChecked()):
            plt.hold = True
            boxes=[]
            nbox=[]
            medianprops=dict(marker='D',markeredgecolor='black',markerfacecolor=color)
            for key, grp in YGg:
                nbox.append(key)
                boxes.append(grp['Y'])
            ax.boxplot(boxes,vert=1,medianprops=medianprops)
            ax.set_xticklabels(nbox, rotation='vertical')
            if self.YcheckBox.isChecked():
                if self.YlineEdit.text():
                    ax.set_ylabel(self.YlineEdit.text())
            if self.XcheckBox.isChecked():
                if self.XlineEdit.text():
                    ax.set_xlabel(self.YlineEdit.text())
        if(self.ConditioningradioButton.isChecked()):           
            for key, grp in YGg:
                if self.CcheckBox.isChecked():
                    vcol=grp['Cr']
                else:
                    vcol=cm.magma.colors[int((len(cm.magma.colors)-1)/ngr*key)]               
                ax.scatter(range(1,len(grp['Y'])+1),grp['Y'],color=vcol,marker='o',label=key)
            ax.legend(loc='best')  
        elif(self.histogramradioButton.isChecked()):
            iqr=np.percentile(YG['Y'], [75, 25])
            iqr=iqr[0]-iqr[1]
            n=YG['Y'].shape[0]
            dy=abs(float(YG['Y'].max())-float(YG['Y'].min()))
            nbins=np.floor(dy/(2*iqr)*n**(1/3))+1
            nbins=2*nbins
            bins=np.linspace(float(YG['Y'].min()),float(YG['Y'].max()),nbins)
            for key, grp in YGg:
                if self.CcheckBox.isChecked():
                    vcol=grp['Cr']
                    vcol=np.unique(vcol)[0]
                else:
                    vcol=cm.magma.colors[int((len(cm.magma.colors)-1)/ngr*key)]                
                ax.hist(grp['Y'],bins=bins,histtype='bar',color=vcol,alpha=0.5,orientation='vertical',label=str(key))
            ax.legend(loc='best')  
        if self.TcheckBox.isChecked():
            if self.TlineEdit.text():
                ax.set_title(self.TlineEdit.text())
        else:
            ax.set_title('')
        if self.XcheckBox.isChecked():
            if self.XlineEdit.text():
                ax.set_xlabel(self.XlineEdit.text())
        else:
            ax.set_xlabel('')
        if self.YcheckBox.isChecked():
            ax.set_ylabel(self.YlineEdit.text())
        else:
            ax.set_ylabel('')
        if self.XGcheckBox.isChecked():
            ax.xaxis.grid(True)
        else:
            ax.xaxis.grid(False)
        if self.YGcheckBox.isChecked():
            ax.yaxis.grid(True)
        else:
            ax.yaxis.grid(False)
        if not self.XMcheckBox.isChecked():    
            ax.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
        if not self.YMcheckBox.isChecked():
            ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
        self.rmmpl()
        self.addmpl(fig)        
    def reset(self):
        self.YcomboBox.setCurrentIndex(0)
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

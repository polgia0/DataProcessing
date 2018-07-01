from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import PLS,DS
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_plsweightDialog,QDialog=loadUiType('plsweight.ui')
class plsweightDlg(QtWidgets.QDialog,Ui_plsweightDialog):
    def __init__(self,parent=None):
        super(plsweightDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        for x in range(PLS.ncp):
            self.componentcomboBox.addItem(str(x+1))
        Lr=DS.Lr[DS.Ir]
        Ts=DS.Ts[DS.Ir]
        for x in Lr[-Ts]:
            self.firstpointcomboBox.addItem(str(x))
            self.secondpointcomboBox.addItem(str(x))
        self.firstpointcomboBox.setCurrentIndex(0)
        self.secondpointcomboBox.setCurrentIndex(1)
        Gr=DS.Gr[DS.Ir]
        Gr=Gr[-Ts]
        Gr=pd.Series(Gr)
        for x in Gr.groupby(Gr).groups.keys():
            self.firstgroupcomboBox.addItem(str(x))
            self.secondgroupcomboBox.addItem(str(x))
        self.VcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
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
        nw=self.componentcomboBox.currentIndex()
        fig=Figure()
        ax=fig.add_subplot(111)
        Gc=DS.Gc[DS.Ic]
        Lc=DS.Lc[DS.Ic]
        Lcx=Lc[-Gc]
        Ccx=DS.Cc[DS.Ic]
        Ccx=Ccx[-Gc]
        ncx=len(Lcx)
        WS=np.dot(PLS.WS,np.linalg.inv(PLS.C))
        ind=np.array(range(1,ncx+1))
        if(ncx>30):
            itick=np.linspace(0,ncx-1,20).astype(int)
            ltick=Lcx[itick]
        else:
            itick=ind
            ltick=Lcx
        ax.set_xticks(itick)
        ax.set_xticklabels(ltick,rotation='vertical')
        ax.set_xlabel('Variable') 
        if self.CcheckBox.isChecked():
            cl=Ccx
        else:
            cl=ncx*['blue']
        ax.set_ylabel('Variable Contributon on Weight '+str(nw+1)) 
        ax.set_xlim([0,ncx+1])
        if self.pointradioButton.isChecked():
            p1=self.firstpointcomboBox.currentIndex()
            p2=self.secondpointcomboBox.currentIndex()
            x1=np.array(PLS.Xc[p1,:])
            x2=np.array(PLS.Xc[p2,:])
            lx=WS[:,nw]*(x1-x2)
            ax.bar(ind,lx,align='center',width=0.8,color=cl)
            ax.set_title('Contribution of object '+self.firstpointcomboBox.currentText()+
            ' vs. object '+self.secondpointcomboBox.currentText()+' to Weight '+str(nw+1))
        elif self.averageradioButton.isChecked():
            p1=self.firstpointcomboBox.currentIndex()
            x1=np.array(PLS.Xc[p1,:])
            lx=WS[:,nw]*x1
            ax.bar(ind,lx,align='center',width=0.8,color=cl)
            ax.set_title('Contribution of object '+self.firstpointcomboBox.currentText()
            +' to Weight '+str(nw+1))
        elif self.groupradioButton.isChecked():
            g1=self.firstgroupcomboBox.currentIndex()
            g2=self.secondgroupcomboBox.currentIndex()
            Gr=DS.Gr[DS.Ir]
            Gr=Gr[-DS.Ts[DS.Ir]]
            df=pd.DataFrame(PLS.Xc).groupby(Gr).mean()
            Xa=df.values
            x1=np.array(Xa[g1,:])
            x2=np.array(Xa[g2,:])
            lx=WS[:,nw]*(x1-x2)
            ax.bar(ind,lx,align='center',width=0.8,color=cl)
            ax.set_title('Contribution of Group '+self.firstgroupcomboBox.currentText()
            +' vs. Group '+self.secondgroupcomboBox.currentText()+' to Weight '+str(nw+1))
        if self.XcheckBox.isChecked():
            if self.XlineEdit.text():
                ax.set_xlabel(self.XlineEdit.text())
        else:
            ax.set_xlabel('')
        if self.YcheckBox.isChecked():
            if self.YlineEdit.text():
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
        self.firstpointcomboBox.setCurrentIndex(0)
        self.secondpointcomboBox.setCurrentIndex(1)
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
        self.XMcheckBox.setChecked(False)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.XlineEdit.setText('')
        self.YlineEdit.setText('')
        self.update()        
    def addmpl(self, fig):
        self.canvas=FigureCanvas(fig)
        self.mplvl.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar=NavigationToolbar(self.canvas, 
                self.mplwindow, coordinates=True)
        self.mplvl.addWidget(self.toolbar)
    def rmmpl(self,):
        self.mplvl.removeWidget(self.canvas)
        self.canvas.close()
        self.mplvl.removeWidget(self.toolbar)
        self.toolbar.close()

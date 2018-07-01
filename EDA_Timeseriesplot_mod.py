from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_timeseriesplotDialog,QDialog=loadUiType('timeseriesplot.ui')
class timeseriesplotDlg(QtWidgets.QDialog,Ui_timeseriesplotDialog):
    def __init__(self,parent=None):
        super(timeseriesplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.YcomboBox.addItems(DS.Lc)
        self.autocorrelationadioButton.setChecked(True)
        self.TcheckBox.setChecked(True)
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
        if self.YcomboBox.currentText()=='None':
            QtWidgets.QMessageBox.critical(self,'Error',"No Variable \n Selected !",QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data[[self.YcomboBox.currentText(),'Lr','Cr']]
        Nnan=data[self.YcomboBox.currentText()].isnull().all()
        data=data.dropna()
        #Lr=data['Lr'].values
        data=data.drop('Lr',axis=1)
        data=data.drop('Cr',axis=1)
        Y=data.values.ravel()
        if Y.dtype=='float' and Y.dtype=='int':
            QtWidgets.QMessageBox.critical(self,'Error',"Some values are not numbers!",\
                                           QtWidgets.QMessageBox.Ok)
            return()            
        color='blue'
        fig=Figure()
        ax=fig.add_subplot(111)
        if self.CcheckBox.isChecked():
             color=DS.Cc[self.YcomboBox.currentIndex()-1]
        if(self.autocorrelationadioButton.isChecked()):
            plot_acf(Y,ax=ax,color=color,alpha=int(self.alfaspinBox.value())/100)
            ax.set_title('Autocorrelation Plot of '+self.YcomboBox.currentText())
        elif(self.spectrumradioButton.isChecked()):
            ps=abs(np.fft.fft(Y))**2
            time_step=1/int(self.freqSpinBox.value())
            freqs=np.fft.fftfreq(Y.size, time_step)
            idx=np.argsort(freqs)
            freqs=freqs[idx]
            ps=ps[idx]
            red=freqs>0
            ax.plot(freqs[red], ps[red])
            ax.set_title('Spectral Plot of '+self.YcomboBox.currentText())
            ax.set_xlabel('Frequency')
            ax.set_ylabel('Spectrum')
        if Nnan:
            ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
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
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
        self.XMcheckBox.setChecked(False)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.XlineEdit.setText('')
        self.YlineEdit.setText('')
        self.TlineEdit.setText('')
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

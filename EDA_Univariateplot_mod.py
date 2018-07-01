from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import numpy.random as random
import scipy.stats as stats
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_univariateplotDialog,QDialog=loadUiType('univariateplot.ui')
class univariateplotDlg(QtWidgets.QDialog,Ui_univariateplotDialog):
    def __init__(self,parent=None):
        super(univariateplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.setCurrentIndex(0)
        self.histogramradioButton.setChecked(True)
        self.spinBox.setDisabled(True)
        self.TcheckBox.setChecked(True)
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.ApplyButton.clicked.connect(self.redraw)
        self.ResetButton.clicked.connect(self.reset)
        self.BootmeanradioButton.clicked.connect(self.deactivate)
        self.BootsdradioButton.clicked.connect(self.deactivate)
        self.BoxCoxradioButton.clicked.connect(self.deactivate1)
        self.histogramradioButton.clicked.connect(self.activate)
        self.NormalityradioButton.clicked.connect(self.activate)
        self.PPCCradioButton.clicked.connect(self.activate)
        self.BoxradioButton.clicked.connect(self.activate)
        fig=Figure()
        ax=fig.add_subplot(111)
        ax.plot(np.array(0))
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.addmpl(fig)
    def activate(self):
        self.spinBox.setDisabled(True)
        self.TcheckBox.setDisabled(False)      
        self.XcheckBox.setDisabled(False)      
        self.YcheckBox.setDisabled(False)     
        self.XMcheckBox.setDisabled(False)      
        self.YMcheckBox.setDisabled(False)     
        self.XGcheckBox.setDisabled(False)      
        self.YGcheckBox.setDisabled(False)     
    def deactivate(self):
        self.TcheckBox.setDisabled(True)      
        self.XcheckBox.setDisabled(True)      
        self.YcheckBox.setDisabled(True)     
        self.XMcheckBox.setDisabled(True)      
        self.YMcheckBox.setDisabled(True)     
        self.XGcheckBox.setDisabled(True)      
        self.YGcheckBox.setDisabled(True)
        self.spinBox.setDisabled(False)
    def deactivate1(self):
        self.TcheckBox.setDisabled(True)      
        self.XcheckBox.setDisabled(True)      
        self.YcheckBox.setDisabled(True)     
        self.XMcheckBox.setDisabled(True)      
        self.YMcheckBox.setDisabled(True)     
        self.XGcheckBox.setDisabled(True)      
        self.YGcheckBox.setDisabled(True)
    def redraw(self):
        def bootstrap(data,num_samples,statistic,alpha):
            n=len(data)
            idx=random.randint(0, n, (num_samples, n))
            samples=data[idx]
            stat=np.sort(statistic(samples, 1))
            return (stat[int((alpha/2.0)*num_samples)],stat[int((1-alpha/2.0)*num_samples)],samples)
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data[[self.YcomboBox.currentText(),'Lr','Cr']]
        if data.shape[1]!=3:
            QtWidgets.QMessageBox.critical(self,'Error',"More columns have the same name",\
                                           QtWidgets.QMessageBox.Ok)
            return()    
        Nnan=data[self.YcomboBox.currentText()].isnull().all()
        data=data.dropna()
        Lr=data['Lr'].values
        Cr=data['Cr'].values
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
        if self.BoxradioButton.isChecked():
            medianprops=dict(marker='D',markeredgecolor='black',markerfacecolor=color)
            ax.boxplot(Y,vert=1,medianprops=medianprops)
            if self.YcheckBox.isChecked():
                if self.YlineEdit.text():
                    ax.set_ylabel(self.YlineEdit.text())
            if self.XcheckBox.isChecked():
                if self.XlineEdit.text():
                    ax.set_xlabel(self.YlineEdit.text())
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.NormalityradioButton.isChecked():
            stats.probplot(Y,plot=ax)
            if self.XcheckBox.isChecked():
                if self.XlineEdit.text():
                    ax.set_xlabel('Normal N(0,1) Statistic Medians')
            if self.YcheckBox.isChecked():
                if self.YlineEdit.text():
                    ax.set_ylabel('Ordered Responce')
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.PPCCradioButton.isChecked():
            stats.ppcc_plot(Y,-6,6,plot=ax)
            if self.XcheckBox.isChecked():
                if self.XlineEdit.text():
                    ax.set_xlabel('Shape Values')
            if self.YcheckBox.isChecked():
                if self.YlineEdit.text():
                    ax.set_ylabel('Prob.Plot.Corr.Coef.')
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.BoxCoxradioButton.isChecked():
            fig=Figure()
            if (Y<=0).all():
                QtWidgets.QMessageBox.critical(self,'Error',"Data must be strictly positive!",QtWidgets.QMessageBox.Ok)
                return()    
            bins=np.linspace(np.amin(Y),np.amax(Y),21)
            ax1=fig.add_subplot(2,2,1,title="Original "+self.YcomboBox.currentText())
            ax1.hist(Y,bins=bins,histtype='bar',color=color, alpha=0.5, orientation="vertical",label="x")
            if Nnan:
                ax1.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
            trans_y,lambda_=stats.boxcox(Y)
            ax2=fig.add_subplot(2,2,2,title='Transformed Data (lambda='+str(round(lambda_,2))+')')
            bins=np.linspace(np.amin(trans_y),np.amax(trans_y),21)
            ax2.hist(trans_y, bins=bins,histtype='bar',color=color,alpha=0.5, orientation="vertical",label="x Transformed")
            ax3=fig.add_subplot(2,2,3,title="Original "+self.YcomboBox.currentText())
            stats.probplot(Y,dist='norm',plot=ax3)
            ax4=fig.add_subplot(2,2,4)
            stats.probplot(trans_y,dist='norm', plot=ax4)
            ax4.set_title('Transformed Data (lambda='+str(round(lambda_,2))+')')
        elif self.logisticradioButton.isChecked():
            stats.probplot(Y,dist=stats.logistic,plot=ax)
            ax.set_xlabel('Quantiles')
            ax.set_ylabel("Ordered "+self.YcomboBox.currentText())
            ax.set_title('Logistic', fontsize=12)
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.laplaceradioButton.isChecked():
            stats.probplot(Y,dist=stats.laplace,plot=ax)
            ax.set_xlabel('Quantiles')
            ax.set_ylabel('Ordered '+self.YcomboBox.currentText())
            ax.set_title('Laplace', fontsize=12)
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.logammaradioButton.isChecked():
            shape=float(self.logammadoubleSpinBox.value())
            stats.probplot(Y,dist=stats.loggamma,sparams=shape,plot=ax)
            ax.set_xlabel('Quantiles')
            ax.set_ylabel("Ordered "+self.YcomboBox.currentText())
            ax.set_title('Log Gamma with shape '+str(shape), fontsize=12)
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.lognormalradioButton.isChecked():
            shape=float(self.lognormdoubleSpinBox.value())/10.
            stats.probplot(Y,dist=stats.lognorm,sparams=(shape),plot=ax)
            ax.set_xlabel('Quantiles')
            ax.set_ylabel("Ordered "+self.YcomboBox.currentText())
            ax.set_title('Log norm with shape '+str(shape), fontsize=12)
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.BootmeanradioButton.isChecked():
            fig=Figure()
            ax1=fig.add_subplot(1,2,1,title="Historgram of "+self.YcomboBox.currentText())
            low,high,samples=bootstrap(Y,self.spinBox.value(),np.mean,0.05)
            points=np.mean(samples,1)
            ax1.hist(points, 50, histtype='step')
            if Nnan:
                ax1.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
            ax2=fig.add_subplot(1,2,2,title='Bootstrap 95% CI for mean')
            ax2.scatter(0.1*(random.random(len(points))-0.5), points)
            ax2.plot([0.19,0.21],[low,low],'r',linewidth=2)
            ax2.plot([0.19,0.21],[high,high],'r',linewidth=2)
            ax2.plot([0.2,0.2],[low,high],'r',linewidth=2)
            ax2.set_xlim([-0.2,0.3])
        elif self.BootsdradioButton.isChecked():
            fig=Figure()
            ax1=fig.add_subplot(1,2,1,title="Historgram of "+self.YcomboBox.currentText())
            low,high,samples=bootstrap(Y,self.spinBox.value(),np.std,0.05)
            points=np.std(samples,1)
            ax1.hist(points, 50, histtype='step')
            if Nnan:
                ax1.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
            ax2=fig.add_subplot(1,2,2,title='Bootstrap 95% CI for standard deviation')
            ax2.scatter(0.1*(random.random(len(points))-0.5),points)
            ax2.plot([0.19,0.21],[low,low],'r',linewidth=2)
            ax2.plot([0.19,0.21],[high,high],'r',linewidth=2)
            ax2.plot([0.2,0.2],[low,high],'r',linewidth=2)
            ax2.set_xlim([-0.2,0.3])
        elif self.histogramradioButton.isChecked():
            iqr=np.percentile(Y,[75,25])
            iqr=iqr[0]-iqr[1]
            n=Y.shape[0]
            dy=abs(float(Y.max())-float(Y.min()))
            nbins=np.floor(dy/(2*iqr)*n**(1/3))+1
            nbins=2*nbins
            bins=np.linspace(float(Y.min()),float(Y.max()),nbins)
            ax.hist(Y,bins=bins,histtype='bar',color=color,alpha=0.5,orientation='vertical',label="X")
            if Nnan:
                ax.annotate('NaN present',xy=(0.05,0.95),xycoords='axes fraction')
        elif self.trendradioButton.isChecked():
            nr=len(Y)
            ind=np.array(range(1,nr+1))
            color_point='red'
            color_line='blue'
            if self.CcheckBox.isChecked():
                color_line=DS.Cc[self.YcomboBox.currentIndex()-1]
                color_point=Cr
            ax.scatter(ind,Y,marker='o',color=color_point)
            if self.LcheckBox.isChecked():
                ax.plot(ind,Y,color=color_line)
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick, rotation='vertical')
            ax.set_xlabel('Object')
            ax.set_ylabel(self.YcomboBox.currentText())
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

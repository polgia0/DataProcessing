from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import sklearn as sk
import scipy.stats as stats
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_bivariateplot,QDialog=loadUiType('bivariateplot.ui')
class bivariateplotDlg(QtWidgets.QDialog,Ui_bivariateplot):
    def __init__(self,parent=None):
        super(bivariateplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
        self.PcheckBox.setChecked(True)
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
        if self.XcomboBox.currentText()==self.YcomboBox.currentText():
            QtWidgets.QMessageBox.critical(self,'Error',"Variables \n must be different !",QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data[[self.XcomboBox.currentText(),self.YcomboBox.currentText(),'Lr','Cr']]
        Nnan=data.isnull().isnull().all().all()
        data=data.dropna()
        Lr=data['Lr'].values
        Cr=data['Cr'].values
        data=data.drop('Lr',axis=1)
        data=data.drop('Cr',axis=1)
        if data.dtypes.all()=='float' and data.dtypes.all()=='int':
            QtWidgets.QMessageBox.critical(self,'Error',"Some values are not numbers!",QtWidgets.QMessageBox.Ok)
            return()            
        x=data[self.XcomboBox.currentText()].values
        y=data[self.YcomboBox.currentText()].values
        fig=Figure()
        ax=fig.add_subplot(111)
        color_line='blue'
        color_point='red'
        if self.CcheckBox.isChecked():
             color_line=DS.Cc[self.YcomboBox.currentIndex()-1]
             color_point=Cr
        if self.scatterradioButton.isChecked():
            if self.PcheckBox.isChecked():
                ax.scatter(x,y,marker='o',color=color_point)
            if self.LcheckBox.isChecked():
                ax.plot(x,y,color=color_line)
            if self.VcheckBox.isChecked():
                for i, txt in enumerate(Lr):
                    ax.annotate(txt, (x[i],y[i]))
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
        elif self.ellipseradioButton.isChecked():
            def plot_ellipse(x,y,nstd=2,ax=None,**kwargs):
                def eigsorted(cov):
                    vals, vecs = np.linalg.eigh(cov)
                    order = vals.argsort()[::-1]
                    return vals[order], vecs[:,order]    
                pos=(x.mean(),y.mean())
                cov=np.cov(x,y)
                vals, vecs = eigsorted(cov)
                theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))          
                width, height = 2 * nstd * np.sqrt(vals)
                ellip=Ellipse(xy=pos,width=width,height=height,angle=theta,fill=False,**kwargs) 
                ax.add_artist(ellip)
                return ellip
            for j in range(1,4):
                plot_ellipse(x,y,j,ax)
            ax.scatter(x,y,marker='o',color=color_point)
            if self.VcheckBox.isChecked():
                for i, txt in enumerate(Lr):
                    ax.annotate(txt, (x[i],y[i]))
            ax.set_xlim([x.mean()-4*x.std(),x.mean()+4*x.std()])
            ax.set_ylim([y.mean()-4*y.std(),y.mean()+4*y.std()])
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_title('Ellipse for 1,2,3 times the Standard Deviation')
        elif self.boxcoxradioButton.isChecked():
            if (x>0).all() and (y>0).all():
                CBC=np.zeros(50)
                vlambda=np.linspace(-2,2,50)
                for i in range(50):
                    trans_x=stats.boxcox(x,vlambda[i])
                    CBC[i]=np.corrcoef(trans_x,y)[0,1]
                if self.PcheckBox.isChecked():
                    ax.scatter(vlambda,CBC,marker='o',color=color_point)
                if self.LcheckBox.isChecked():
                    ax.plot(vlambda,CBC,color=color_line)
                ax.set_xlabel('Lambda')
                ax.set_ylabel('Correlation Coefficient')
            else:
                QtWidgets.QMessageBox.critical(self,'Error',"All values must be strictly positives",\
                                               QtWidgets.QMessageBox.Ok)
                return()            
        elif self.histogramradioButton.isChecked():
            cx='blue'
            cy='red'
            xm=x.mean()
            ym=y.mean()
            xstd=x.std()
            ystd=y.std()
            dy=(ym-3*ystd)-(xm+3*xstd)
            dx=(xm-3*xstd)-(ym+3*ystd)
            if(dy>0)|(dx>0):
                x=sk.preprocessing.normalize(x.reshape(1,-1),norm='l2',axis=1,copy=True,return_norm=False)
                y=sk.preprocessing.normalize(y.reshape(1,-1),norm='l2',axis=1,copy=True,return_norm=False)
                x=x.ravel()
                y=y.ravel()
                ax.set_xlabel('Normalized Quantities')
            if self.CcheckBox.isChecked():
                 cx=DS.Cc[self.XcomboBox.currentIndex()-1]
                 cy=DS.Cc[self.YcomboBox.currentIndex()-1]
            iqr=np.percentile(x,[75,25])
            iqr=iqr[0]-iqr[1]
            n=x.size
            dx=abs(max((x.max(),y.max()))-min((x.min(),y.min())))
            nbins=int(np.floor(dx/(2*iqr)*n**(1/3)))+1
            if nbins>self.spinBox.value():
                self.spinBox.setValue(nbins)
            else:
                nbins=self.spinBox.value()
            bins=np.linspace(min((x.min(),y.min())),max((x.max(),y.max())),nbins)
            ax.hist(x,bins=bins,histtype='bar',color=cx,alpha=0.5,
                    orientation='vertical',label=str(self.XcomboBox.currentText()))
            ax.hist(y,bins=bins,histtype='bar',color=cy,alpha=0.5,
                    orientation='vertical',label=str(self.YcomboBox.currentText()))
            box=ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
            ax.legend(bbox_to_anchor=(1,1),loc='upper left',borderaxespad=0.2)
        if Nnan:
            ax.annotate('{:04.2f} NaN'.format(Nnan),xy=(0.80,0.95),xycoords='figure fraction')
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
        if self.YGcheckBox.isChecked():
            ax.yaxis.grid(True)
        if self.TlineEdit.text():
            ax.set_title(self.TlineEdit.text())
        if not self.XMcheckBox.isChecked():    
            ax.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
        if not self.YMcheckBox.isChecked():
            ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
        self.rmmpl()
        self.addmpl(fig)        
    def reset(self):
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
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

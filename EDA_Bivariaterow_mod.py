from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import sklearn as sk
import pandas as pd
import scipy.stats as stats
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_bivariaterow,QDialog=loadUiType('bivariaterow.ui')
class bivariaterowDlg(QtWidgets.QDialog,Ui_bivariaterow):
    def __init__(self,parent=None):
        super(bivariaterowDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItem('Auto')
        self.YcomboBox.addItem('All')
        self.XcomboBox.addItems(DS.Lr[DS.Ir])
        self.YcomboBox.addItems(DS.Lr[DS.Ir])
        self.GcomboBox.addItem('All')
        groups=pd.Series(DS.Gr[DS.Ir])
        groups=groups.dropna()
        groups=groups.values
        groups=groups.astype('str')
        groups=np.unique(groups)
        groups=np.sort(groups)
        self.GcomboBox.addItems(groups)
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
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
            QtWidgets.QMessageBox.critical(self,'Error','Variables \n must be different !',QtWidgets.QMessageBox.Ok)
            return()
        if (self.XcomboBox.currentText()=='Auto') and (self.YcomboBox.currentText()=='All') and not self.scatterradioButton.isChecked():
            QtWidgets.QMessageBox.critical(self,'Error',"You have to select two rows \n for this kind of plot!",QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data.assign(Gr=DS.Gr[DS.Ir])
        if(self.XcomboBox.currentText()!='Auto') and (self.YcomboBox.currentText()!='All'):        
            data=data.loc[[self.XcomboBox.currentText(),self.YcomboBox.currentText()]]
        elif(self.XcomboBox.currentText()!='Auto') and (self.YcomboBox.currentText()=='All'):  
            QtWidgets.QMessageBox.critical(self,'Error',"Select two rows!",QtWidgets.QMessageBox.Ok)
            return()
        elif(self.XcomboBox.currentText()=='Auto') and (self.YcomboBox.currentText()!='All'):  
            QtWidgets.QMessageBox.critical(self,'Error',"Use Univariate plot!",QtWidgets.QMessageBox.Ok)
            return()
        Nnan=data.isnull().isnull().all().all()
        data=data.T.dropna()
        data=data.T
        Lr=data['Lr'].values
        Cr=data['Cr'].values
        Gr=data['Gr'].values
        data=data.drop('Lr',axis=1)
        data=data.drop('Cr',axis=1)
        data=data.drop('Gr',axis=1)
        if data.dtypes.all()=='float' and data.dtypes.all()=='int':
            QtWidgets.QMessageBox.critical(self,'Error',"Some values are not numbers!",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        if(self.XcomboBox.currentText()!='Auto') and (self.YcomboBox.currentText()!='All'):        
            if data.shape[0]!=2:
                QtWidgets.QMessageBox.critical(self,'Error',"Raw labels must be different",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            x=data.loc[self.XcomboBox.currentText()].values
            y=data.loc[self.YcomboBox.currentText()].values
        fig = Figure()
        ax = fig.add_subplot(111)
        color='blue'
        if self.scatterradioButton.isChecked():
            if(self.XcomboBox.currentText()!='Auto') and (self.YcomboBox.currentText()!='All'):        
                if self.PcheckBox.isChecked():
                    ax.scatter(x,y,marker='o',color=Cr)
                if self.LcheckBox.isChecked():
                    ax.plot(x,y,color='blue')
                if self.VcheckBox.isChecked():
                    for i, txt in enumerate(Lr):
                        ax.annotate(txt, (x[i],y[i]))
                ax.set_xlabel(self.XcomboBox.currentText())
                ax.set_ylabel(self.YcomboBox.currentText())
            else:
                nr,nc=data.shape
                Lc=DS.Lc[DS.Ic]
                x=range(1,nc+1)
                color=Cr
                if self.GcheckBox.isChecked():
                    groups=Gr
                    ngr=len(np.unique(groups))
                    color=[]
                    for key in groups:
                        color.append(cm.viridis.colors[int((len(cm.viridis.colors)-1)/ngr*key)])
                for i in range(nr):
                    y=data.iloc[i,:]
                    col=color[i]
                    if self.GcomboBox.currentText()=='All': 
                        if self.PcheckBox.isChecked():
                            ax.scatter(x,y,marker='o',color=col)
                        if self.LcheckBox.isChecked():
                            ax.plot(x,y,color=col)
                    else:
                        if int(self.GcomboBox.currentText())==groups[i]:
                            if self.PcheckBox.isChecked():
                                ax.scatter(x,y,marker='o',color=col)
                            if self.LcheckBox.isChecked():
                                ax.plot(x,y,color=col)
                if(nc>30):
                    itick=np.linspace(0,nc-1,20).astype(int)
                    ltick=Lc[itick]
                else:
                    itick=x
                    ltick=Lc
                ax.set_xlim([0,nc+2])
                ax.set_xticks(itick)
                ax.set_xticklabels(ltick, rotation='vertical')
        if self.ellipseradioButton.isChecked():
            def plot_ellipse(x,y,nstd=2,ax=None,**kwargs):
                def eigsorted(cov):
                    vals, vecs = np.linalg.eigh(cov)
                    order = vals.argsort()[::-1]
                    return vals[order], vecs[:,order]    
                pos=(x.mean(),y.mean())
                cov=np.cov(x,y).tolist()
                vals, vecs = eigsorted(cov)
                theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))          
                width, height = 2 * nstd * np.sqrt(vals)
                ellip=Ellipse(xy=pos,width=width,height=height,angle=theta,fill=False,**kwargs) 
                ax.add_artist(ellip)
                return ellip
            for j in range(1,4):
                plot_ellipse(x,y,j,ax)
            ax.scatter(x,y)
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_title('Ellipse for 1,2,3 times the Standard Deviation')
        if self.boxcoxradioButton.isChecked():
            if (not (x>0).all()) and (not (y>0).all()) :
                QtWidgets.QMessageBox.critical(self,'Error',"Values must be strictly positive",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            CBC=np.zeros(50)
            vlambda=np.linspace(-2,2,50)
            for i in range(50):
                trans_x=stats.boxcox(x,vlambda[i])
                CBC[i]=np.corrcoef(trans_x,y)[0,1]
            if self.PcheckBox.isChecked():
                ax.scatter(vlambda,CBC,marker='o',color=color)
            if self.LcheckBox.isChecked():
                ax.plot(vlambda,CBC,color=color)
            ax.set_xlabel('Lambda')
            ax.set_ylabel('Correlation Coefficient')
        if self.histogramradioButton.isChecked():
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

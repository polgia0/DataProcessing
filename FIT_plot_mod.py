from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS,FIT
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.patches import Ellipse
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_fitplot,QDialog=loadUiType('fitplot.ui')
class fitplotDlg(QtWidgets.QDialog,Ui_fitplot):
    def __init__(self,parent=None):
        super(fitplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        list_p=['p0','p1','p2','p3']
        self.XcomboBox.addItems(list_p)
        self.YcomboBox.addItems(list_p)
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
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
        if self.YcomboBox.currentText() == self.XcomboBox.currentText():
            QtWidgets.QMessageBox.critical(self,'Error',"You have to choose different parameters!",QtWidgets.QMessageBox.Ok)
            return()
        res=FIT.getres()
        Mod=FIT.getmodel()
        p=FIT.getp()
        jac=FIT.getjac()
        fig = Figure()
        ax = fig.add_subplot(111)
        vcol=['red']*len(res)
        ind=range(1,len(res)+1)
        ix=self.XcomboBox.currentIndex()
        iy=self.YcomboBox.currentIndex()
        if self.ellradioButton.isChecked():
            def eigsorted(cov):
                vals, vecs = np.linalg.eigh(cov)
                order = vals.argsort()[::-1]
                return vals[order], vecs[:,order]    
            pos=(p[ix],p[iy])
            s2=res.var()
            cov=np.linalg.inv(np.dot(jac.T,jac))*s2
            cov=cov[np.ix_([ix,iy],[ix,iy])]
            vals, vecs = eigsorted(cov)
            theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))          
            width, height = 2 * np.sqrt(vals)
            ellip=Ellipse(xy=pos,width=width,height=height,angle=theta,fill=False) 
            ax.add_artist(ellip)
            ax.set_xlim([p[ix]-4*np.sqrt(cov[0,0]),p[ix]+4*np.sqrt(cov[0,0])])
            ax.set_ylim([p[iy]-4*np.sqrt(cov[1,1]),p[iy]+4*np.sqrt(cov[1,1])])
            ax.scatter(p[ix],p[iy],color='red',marker='o')
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
        elif self.resradioButton.isChecked():
            if self.CcheckBox.isChecked():
                 vcol=DS.getCr()
            ax.hist(res,bins=10,orientation=u'horizontal',fc=(0, 0, 1, 0.5))
            ax.scatter(ind,res,color=vcol,marker='o')
            ax.set_ylabel('Residuals')
            ax.set_xlabel('Object Index')
            if self.VcheckBox.isChecked():
                for txt in enumerate(DS.getLr()):
                    ax.annotate(txt,(ind,res))
        elif self.surradioButton.isChecked():
            def fun(p1,p2):
                pi=p
                pi[ix]=p1
                pi[iy]=p2
                return sum((model(pi,x)-y)**2)/2
            def model(p,x):
                if Mod==0:
                    return p[0]*x**3+p[1]*x**2+p[2]*x+p[3]
                elif Mod==1:
                    return p[0]*x**2+p[1]*x+p[2]
                elif Mod==2:
                    return p[0]*x+p[1]
                elif Mod==3:
                    return p[0]*np.exp(p[1]*x)
                elif Mod==4:
                    return p[0]*np.exp(p[1]/(p[2]+x))   
                elif Mod==5:
                    return p[0]*np.exp(-p[1]/x)   
                elif Mod==6:
                    return p[0]*np.log(p[1]*x)     
                elif Mod==7:
                    return p[0]*x**(p[1])   
                elif Mod==8:
                    return p[0]/(1+p[1]*x)       
                elif Mod==9:
                    return p[0]/(1+p[1]*x**2)       
                elif Mod==10:
                    return p[0]/(1+np.exp(-p[1]*x))        
                elif Mod==11:
                    return p[0]*(x**2+p[1]*x)/(x**2+p[2]*x+p[3])
            fig=plt.figure()
            ax = fig.add_subplot(111)
            npts=60
            s2=res.var()
            x=FIT.getx()
            y=FIT.gety()
            cov=np.linalg.inv(np.dot(jac.T,jac))*s2
            cov=cov[np.ix_([ix,iy],[ix,iy])]
            pcx=p[ix]
            pcy=p[iy]
            pxi=np.linspace(pcx-4*np.sqrt(cov[0,0]),pcx+4*np.sqrt(cov[0,0]),npts)
            pyi=np.linspace(pcy-4*np.sqrt(cov[1,1]),pcy+4*np.sqrt(cov[1,1]),npts)
            px=[pcx]
            py=[pcy]
            pz=[fun(pcx,pcy)]
            for i in range(npts):
                for j in range(npts):
                    px.append(pxi[i])
                    py.append(pyi[j])
                    pz.append(fun(pxi[i],pyi[j])) 
            px=np.array(px)
            py=np.array(py)
            pz=np.array(pz)
            pzi=plt.mlab.griddata(px,py,pz,pxi,pyi,interp='linear')
            plt.contour(pxi,pyi,pzi,15,linewidths=0.5, colors='k')
            plt.contourf(pxi,pyi,pzi,15,cmap=plt.cm.rainbow)
            plt.colorbar()
            ax.scatter(pcx,pcy,color='red',marker='o')
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_xlim([px.min(),px.max()])
            ax.set_ylim([py.min(),py.max()])
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

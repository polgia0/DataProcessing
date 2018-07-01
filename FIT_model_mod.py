from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS,FIT
import numpy as np
from matplotlib.figure import Figure
from scipy.optimize import least_squares
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
from sklearn import preprocessing
Ui_fitmodel,QDialog=loadUiType('fitmodel.ui')
class fitmodelDlg(QtWidgets.QDialog,Ui_fitmodel):
    def __init__(self,parent=None):
        super(fitmodelDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItem('None')
        self.YcomboBox.addItem('None')
        listmodel=['cubic: p[0]x^3+p[1]x^2+p[2]x+p[3]',
                'parabolic: p[0]x^2+p[1]x+p[2]',
                'linear: p[0]x+p[1]',
                'exponential: p[0]e^(p[1]x)',
                'antoine: p[0]e^(p[1]/(p[2]+x))',
                'arrhenius: p[0]e^(-p[1]/x)',
                'logarithm: p[0] ln (p[1]*x)',
                'power: p[0] x^p[1]',
                'iperbolic: p[0]/(1+p[1]x)',
                'rational: p[0]/(1+p[1] x^2)',
                'logistic: p[0]/(1+e^(-p[1] x))',
                'enzimatic: p[0] (x^2+p[1]*x)/(x^2+p[2] x+p[3])']
        self.McomboBox.addItems(listmodel)
        self.XcomboBox.addItems(DS.getLc())
        self.YcomboBox.addItems(DS.getLc())
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
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
        if self.YcomboBox.currentText() == 'None' or self.XcomboBox.currentText() == 'None':
            QtWidgets.QMessageBox.critical(self,'Error',"You have to choose both variables!",QtWidgets.QMessageBox.Ok)
            return()
        data=DS.getData()
        x=data[self.XcomboBox.currentText()]
        y=data[self.YcomboBox.currentText()]
        if self.normalizecheckBox.isChecked():
            xscaler=preprocessing.MinMaxScaler().fit(x.reshape(-1,1))
            x=xscaler.transform(x.reshape(-1,1))
            yscaler=preprocessing.MinMaxScaler().fit(y.reshape(-1,1))
            y=yscaler.transform(y.reshape(-1,1))
            x=np.squeeze(x.T)
            y=np.squeeze(y.T)
        x=x.values.astype('float').ravel()
        y=y.values.astype('float').ravel()  
        if self.radioButton_a0.isChecked():mth='trf'
        elif self.radioButton_a1.isChecked():mth='dogbox'
        elif self.radioButton_a2.isChecked():mth='lm'
        p0=np.array([float(self.lineEdit_0.text()),
                     float(self.lineEdit_1.text()),
                     float(self.lineEdit_2.text()),
                     float(self.lineEdit_3.text())])
        bounds=np.array([-np.inf,np.inf])
        if self.lineEdit_low.text()!='':bounds[0]=float(self.lineEdit_low.text())
        if self.lineEdit_up.text()!='':bounds[1]=float(self.lineEdit_up.text())
        if self.McomboBox.currentIndex()==0:p0=p0[:4]
        elif self.McomboBox.currentIndex()==1:p0=p0[:3]
        elif self.McomboBox.currentIndex()==2:p0=p0[:2]
        elif self.McomboBox.currentIndex()==3:p0=p0[:2]
        elif self.McomboBox.currentIndex()==4:p0=p0[:3]
        elif self.McomboBox.currentIndex()==5:p0=p0[:2]
        elif self.McomboBox.currentIndex()==6:p0=p0[:2]
        elif self.McomboBox.currentIndex()==7:p0=p0[:2]
        elif self.McomboBox.currentIndex()==8:p0=p0[:2]
        elif self.McomboBox.currentIndex()==9:p0=p0[:2]
        elif self.McomboBox.currentIndex()==10:p0=p0[:2]
        elif self.McomboBox.currentIndex()==11:p0=p0[:4]
        bounds=(bounds[0],bounds[1])
        def fun(p,x,y):
            return model(p,x)-y
        def model(p,x):
            if self.McomboBox.currentIndex()==0:
                return p[0]*x**3+p[1]*x**2+p[2]*x+p[3]
            elif self.McomboBox.currentIndex()==1:
                return p[0]*x**2+p[1]*x+p[2]
            elif self.McomboBox.currentIndex()==2:
                return p[0]*x+p[1]
            elif self.McomboBox.currentIndex()==3:
                return p[0]*np.exp(p[1]*x)
            elif self.McomboBox.currentIndex()==4:
                return p[0]*np.exp(p[1]/(p[2]+x))   
            elif self.McomboBox.currentIndex()==5:
                return p[0]*np.exp(-p[1]/x)   
            elif self.McomboBox.currentIndex()==6:
                return p[0]*np.log(p[1]*x)     
            elif self.McomboBox.currentIndex()==7:
                return p[0]*x**(p[1])   
            elif self.McomboBox.currentIndex()==8:
                return p[0]/(1+p[1]*x)       
            elif self.McomboBox.currentIndex()==9:
                return p[0]/(1+p[1]*x**2)       
            elif self.McomboBox.currentIndex()==10:
                return p[0]/(1+np.exp(-p[1]*x))        
            elif self.McomboBox.currentIndex()==11:
                return p[0]*(x**2+p[1]*x)/(x**2+p[2]*x+p[3])
        def jac(p,x,y):
            J=np.empty((x.size,p.size))
            if self.McomboBox.currentIndex()==0:
                J[:,0]=x**3
                J[:,1]=x**2
                J[:,2]=x                
                J[:,3]=1                
            elif self.McomboBox.currentIndex()==1:
                J[:,0]=x**2
                J[:,1]=x
                J[:,2]=1                
            elif self.McomboBox.currentIndex()==2:
                J[:,0]=x
                J[:,1]=1
            elif self.McomboBox.currentIndex()==3:
                J[:,0]=np.exp(p[1]*x)
                J[:,1]=p[0]*x*np.exp(p[1]*x)
            elif self.McomboBox.currentIndex()==4:
                J[:,0]=np.exp(p[1]/(p[2]+x)) 
                J[:,1]=p[0]*np.exp(p[1]/(p[2]+x))/(p[2]+x)
                J[:,2]=-p[0]*np.exp(p[1]/(p[2]+x))*p[1]/(p[2]+x)**2             
            elif self.McomboBox.currentIndex()==5:
                J[:,0]=np.exp(-p[1]/x) 
                J[:,1]=-p[0]*np.exp(-p[1]/x)/x
            elif self.McomboBox.currentIndex()==6:
                J[:,0]=np.log(p[1]*x) 
                J[:,1]=p[0]*x/p[1] 
            elif self.McomboBox.currentIndex()==7:
                J[:,0]=x**(p[1])  
                J[:,1]=p[0]*x**(p[1])*np.log(x)  
            elif self.McomboBox.currentIndex()==8:
                J[:,0]=1/(1+p[1]*x)   
                J[:,1]=p[0]*x/(1+p[1]*x)**2 
            elif self.McomboBox.currentIndex()==9:
                J[:,0]=1/(1+p[1]*x**2)   
                J[:,1]=p[0]*x**2/(1+p[1]*x)**2 
            elif self.McomboBox.currentIndex()==10:
                J[:,0]=1/(1+np.exp(-p[1]*x)) 
                J[:,1]=p[0]*x*np.exp(-p[1]*x)/(1+np.exp(-p[1]*x))**2 
            elif self.McomboBox.currentIndex()==11:
                den=x**2+p[2]*x+p[3]
                num=x**2+p[1]*x
                J[:,0]=num/den
                J[:,1]=p[0]*num*x/den
                J[:,2]=-p[0]*num*x/den**2
                J[:,3]=-p[0]*num/den**2
            return J
        try:
            res=least_squares(fun,
                              p0,
                              jac=jac,
                              bounds=bounds,
                              args=(x,y),
                              verbose=0,
                              method=mth,
                              xtol=float(self.lineEdit_xtol.text()),
                              ftol=float(self.lineEdit_ytol.text()))
        except:
            QtWidgets.QMessageBox.critical(self,'Error',"Solver crashed! \n something wrong in parameters or bounds set.",QtWidgets.QMessageBox.Ok)
            return()
        FIT.setx(x)
        FIT.sety(y)
        FIT.setp(res.x)
        FIT.setjac(res.jac)
        FIT.setres(res.fun)
        FIT.setfit(True)
        FIT.setmodel(self.McomboBox.currentIndex())        
        x_test=np.linspace(x.min(),x.max(),50)
        y_test=model(res.x,x_test)
        fig = Figure()
        ax = fig.add_subplot(111)
        vcol=['red']*len(y)
        if self.CcheckBox.isChecked():
             vcol=DS.getCr()
        ax.scatter(x,y,color=vcol,marker='o',label='data')
        ax.plot(x_test,y_test,label='fitted model')
        ax.set_ylabel(self.YcomboBox.currentText())
        ax.set_xlabel(self.XcomboBox.currentText())
        ax.legend(loc='lower right')
        ax.annotate(res.message, xy=(1, 1), xycoords='axes fraction', fontsize=6,
                xytext=(0, +15), textcoords='offset points',ha='right', va='top')
        if self.VcheckBox.isChecked():
            for txt in enumerate(DS.getLr()):
                ax.annotate(txt,(x,y))
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

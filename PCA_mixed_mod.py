from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import PCA,DS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_pcamixedplotDialog,QDialog=loadUiType('pcamixed.ui')
class pcamixedplotDlg(QtWidgets.QDialog,Ui_pcamixedplotDialog):
    def __init__(self,parent=None):
        super(pcamixedplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.lo2comboBox.addItem('None')
        self.lo3comboBox.addItem('None')
        self.YcomboBox.addItem('None')
        for x in range(PCA.ncp):
            self.lo1comboBox.addItem(str(x+1))
            self.lo2comboBox.addItem(str(x+1))
            self.lo3comboBox.addItem(str(x+1))
            self.XcomboBox.addItem(str(x+1))
            self.YcomboBox.addItem(str(x+1))
        self.YcomboBox.setCurrentIndex(2)
        self.variablecomboBox.addItems(DS.Raw.columns)
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
        Lc=DS.Lc[DS.Ic]
        nc=len(Lc)
        Lr=DS.Lr[DS.Ir]
        Ts=DS.Ts[DS.Ir]
        Lr=Lr[-Ts]
        nr=len(Lr)
        Cr=DS.Cr[DS.Ir]
        Cr=Cr[-Ts]
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        data=data[-Ts]
        if self.loadingradioButton.isChecked():
            l1=self.lo1comboBox.currentIndex()
            l2=self.lo2comboBox.currentIndex()-1
            l3=self.lo3comboBox.currentIndex()-1
            ind=np.array(range(1,nc+1))
            bar_width=0.25      
            opacity=0.4
            fig=Figure()
            ax=fig.add_subplot(111)
            if(nc>30):
                itick=np.linspace(0,nc-1,20).astype(int)
                ltick=Lc[itick]
            else:
                itick=ind
                ltick=Lc
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick, rotation='vertical')
            ax.bar(ind,PCA.lo[:,l1],bar_width,alpha=opacity,color='blue',label=self.lo1comboBox.currentText())
            ax.set_xlim([min(itick)-bar_width,max(itick)+2*bar_width])
            if(l2>0):
                ax.bar(ind+bar_width,PCA.lo[:,l2],bar_width,alpha=opacity,color='red',\
                       label=self.lo2comboBox.currentText())
                ax.set_xlim([min(itick)-bar_width,max(itick)+3*bar_width])
            if(l3>0):
                ax.bar(ind+2*bar_width,PCA.lo[:,l3],bar_width,alpha=opacity,color='green',\
                       label=self.lo3comboBox.currentText())
                ax.set_xlim([min(itick)-bar_width,max(itick)+4*bar_width])
            ax.set_xlabel('Variables') 
            ax.set_ylabel('Loadings')
            ax.set_title('Loading vs.Variables')
            ax.legend()
        elif self.scoreradioButton.isChecked():
            if self.variablecomboBox.currentText()=='None':
                QtWidgets.QMessageBox.critical(self,'Error',"Set the Variable!",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            s1=self.XcomboBox.currentIndex()
            s2=self.YcomboBox.currentIndex()-1
            vr=DS.Raw[self.variablecomboBox.currentText()]
            vr=vr[DS.Ir]
            if len(vr)!=nr:
                QtWidgets.QMessageBox.critical(self,'Error',"The variable is not defined \n in all points!",\
                                               QtWidgets.QMessageBox.Ok)
                return()                
            rv=PCA.rv*100        
            if(s2>0):
                data=pd.DataFrame([PCA.sco[:,s1],PCA.sco[:,s2],vr,Cr],index=['s1','s2','variable','color']).T
                fig=plt.figure()
                ax=fig.add_subplot(111)
                npts=self.nptsspinBox.value()
                x=data['s1']
                y=data['s2']
                z=data['variable'] 
                xi=np.linspace(x.min(),x.max(),npts)
                yi=np.linspace(y.min(),y.max(),npts)
                zi=plt.mlab.griddata(x,y,z,xi,yi,interp='linear')
                plt.contour(xi,yi,zi,15,linewidths=0.5,colors='k')
                plt.contourf(xi,yi,zi,15,cmap=plt.cm.rainbow)
                plt.colorbar()
                plt.scatter(x,y,marker='o',c='b',s=5,zorder=10)
                plt.scatter(0,0,color='red',s=60,marker='+')
                if self.VcheckBox.isChecked():
                    for i, txt in enumerate(vr):
                        plt.text(data.iloc[i,0],data.iloc[i,1],txt)
                plt.title('Score Plot ('+str(round(rv[s1]+rv[s2],2))+'%), Variable: '+self.variablecomboBox.currentText())
                plt.ylabel('Comp.'+str(s2+1)+' ('+str(round(rv[s2],2))+'%)')
                plt.xlabel('Comp.'+str(s1+1)+' ('+str(round(rv[s1],2))+'%)')
            else:
                data=pd.DataFrame([PCA.sco[:,s1],vr,Cr],index=['s1','variable','color']).T
                fig=Figure()
                ax=fig.add_subplot(111)
                ax.scatter(data['s1'],data['variable'],alpha=0.3,color=data['color'],s=30,marker='o')
                ax.set_title('Variable: '+self.variablecomboBox.currentText()+' vs. Score '+str(s1+1)+' ('+str(round(rv[s1],2))+'%)')
                ax.set_ylabel('Variable: '+self.variablecomboBox.currentText())
                ax.set_xlabel('Comp.'+str(s1+1)+' ('+str(round(rv[s1],2))+'%)')
        elif self.pcrradioButton.isChecked():
            if self.variablecomboBox.currentText()=='None':
                QtWidgets.QMessageBox.critical(self,'Error',"Set the Variable!",QtWidgets.QMessageBox.Ok)
                return()
            if self.XcomboBox.currentText()=='None' and not self.pcrcheckBox.isChecked():
                QtWidgets.QMessageBox.critical(self,'Error',"Set at least the X component!",QtWidgets.QMessageBox.Ok)
                return()
            vr=data[self.variablecomboBox.currentText()]
            rv=PCA.rv*100        
            fig=plt.figure()
            pcr=self.pcrcheckBox.isChecked()
            if(not(pcr)):
                s1=self.XcomboBox.currentIndex()
                s2=self.YcomboBox.currentIndex()-1
                if(s2>0):
                    data=np.stack((PCA.sco[:,s1],PCA.sco[:,s2],np.ones(nr),vr),axis=1)
                    X=data[:,0:3]
                    Y=data[:,3]
                    OLS=np.linalg.lstsq(X,Y)
                    Yh=np.dot(X,OLS[0])
                    X1=X[:,0]
                    X2=X[:,1]
                    x1,x2=np.meshgrid(np.linspace(X1.min(),X1.max(),20),np.linspace(X2.min(),X2.max(),20),sparse=True)
                    x12=np.concatenate((x1.T,x2,np.ones(20)[np.newaxis].T),axis=1)
                    z=np.dot(x12,OLS[0])
                    ax=fig.gca(projection='3d')
                    ax.scatter(X1,X2,Y,c=Cr,marker='o')
                    ax.set_xlabel('PC'+str(s1+1))
                    ax.set_ylabel('PC'+str(s2+1))
                    ax.set_zlabel(self.variablecomboBox.currentText())
                    ax.plot_surface(x1,x2,z,alpha=0.5,rstride=1,cstride=1,linewidth=0,antialiased=False)
                else:
                    data=np.stack((PCA.sco[:,s1],np.ones(nr),vr),axis=1)
                    X=data[:,0:2]
                    Y=data[:,2]
                    Y=Y[:,np.newaxis]
                    OLS=np.linalg.lstsq(X,Y)
                    Yh=np.dot(X,OLS[0])
                    X=X[:,0]
                    ax=fig.add_subplot(111)
                    ax.scatter(X,Y,color=Cr,marker='o')
                    ax.plot(X,Yh,'r-')
                    ax.set_title(self.variablecomboBox.currentText() +' vs. PC'+str(s1+1))
                    ax.set_xlabel('PC'+str(s1+1))
                    ax.set_ylabel(self.variablecomboBox.currentText())
            else: # case of whole PCR
                data=np.stack((np.ones(nr),vr),axis=1)
                data=np.concatenate((PCA.sco,data),axis=1)
                X=data[:,0:PCA.ncp+1]
                Y=data[:,PCA.ncp+1]
                OLS=np.linalg.lstsq(X,Y)
                Yh=np.dot(X,OLS[0])
                ax=fig.add_subplot(111)
                ax.scatter(Y,Yh,color=Cr,alpha=0.3,marker='o')
                Dmin=min([min(Y),min(Yh)])
                Dmax=max([max(Y),max(Yh)])
                ax.set_xlim([Dmin,Dmax])
                ax.set_ylim([Dmin,Dmax])
                ax.set_xlabel(self.variablecomboBox.currentText()+' measured')
                ax.set_ylabel(self.variablecomboBox.currentText()+' fitted')
                ax.set_title('Fitted vs. Measured Plot for '+self.variablecomboBox.currentText()+' : Model '+str(PCA.ncp)+' components')
                ax.add_line(Line2D([Dmin,Dmax],[Dmin,Dmax],color='red'))
                if self.VcheckBox.isChecked():
                    for i in range(nr):
                        ax.annotate(Lr[i],(Y[i],Yh[i]))
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
        self.variablecomboBox.setCurrentIndex(0)
        self.lo1comboBox.setCurrentIndex(0)
        self.lo2comboBox.setCurrentIndex(0)
        self.lo3comboBox.setCurrentIndex(0)
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
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

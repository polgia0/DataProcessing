from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DOE,DS
import numpy as np
import scipy as sp
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D
from matplotlib.gridspec import GridSpec
from matplotlib.figure import Figure
from DOE_model_mod import doemodel
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_doeplotDialog,QDialog=loadUiType('doeplot.ui')
class doeplotDlg(QtWidgets.QDialog,Ui_doeplotDialog):
    def __init__(self,parent=None):
        super(doeplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Lcx=Lc[-Gc]
        Lcy=Lc[Gc]
        for x in Lcy:
            self.responcecomboBox.addItem(str(x))
        for x in Lcx:
            self.factorcomboBox.addItem(str(x))
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
        if DOE.lfac is None: 
            doemodel(self)
        fig=Figure()
        ny=self.responcecomboBox.currentIndex()
        nf=self.factorcomboBox.currentIndex()
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Lcy=Lc[Gc]
        Lcx=Lc[-Gc]
        nX=len(Lcx)
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        Y=data[Lcy]
        X=data[Lcx]
        nr=X.shape[0]
        w_text=''
        if nr>2**nX:
            Xu=X[-X.duplicated().values]
            Yu=[]
            for i in range(Xu.shape[0]):
                Yu.append(Y[(X==Xu.ix[i,:]).product(axis=1).astype('bool').values].mean().values)
            nr=2**nX
            X=Xu
            Y=pd.DataFrame(Yu,index=X.index,columns=Y.columns)
            w_text='Duplicated tests are averaged'
        ncx=len(Lcx)
        Y=Y.values.astype('float')
        X=X.values.astype('float')
        if self.orderedradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            order=Y.argsort()
            ind=np.arange(nr)
            X=X[order,:]
            if((X.max()==1)&(X.min()==-1)):
                X=X.astype('str')
                X[X=='-1.0']='-'
                X[X=='1.0']='+'
                X[X=='0.0']='O'
            else:
                X=X.astype('str')            
            label=nr*['']
            for i in range(nr):
                label[i]=' '.join(X[i,:].tolist())
            ax.scatter(ind,Y[order],color='red',alpha=0.3,marker='o')
            ax.set_xticks(ind)
            ax.set_xticklabels(ind[order]+1, rotation='vertical')
            ax.set_xlabel('Experiment Sequence')
            ax.set_ylabel('Responce')
            ax.xaxis.grid()
            ax.yaxis.grid()
            ax.set_title('Ordered Plot for '+self.responcecomboBox.currentText())
            for i in range(nr):
                ax.annotate(label[i],(ind[i],Y[order][i]),rotation=-90,size=14)
        elif self.meanradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            vmain=np.zeros(2*ncx)
            Ym=np.mean(Y)
            labels=[]
            for i in range(ncx):
                labels=labels+['-']+[Lcx[i]]+['+']+[' ']
                vmain[2*i]=np.mean(Y[X[:,i]==-1])
                vmain[2*i+1]=np.mean(Y[X[:,i]==1])
            ind=np.arange(2*ncx)
            ax.scatter(ind,vmain,color='red',alpha=0.3,marker='o')
            ax.set_xlabel('Factors')
            ax.set_ylabel('Responce')
            ax.set_xticks(np.arange(0,2*ncx,0.5))
            ax.set_xticklabels(labels,rotation='vertical')
            ax.set_title('Main Effects Plot for Responce: '+self.responcecomboBox.currentText())
            ax.add_line(Line2D([-1,2*ncx],[Ym,Ym],color='green'))
            for i in range(ncx):
                ax.add_line(Line2D([ind[2*i],ind[2*i+1]],[vmain[2*i],vmain[2*i+1]],color='red')) 
        elif self.mainradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            Ym=np.mean(Y)
            labels=[]
            ind=[]
            vy=[]
            for i in range(ncx):
                labels=labels+['-']+[Lcx[i]]+['+']+[' ']
                vy=vy+[Y[X[:,i]==-1].T.tolist()]+[Y[X[:,i]==1].T.tolist()]
                ind=ind+len(Y[X[:,i]==-1])*[2*i]+len(Y[X[:,i]==1])*[2*i+1]
            ax.scatter(ind,vy,color='red',alpha=0.3,marker='o')
            ax.set_xlabel('Factors')
            ax.set_ylabel('Responce')
            ax.set_xticks(np.arange(0,2*ncx,0.5))
            ax.set_xticklabels(labels, rotation='vertical')
            ax.set_title('Scatter Plot for Responce :'+self.responcecomboBox.currentText())
            ax.add_line(Line2D([-1,2*ncx],[Ym,Ym],color='green'))
            for i in range(2*ncx):
                ax.add_line(Line2D([i,i],[min(vy[i]),max(vy[i])],color='red')) 
        elif self.interactionradioButton.isChecked():
            def int_plot(ax,X,Y,Ym,i,j):
                x=X[:,i]
                if(i!=j):
                    x=x*X[:,j]
                y_m=np.mean(Y[x==-1])
                y_p=np.mean(Y[x==+1])
                ax.set_ylim([min(Y),max(Y)])
                ax.scatter([0,1],[y_m,y_p],color='red',alpha=0.3,marker='o')
                ax.add_line(Line2D([-1,2],[Ym,Ym],color='green'))
                ax.add_line(Line2D([0,1],[y_m,y_p],color='red'))
            Y=Y[:,ny]
            Ym=np.mean(Y)
            gs=GridSpec(ncx,ncx)
            for i in range(ncx):
                for j in range(ncx):
                    if(j>=i):
                        ax=fig.add_subplot(gs[i,j])
                        int_plot(ax,X,Y,Ym,i,j)
                        if(i==j):
                            ax.set_ylabel('Responce')
                            ax.set_xticks([0,1], minor=False)
                            ax.set_xticklabels(['-','+'],minor=False)
                            ax.set_xlabel(Lcx[i])
                        else:
                            ax.xaxis.set_visible(False)
        elif self.blockradioButton.isChecked():
            ax=fig.add_subplot(111)
            for i in range(nr):
                for j in range(ncx):
                   if((X[i,j]!=1)&(X[i,j]!=-1)):
                        QtWidgets.QMessageBox.critical(self,'Output Limit',
                        'There are more then 2 levels\n I am not able to plot',QtWidgets.QMessageBox.Ok)
                        return()
            labels=np.array(range(1,ncx+1))
            labels=np.delete(labels,nf)
            x=X[:,nf]
            X=np.delete(X,nf,1)
            Y=Y[:,ny]
            if(min(Y)>0):
                ymin=0.99*min(Y)
            else:
                ymin=1.01*min(Y)
            if(max(Y)>0):
                ymax=1.01*max(Y)
            else:
                ymax=0.99*max(Y)
            n_factor=math.factorial(ncx)/math.factorial(ncx-2)/2
            if(n_factor>10):
                QtWidgets.QMessageBox.critical(self,'Output Limit',
                'There are more then 10 interactions. \n Too many to be plotted!',QtWidgets.QMessageBox.Ok)
                return()
            if(n_factor==1):
                QtWidgets.QMessageBox.critical(self,'Output Limit',
                'There are no interaction left. \n Block Plot does not apply',QtWidgets.QMessageBox.Ok)
                return()
            for i in range(ncx-1):
                for j in range(i,(ncx-1)):
                    if(j>i):
                        vm=np.zeros(4)
                        vp=np.zeros(4)
                        vm[0]=np.mean(Y[(x==-1)&(X[:,j]==-1)&(X[:,i]==-1)])
                        vm[1]=np.mean(Y[(x==-1)&(X[:,j]==-1)&(X[:,i]==+1)])
                        vm[2]=np.mean(Y[(x==-1)&(X[:,j]==+1)&(X[:,i]==-1)])
                        vm[3]=np.mean(Y[(x==-1)&(X[:,j]==+1)&(X[:,i]==+1)])
                        vp[0]=np.mean(Y[(x==+1)&(X[:,j]==-1)&(X[:,i]==-1)])
                        vp[1]=np.mean(Y[(x==+1)&(X[:,j]==-1)&(X[:,i]==+1)])
                        vp[2]=np.mean(Y[(x==+1)&(X[:,j]==+1)&(X[:,i]==-1)])
                        vp[3]=np.mean(Y[(x==+1)&(X[:,j]==+1)&(X[:,i]==+1)])
                        ind=[0,1,2,3]
                        ax.set_xlabel('Factors Combinations')
                        ax.set_ylabel('Responce')
                        ax.set_title('Block Plot: Responce '+self.responcecomboBox.currentText()+', Factor '+
                        self.factorcomboBox.currentText()+', interaction '+Lcx[labels[i]-1]+'-'+Lcx[labels[j]-1])
                        ax.plot(ind,vm,'_',ind,vp,'+')
                        ax.set_xticks(ind)
                        ax.set_xticklabels(['(- -)','(-,+)','(+,-)','(+,+)'], rotation='horizontal')
                        ax.set_xlim([-1,4])
                        ax.set_ylim([ymin,ymax])
                        currentAxis = plt.gca()
                        for k in range(4):
                            someX=k
                            someY=np.mean([vm[k],vp[k]])
                            d=abs(vm[k]-vp[k])*1.1
                            currentAxis.add_patch(Rectangle((someX-.1,someY-d/2),0.2,d,fill=False))
        elif self.vsfactoradioButton.isChecked():
            ax=fig.add_subplot(111)
            for i in range(nr):
                for j in range(ncx):
                   if((X[i,j]!=1)&(X[i,j]!=-1)):
                        QtWidgets.QMessageBox.critical(self,'Output Limit',
                        'There are more then 2 levels\n I am not able to plot',QtWidgets.QMessageBox.Ok)
                        return()
            x=X[:,nf]
            Y=Y[:,ny]
            ym=Y[x==-1]
            yp=Y[x==+1]
            ind=range(1,3)
            ax.set_ylabel('Responce')
            ax.set_title('Block Plot: Responce '+self.responcecomboBox.currentText()
            +' vs. Factor '+self.factorcomboBox.currentText())
            ax.boxplot([ym,yp])
            ax.set_xticks(ind)
            ax.set_xticklabels(['(-)','(+)'], rotation='horizontal')
        elif self.youdenradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            nfac=len(DOE.lfac)
            sfac=np.array([str(i) for i in DOE.lfac])
            x=np.zeros(nfac)
            y=np.zeros(nfac)
            for i in range(nfac):
                Xp=X[:,(DOE.lfac[i][0]-1)]
                for j in range(1,len(DOE.lfac[i])):
                    Xp=Xp*X[:,(DOE.lfac[i][j]-1)]
                x[i]=Y[Xp==-1].mean()
                y[i]=Y[Xp==+1].mean()
            ax.set_ylabel('Average Responce for +1')
            ax.set_xlabel('Average Responce for -1')
            ax.set_title('Youden Plot: Responce :'+self.responcecomboBox.currentText())
            ax.scatter(x,y,color='red',alpha=0.3,marker='o')
            ax.scatter(Y.mean(),Y.mean(),color='blue',s=60,marker='+')
            ax.axhline(y=Y.mean(),color='red',linewidth=1.5,zorder=0)
            ax.axvline(x=Y.mean(),color='red',linewidth=1.5,zorder=0)
            for i in range(nfac):
                ax.annotate(sfac[i],(x[i],y[i]),rotation=0,size=12)
        elif self.effectradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            nfac=len(DOE.lfac)
            sfac=np.array([str(i) for i in DOE.lfac])
            x=np.zeros(nfac)
            y=np.zeros(nfac)
            for i in range(nfac):
                Xp=X[:,(DOE.lfac[i][0]-1)]
                for j in range(1,len(DOE.lfac[i])):
                    Xp=Xp*X[:,(DOE.lfac[i][j]-1)]
                x[i]=Y[Xp==-1].mean()
                y[i]=Y[Xp==+1].mean()
            eff=abs(x-y)
            order=eff.argsort()
            width=0.35 
            ind=np.arange(1,nfac+1)
            ax.bar(ind,eff[order],width,color='blue')
            ax.set_xticks(ind+width/2)
            ax.set_xticklabels(sfac[order], rotation='vertical')
            ax.set_xlabel('Factors') 
            ax.set_ylabel('|Effects|') 
            ax.set_title('Effect Plot for '+self.responcecomboBox.currentText())
        elif self.halfradioButton.isChecked():
            ax=fig.add_subplot(111)
            Y=Y[:,ny]
            nfac=len(DOE.lfac)
            sfac=np.array([str(i) for i in DOE.lfac])
            x=np.zeros(nfac)
            y=np.zeros(nfac)
            for i in range(nfac):
                Xp=X[:,(DOE.lfac[i][0]-1)]
                for j in range(1,len(DOE.lfac[i])):
                    Xp=Xp*X[:,(DOE.lfac[i][j]-1)]
                x[i]=Y[Xp==-1].mean()
                y[i]=Y[Xp==+1].mean()
            eff=abs(x-y)
            order=eff.argsort()
            ind=[sp.stats.halfnorm.ppf(i/(nfac+1)) for i in range(1,nfac+1)]
            ax.scatter(ind,eff[order],color='blue',s=60,marker='+')
            for i in range(nfac):
                ax.annotate(sfac[order][i],(ind[i],eff[order][i]),rotation=-90,size=12)
            ax.set_xlabel('Half Normal Distribution Order') 
            ax.set_ylabel('Ordered |Effects|') 
            ax.set_title('Half Normal Distribution Plot for '+self.responcecomboBox.currentText())
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
        ax.annotate(w_text,xy=(0.75,0.95),xycoords='figure fraction',fontsize=8)
        self.rmmpl()
        self.addmpl(fig)        
    def reset(self):
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

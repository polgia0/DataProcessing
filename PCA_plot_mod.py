from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import PCA,DS
from PCA_model_mod import pca_model
import pandas as pd
import numpy as np
import scipy as sp
import sklearn as sk
import math
from matplotlib.patches import Ellipse
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_pcaplotDialog,QDialog=loadUiType('pcaplot.ui')
class pcaplotDlg(QtWidgets.QDialog,Ui_pcaplotDialog):
    def __init__(self,parent=None):
        super(pcaplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        for x in range(PCA.ncp):
            self.XcomboBox.addItem(str(x+1))
            self.YcomboBox.addItem(str(x+1))
        Lr=DS.Lr[DS.Ir]
        Ts=DS.Ts[DS.Ir]
        Lr=Lr[-Ts]
        for x in Lr:
            self.objcomboBox.addItem(str(x))
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
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
        fig=Figure()
        ax=fig.add_subplot(111)
        c1=self.XcomboBox.currentIndex()
        c2=self.YcomboBox.currentIndex()
        Lc=DS.Lc[DS.Ic]
        Lr=DS.Lr[DS.Ir]
        Ts=DS.Ts[DS.Ir]
        Cr=DS.Cr[DS.Ir]
        Lr=Lr[-Ts]
        Cr=Cr[-Ts]
        nr=len(Lr)
        nc=len(Lc)
        if(self.varianceradioButton.isChecked()):
            ind=range(1,len(PCA.rv)+1)
            ax.bar(ind,PCA.rv,align='center')
            ax.set_xticks(ind)
            ax.set_xticklabels(ind, rotation='vertical')
            ax.set_xlabel('Component Number') 
            ax.yaxis.grid()
            ax.set_title('Explained Variance')
        elif self.variancecumradioButton.isChecked():
            rvc=PCA.rv.cumsum()
            ind=range(1,len(rvc)+1)
            ax.bar(ind,rvc,align='center')
            ax.set_xticks(ind)
            ax.set_xticklabels(ind, rotation='vertical')
            ax.set_xlabel('Component Number') 
            ax.yaxis.grid()
            ax.set_title('Cumulative Explained Variance')
        elif self.loadingradioButton.isChecked():
            color=['red']*nc
            if self.CcheckBox.isChecked():
                 color=DS.Cc[DS.Ic]
            rv=PCA.rv*100
            llim=[PCA.lo.min(),0,PCA.lo.max()]
            vllim=1.1*max(abs(np.array(llim)))
            ax.scatter(PCA.lo[:,c1],PCA.lo[:,c2],color='k',alpha=0.3,marker='.')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i, txt in enumerate(Lc):
                ax.arrow(0,0,PCA.lo[:,c1][i],PCA.lo[:,c2][i], fc="r", ec="r",head_width=0.02,head_length=0.03,color=color[i])
                ax.annotate(txt,(PCA.lo[:,c1][i],PCA.lo[:,c2][i]))
            ax.set_xlim([math.copysign(vllim,llim[0]),math.copysign(vllim,llim[2])])
            ax.set_ylim([math.copysign(vllim,llim[0]),math.copysign(vllim,llim[2])])
            ax.set_title('Loading Plot ('+str(round(rv[c1]+rv[c2],2))+'%)')
            ax.set_xlabel('Comp.'+self.XcomboBox.currentText()+' ('+str(round(rv[c1],2))+'%)')
            ax.set_ylabel('Comp.'+self.YcomboBox.currentText()+' ('+str(round(rv[c2],2))+'%)')
        elif self.scoreradioButton.isChecked():
            vcol=['red']*nr
            if self.CcheckBox.isChecked():
                 vcol=Cr
            rv=PCA.rv*100
            slim=[PCA.sco.min(),0,PCA.sco.max()]
            vslim=1.2*max(abs(np.array(slim)))
            ax.scatter(PCA.sco[:,c1],PCA.sco[:,c2],alpha=0.3,color=vcol,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            if self.VcheckBox.isChecked():
                for i,txt in enumerate(Lr):
                    ax.annotate(txt,(PCA.sco[:,c1][i],PCA.sco[:,c2][i]))
            ax.set_xlim([math.copysign(vslim,slim[0]),math.copysign(vslim,slim[2])])
            ax.set_ylim([math.copysign(vslim,slim[0]),math.copysign(vslim,slim[2])])
            ax.set_title('Score Plot ('+str(round(rv[c1]+rv[c2],2))+'%)')
            ax.set_xlabel('Comp.'+self.XcomboBox.currentText()+' ('+str(round(rv[c1],2))+'%)')
            ax.set_ylabel('Comp.'+self.YcomboBox.currentText()+' ('+str(round(rv[c2],2))+'%)')
        elif self.ellipseradioButton.isChecked():
            st2=PCA.rv*nc
            alpha=(100-self.alphaspinBox.value())/100
            fn=np.array(range(1,(PCA.ncp+1)))
            fd=(nr+1)-fn
            fn =tuple(fn)
            fd =tuple(fd)
            falpha=sp.stats.f.ppf(alpha,fn,fd)
            color=[]
            txt=[]
            for i in range(nr):
                txt.append('')
                color.append('blue')
                rp=(PCA.sco[:,c1][i])**2/st2[c1]+(PCA.sco[:,c2][i])**2/st2[c2]
                if(rp>falpha[PCA.ncp-1]):
                    color[i]='red'
                    txt[i]=Lr[i]
            slim=[PCA.sco.min(),0,PCA.sco.max()]
            vslim=1.2*max(abs(np.array(slim)))
            ax.scatter(PCA.sco[:,c1],PCA.sco[:,c2],alpha=0.3,color=color,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i,label in enumerate(txt):
                ax.annotate(label,(PCA.sco[:,c1][i],PCA.sco[:,c2][i]))
            ax.set_xlim([math.copysign(vslim,slim[0]),math.copysign(vslim,slim[2])])
            ax.set_ylim([math.copysign(vslim,slim[0]),math.copysign(vslim,slim[2])])
            ax.set_title('Score Plot ('+str(round(PCA.rv[c1]+PCA.rv[c2],2))+'%)')
            ax.set_xlabel('Comp.'+self.XcomboBox.currentText()+' ('+str(round(PCA.rv[c1],2))+'%)')
            ax.set_ylabel('Comp.'+self.YcomboBox.currentText()+' ('+str(round(PCA.rv[c2],2))+'%)')
            ella=Ellipse(xy=(0,0),width=2*math.sqrt(falpha[PCA.ncp-1]*st2[c1]),height=2*math.sqrt(falpha[PCA.ncp-1]*st2[c2]),color='red')
            ella.set_facecolor('none')
            ax.add_artist(ella)
            alpha=alpha*100
            ax.annotate(str(round(alpha,0))+'%',xy=(0,-math.sqrt(falpha[PCA.ncp-1]*st2[c2])),color='red')
        elif self.biplotradioButton.isChecked():
            xs=PCA.sco[:,c1]
            ys=PCA.sco[:,c2]
            if self.VcheckBox.isChecked():
                for i,(t,x,y) in enumerate(zip(Lr,xs,ys)):
                    ax.text(x,y,t,color=Cr[i],ha='center',va='center')
                xmin,xmax=xs.min(),xs.max()
                ymin,ymax=ys.min(),ys.max()
                xpad=(xmax-xmin)*0.1
                ypad=(ymax-ymin)*0.1
                ax.set_xlim(xmin-xpad,xmax+xpad)
                ax.set_ylim(ymin-ypad,ymax+ypad)
            else:
                ax.scatter(xs,ys,c=Cr,marker='o')
            for i,col in enumerate(Lc):
                x,y=PCA.lo[i,c1],PCA.lo[i,c2]
                ax.arrow(0, 0, x, y, color='r',width=0.002, head_width=0.05)
                ax.text(x* 1.4, y * 1.4, col, color='r', ha='center', va='center')
            ax.set_xlabel('PC{}'.format(c1 + 1))
            ax.set_ylabel('PC{}'.format(c2 + 1))
        elif self.ht2radioButton.isChecked():
            ind=np.array(range(1,nr+1))
            colors=[]
            for i in range(nr):
                colors.append('blue')
                if(PCA.ht2[i]>PCA.T95):
                    colors[i]='red'
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlabel('Object') 
            ax.bar(ind,PCA.ht2,align='center',color=colors)
            ax.yaxis.grid()
            ax.set_title('Hoteling T2 for '+str(PCA.ncp)+' components model')
            ax.axhline(y=PCA.T95,color='red',linewidth=1.5,zorder=0)
            ax.annotate('95%',xy=(0,PCA.T95),color='red')
            ax.axhline(y=PCA.T99,color='red',linewidth=1.5,zorder=0)
            ax.annotate('99%',xy=(0,PCA.T99),color='red')
            ax.set_ylim([0,1.2*max([PCA.T99,max(PCA.ht2)])])
            ax.set_xlim([0,nr+1])
        elif self.speradioButton.isChecked():
            ind=np.array(range(1,nr+1))
            colors=[]
            for i in range(nr):
                colors.append('blue')
                if(PCA.Q[i]>PCA.Q95):
                     colors[i]='red'
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick, rotation='vertical',fontsize=8)
            ax.set_xlabel('Object') 
            ax.scatter(ind,PCA.Q,color=colors)
            ax.set_ylabel('Q-SPE') 
            ax.yaxis.grid()
            ax.set_title('Q-SPE for '+str(PCA.ncp)+' components model')
            ax.axhline(y=PCA.Q95,color='red',linewidth=1.5,zorder=0)
            ax.annotate('95%',xy=(0,PCA.Q95),color='red')
            ax.axhline(y=PCA.Q99,color='red',linewidth=1.5,zorder=0)
            ax.annotate('99%',xy=(0,PCA.Q99),color='red')
            ax.set_ylim([0,1.2*max([PCA.Q99,max(PCA.Q)])])
        elif self.columnresradioButton.isChecked():
            ind=np.array(range(1,nc+1))
            if(nc>30):
                itick=np.linspace(0,nc-1,20).astype(int)
                ltick=Lc[itick]
            else:
                itick=ind
                ltick=Lc
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick, rotation='vertical')
            ax.set_xlabel('Variable') 
            ax.bar(ind,PCA.cres,align='center',width=0.8)
            ax.set_ylabel('Column R2 over all components') 
            ax.yaxis.grid()
            ax.set_title('Column Residual Plot for '+str(PCA.ncp)+' components space')
            ax.set_ylim([0,1])
            ax.set_xlim([0,nc+1])
        elif self.specontribradioButton.isChecked():
            obj=self.objcomboBox.currentIndex()
            res=PCA.res[obj,:]
            ind=np.array(range(1,nc+1))
            if(nc>30):
                itick=np.linspace(0,nc-1,20).astype(int)
                ltick=Lc[itick]
            else:
                itick=ind
                ltick=Lc
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick, rotation='vertical')
            ax.set_xlabel('Variable') 
            ax.bar(ind,res,align='center',width=0.8)
            ax.set_ylabel('Variable Contributon on SPE') 
            ax.yaxis.grid()
            ax.set_title('Residual Plot for object '+self.objcomboBox.currentText())
            ax.set_xlim([0,nc+1])
        elif self.cvradioButton.isChecked():
            Xc=pd.DataFrame(PCA.Xc)
            np.random.seed(nr)
            kf=sk.model_selection.KFold(n_splits=self.segmentspinBox.value(),shuffle=True)
            Xcv=pd.DataFrame(0,index=range(nr),columns=range(nc))
            for train, test in kf.split(Xc):
                 Xt=Xc.iloc[train,:]
                 T,P,LAM,SSX,RV,X,SPE,SSE,R2X,HT2,Res,Xm,Xstd,MQ,MT,Q95,T95,Q99,T99=pca_model(Xt,PCA.ncp,False,False,False)
                 X_test=Xc.iloc[test,:]
                 T_test=np.dot(X_test,P)
                 Xcv.iloc[test,:]=np.dot(T_test,P.T)
            PCA.Xcv=Xcv
            Xcv=np.array(Xcv)
            Xc=np.array(Xc)
            for i in range(nc):
                ax.scatter(Xc[:,i],Xcv[:,i],color =(0,i/float(nc),0,1),alpha=0.3,marker='o')
            if self.VcheckBox.isChecked():
                for i in range(nc):
                    for j,txt in enumerate(Lr):
                        ax.annotate(txt,(Xc[j,i],Xcv[j,i]))
            ax.set_xlabel('Original Data')
            ax.set_ylabel('CV Predicted Data')
            ax.xaxis.grid()
            ax.yaxis.grid()
            ax.set_ylim([-3,3])
            ax.set_xlim([-3,3])
            ax.set_title('Predicted Data vs. Original')
            ax.add_line(Line2D([-3,3],[-3,3],color='red')) 
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
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
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

from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import PLS,DS
from PLS_model_mod import pls_model
from cycler import cycler
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
Ui_plsplotDialog,QDialog=loadUiType('plsplot.ui')
class plsplotDlg(QtWidgets.QDialog,Ui_plsplotDialog):
    def __init__(self,parent=None):
        super(plsplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        for x in range(PLS.ncp):
            self.XcomboBox.addItem(str(x+1))
            self.YcomboBox.addItem(str(x+1))
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Lcy=Lc[Gc]
        for x in Lcy:
            self.responcecomboBox.addItem(str(x))
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
        ny=self.responcecomboBox.currentIndex()
        Yname=self.responcecomboBox.currentText()
        Ts=DS.Ts[DS.Ir]
        Gc=DS.Gc[DS.Ic]
        Cr=DS.Cr[DS.Ir]
        Cr=Cr[-Ts]
        Lr=DS.Lr[DS.Ir] 
        Lr=Lr[-Ts]
        Lc=DS.Lc[DS.Ic]
        Lcx=Lc[-Gc]
        Lcy=Lc[Gc]
        Cc=DS.Cc[DS.Ic]
        Ccx=Cc[-Gc]
        ncx=len(Lcx)
        ncy=len(Lcy)
        nr=len(Lr)
        Y=DS.Raw.loc[DS.Ir,DS.Ic][Lcy]
        Y=Y[-Ts]
        if(self.fittedradioButton.isChecked()):
            Y=Y.values
            ax.scatter(Y[:,ny],PLS.Ys[:,ny],color=Cr,alpha=0.3,marker='o')
            xmin,xmax=ax.get_xlim()
            ax.set_ylim([xmin,xmax])
            ax.set_xlabel(Yname+' measured')
            ax.set_ylabel(Yname+' fitted')
            ax.set_title('Fitted vs. Measured Plot for '+Yname+ ' : Model '+str(PLS.ncp)+' components')
            ax.add_line(Line2D([xmin,xmax],[xmin,xmax],color='red'))
            if self.VcheckBox.isChecked():
                for i in range(nr):
                    ax.annotate(Lr[i],(Y[:,c1][i],PLS.Ys[:,c1][i]))
        elif(self.allfittedradioButton.isChecked()):
            Yc=pd.melt(pd.DataFrame(PLS.Yc))
            Ysc=pd.melt(pd.DataFrame(PLS.Ysc))
            df=pd.DataFrame(dict(X=Yc['value'],Y=Ysc['value'],point=Yc['variable']))
            np.random.seed(nr)
            groups=df.groupby('point')
            colors=pd.tools.plotting._get_standard_colors(len(groups),color_type='random')
            ax.set_prop_cycle(cycler('color',colors))
            ax.margins(0.05)
            for group in groups:
                ax.plot(group[1].X,group[1].Y, marker='o',linestyle='',ms=5,label=Lcy[group[0]])
            ax.set_xlabel('Measured Data')
            ax.set_ylabel('Fitted Data')
            Dmin=min([Yc.value.min(),Ysc.value.min()])
            Dmax=max([Yc.value.max(),Ysc.value.max()])
            ax.set_xlim([Dmin,Dmax])
            ax.set_ylim([Dmin,Dmax])
            ax.set_title('Measured vs. Fitted Data')
            ax.add_line(Line2D([Dmin,Dmax],[Dmin,Dmax],color='red')) 
            ax.legend(loc='best') 
        elif(self.coefficientradioButton.isChecked()):
            B=PLS.B[:,ny]
            ind=np.array(range(1,ncx+1))
            if(ncx>30):
                itick=np.linspace(0,ncx-1,20).astype(int)
                ltick=Lcx[itick]
            else:
                itick=ind
                ltick=Lcx
            if self.CcheckBox.isChecked():
                vcol=Ccx
            else:
                vcol='blue'
            ax.bar(ind,B,align='center',color=vcol)
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlim([0,ncx+1])
            ax.set_xlabel('Variables') 
            ax.set_ylabel('Coefficients') 
            ax.set_title('Coefficients for '+Yname+' : Model '+str(PLS.ncp)+' components')
        elif self.wiradioButton.isChecked():
            WS=np.dot(PLS.WS,np.linalg.inv(PLS.C))
            txt=range(1,ncx+1)
            if self.VcheckBox.isChecked():
                txt=Lcx
            vcol=ncx*['blue']
            if self.CcheckBox.isChecked():
                vcol=Ccx
            ax.scatter(WS[:,c1],WS[:,c2],alpha=0.3,color=vcol,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i in range(ncx):
                ax.annotate(txt[i],(WS[:,c1][i],WS[:,c2][i]))
            lim=[WS.min(),0, WS.max()]
            vlim=max(abs(np.array(lim)))*1.2
            ax.set_xlim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_ylim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_title('Weight Plot: Model with '+str(PLS.ncp)+' components')
            ax.set_xlabel('W*'+str(c1+1))
            ax.set_ylabel('W*'+str(c2+1))
        elif(self.qiradioButton.isChecked()):
            txt=range(1,ncy+1)
            if self.VcheckBox.isChecked():
                txt=Lcx
            vcol=ncy*['blue']
            if self.CcheckBox.isChecked():
                vcol=Ccx
            ax.scatter(PLS.Q[:,c1],PLS.Q[:,c2],alpha=0.3,color=vcol,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i in range(ncy):
                ax.annotate(txt[i],(PLS.Q[:,c1][i],PLS.Q[:,c2][i]))
            lim=[PLS.Q.min(),0,PLS.Q.max()]
            vlim=max(abs(np.array(lim)))*1.2
            ax.set_xlim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_ylim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_title('Loading Plot: Model with '+str(PLS.ncp)+' components')
            ax.set_xlabel('C'+str(c1+1))
            ax.set_ylabel('C'+str(c2+1))
        elif(self.wqiradioButton.isChecked()):
            WS=np.dot(PLS.WS,np.linalg.inv(PLS.C))
            txtc=range(1,ncy+1)
            txtw=range(1,ncx+1)
            if self.VcheckBox.isChecked():
                txt=DS.Lc[DS.Ic]
                txtc=txt[DS.Gc[DS.Ic]]
                txtw=txt[-DS.Gc[DS.Ic]]
            vcolc=ncy*['red']
            vcolw=ncx*['blue']
            if self.CcheckBox.isChecked():
                vcol=DS.Cc[DS.Ic]
                vcolc=vcol[DS.Gc[DS.Ic]]
                vcolw=vcol[-DS.Gc[DS.Ic]]
            ax.scatter(PLS.Q[:,c1],PLS.Q[:,c2],alpha=0.3,color=vcolc,s=30,marker='o')
            ax.scatter(WS[:,c1],WS[:,c2],alpha=0.3,color=vcolw,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i in range(ncy):
                ax.annotate(txtc[i],(PLS.Q[:,c1][i],PLS.Q[:,c2][i]))
            for i in range(ncx):
                ax.annotate(txtw[i],(WS[:,c1][i],WS[:,c2][i]))
            lim=[PLS.Q.min(),0,PLS.Q.max(),WS.max(),WS.min()]
            vlim=max(abs(np.array(lim)))*1.2
            ax.set_xlim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_ylim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_title('Loading Plot: Model with '+str(PLS.ncp)+' components')
            ax.set_xlabel('W* Q'+str(c1+1))
            ax.set_ylabel('W* Q'+str(c2+1))
        elif(self.ht2radioButton.isChecked()):
            ind=np.array(range(1,nr+1))
            colors=[]
            for i in range(nr):
                colors.append('blue')
                if(PLS.HT2[i]>PLS.T95):
                    colors[i]='red'
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.bar(ind,PLS.HT2,align='center',color=colors)
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlabel('Object') 
            ax.set_title('Hoteling T2 for '+str(PLS.ncp)+' components model')
            ax.axhline(y=PLS.T95,color='red',linewidth=1.5,zorder=0)
            ax.annotate('95%',xy=(0,PLS.T95),color='red')
            ax.axhline(y=PLS.T99,color='red',linewidth=1.5,zorder=0)
            ax.annotate('99%',xy=(0,PLS.T99),color='red')
            ax.set_ylim([0,1.2*max([PLS.T99,max(PLS.HT2)])])
            ax.set_xlim([0,nr+1])
        elif(self.scoreradioButton.isChecked()):
            st2=PLS.T.var(axis=0)
            alpha=(100-self.alphaspinBox.value())/100
            fn=np.array(range(1,(PLS.ncp+1)))
            fd=(nr+1)-fn
            fn =tuple(fn)
            fd =tuple(fd)
            falpha=sp.stats.f.ppf(alpha,fn,fd)
            colors=[]
            txt=[]
            for i in range(nr):
                txt.append('')
                colors.append('blue')
                rp=(PLS.T[:,c1][i])**2/st2[c1]+(PLS.T[:,c2][i])**2/st2[c2]
                if(rp>falpha[PLS.ncp-1]):
                    colors[i]='red'
                    txt[i]=Lr[i]
            ax.scatter(PLS.T[:,c1],PLS.T[:,c2],alpha=0.3,color=colors,s=30,marker='o')
            ax.scatter(0,0,color='red',s=60,marker='+')
            for i in range(nr):
                ax.annotate(txt[i],(PLS.T[:,c1][i],PLS.T[:,c2][i]))
            lim=[PLS.T.min(),0,PLS.T.max()]
            vlim=max(abs(np.array(lim)))*1.2
            ax.set_xlim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_ylim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_title('Score Plot: Model with '+str(PLS.ncp)+' components')
            ax.set_xlabel('Comp.'+str(c1+1)+' ('+str(round(st2[c1]/PLS.ncp*100,2))+'%)')
            ax.set_ylabel('Comp.'+str(c2+1)+' ('+str(round(st2[c2]/PLS.ncp*100,2))+'%)')
            ella=Ellipse(xy=(0,0),width=2*math.sqrt(falpha[PLS.ncp-1]*st2[c1]),height=2*math.sqrt(falpha[PLS.ncp-1]*st2[c2]),color='red')
            ella.set_facecolor('none')
            ax.add_artist(ella)
            alpha=alpha*100
            ax.annotate(str(round(alpha,0))+'%',xy=(0,-math.sqrt(falpha[PLS.ncp-1]*st2[c2])),color='red')
        elif(self.spexradioButton.isChecked()):
            T95=sp.stats.chi2.ppf(0.95,nr)/(nr-PLS.ncp)
            T99=sp.stats.chi2.ppf(0.99,nr)/(nr-PLS.ncp)
            ind=np.array(range(1,nr+1))
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.bar(ind,PLS.SPEX,color='blue')
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlabel('X Variables') 
            ax.set_ylabel('SPE X') 
            ax.set_title('SPE X for '+str(PLS.ncp)+' components model')
            ax.set_ylim([0,1.2*max([max(PLS.SPEX),T99])])
            ax.set_xlim([0,max(itick)])
            ax.axhline(y=T95,color='red',linewidth=1.5)
            ax.annotate('95%',xy=(0,T95),color='red')
            ax.axhline(y=T99,color='red',linewidth=1.5)
            ax.annotate('99%',xy=(0,T99),color='red')
        elif self.speyradioButton.isChecked():
            T95=sp.stats.chi2.ppf(0.95,nr)/(nr-PLS.ncp)
            T99=sp.stats.chi2.ppf(0.99,nr)/(nr-PLS.ncp)
            ind=np.array(range(1,nr+1))
            if(nr>30):
                itick=np.linspace(0,nr-1,20).astype(int)
                ltick=Lr[itick]
            else:
                itick=ind
                ltick=Lr
            ax.bar(ind,PLS.SPEY,color='blue')
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlabel('Y Variables') 
            ax.set_ylabel('SPE Y') 
            ax.set_title('SPE Y for '+str(PLS.ncp)+' components model')
            ax.set_ylim([0,1.2*max([max(PLS.SPEY),T99])])
            ax.set_xlim([0,max(itick)])
            ax.axhline(y=T95,color='red',linewidth=1.5)
            ax.annotate('95%',xy=(0,T95),color='red')
            ax.axhline(y=T99,color='red',linewidth=1.5)
            ax.annotate('99%',xy=(0,T99),color='red')
        elif self.cvradioButton.isChecked():
            X0=pd.DataFrame(PLS.Xc)
            Y0=pd.DataFrame(PLS.Yc)
            np.random.seed(nr)
            kf=sk.model_selection.KFold(n_splits=self.segmentspinBox.value(),shuffle=True)
            Ycv=pd.DataFrame(0,index=range(nr),columns=range(ncy))
            for train, test in kf.split(X0):
                 X=X0.iloc[train,:]
                 Y=Y0.iloc[train,:]
                 Xm,Ym,Sx,Sy,Xc,Yc,SSX,SSY,P,C,U,T,Q,W,WS,B,Ysc,Ys,R2,SPEX,SPEY,HT2,VIP,T95,T99=pls_model(X,Y,PLS.ncp,False,False,False)
                 X_test=X0.iloc[test,:]
                 Ycv.iloc[test,:]=np.dot(X_test,B)
            Y0=Y0.values
            PLS.Ycv=Ycv.values
            Ycvs=PLS.Ym+PLS.Sy*Ycv.T
            PLS.Ycvs=Ycvs.T.values
            Y=PLS.Ym+PLS.Sy*Y0.T
            Y=Y.T
            if self.CcheckBox.isChecked():
                vcol=Cr
            else:
                vcol='red'
            ax.scatter(Y[:,ny],PLS.Ycvs.iloc[:,ny],color=vcol,alpha=0.3,marker='o')
            if self.VcheckBox.isChecked():       
                for i in range(nr):
                    ax.annotate(Lr[i],(Y[:,ny][i],PLS.Ycvs.iloc[:,ny][i]))
            ax.set_xlabel(Yname+' measured')
            ax.set_ylabel(Yname+' CV predicted')
            xmin,xmax=ax.get_xlim()
            ax.set_ylim([xmin,xmax])
            ax.set_title('CV Predicted vs. Measured Plot for '+Yname+' : Model '+str(PLS.ncp)+' components')
            ax.add_line(Line2D([xmin,xmax],[xmin,xmax],color='red'))
        elif self.turadioButton.isChecked():
            if self.CcheckBox.isChecked():
                vcol=Cr
            else:
                vcol='red'
            ax.scatter(PLS.T[:,c1],PLS.U[:,c1],color=vcol,alpha=0.3,marker='o')
            if self.VcheckBox.isChecked():       
                for i in range(nr):
                    ax.annotate(Lr[i],(PLS.T[:,c1][i],PLS.U[:,c1][i]))
            ax.set_xlabel('T('+str(c1+1)+')')
            ax.set_ylabel('U('+str(c1+1)+')')
            ax.set_title('T vs. U Plot')
        elif self.vipradioButton.isChecked():
            ind=np.array(range(1,ncx+1))
            if(ncx>30):
                itick=np.linspace(0,ncx-1,20).astype(int)
                ltick=Lcx[itick]
            else:
                itick=ind
                ltick=Lcx
            colors=[]
            for i in range(ncx):
                colors.append('blue')
                if(PLS.VIP[i]>1):
                    colors[i]='red'
            ax.bar(ind,PLS.VIP,align='center',color=colors)
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlim([0,max(itick)+1])
            ax.set_xlabel('Variables') 
            ax.yaxis.grid()
            ax.set_title('Variable Importance Plot (VIP): Model '+str(PLS.ncp)+' components')
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

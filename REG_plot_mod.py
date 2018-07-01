from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import REG,DS
import numpy as np
import sklearn as sk
import pandas as pd
import matplotlib.pyplot as plt
from distutils.util import strtobool
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_regplot,QDialog=loadUiType('regplot.ui')
Ui_surtab,QDialog=loadUiType('surtab.ui')
class regplotDlg(QtWidgets.QDialog,Ui_regplot):
    def __init__(self,parent=None):
        super(regplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
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
        fig=Figure()
        ax=fig.add_subplot(111)
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Ts=DS.Ts[DS.Ir]
        X=data.loc[:,-Gc]
        Y=data.loc[:,Gc]
        Yname=Y.columns[0]
        X=X[-Ts]
        Y=Y[-Ts]
        Lr=DS.Lr[DS.Ir]
        Cr=DS.Cr[DS.Ir]
        Lr=Lr[-Ts]
        Cr=Cr[-Ts]
        nr=len(Lr)
        Lc=DS.Lc[DS.Ic]
        Lcx=Lc[-Gc]
        ncx=len(Lcx)
        Lcy=Lc[Gc]
        scoretr=REG.lr.score(X,Y)
        np.random.seed(REG.seed)
        if self.coeffradioButton.isChecked():
            B=REG.lr.coef_            
            ind=np.array(range(1,ncx+1))
            if(ncx>30):
                itick=np.linspace(0,ncx-1,20).astype(int)
                ltick=Lcx[itick]
            else:
                itick=ind
                ltick=Lcx
            vcol=[]
            for i in ind:
                if(REG.pS[i]<0.05):vcol.append('red')
                else:vcol.append('blue')
            ax.bar(ind,B,align='center',color=vcol,label='Score: {:04.2f}'.format(scoretr))
            ax.errorbar(ind,B,yerr=REG.dB[1:],fmt='o',ecolor='green')
            ax.set_xticks(itick)
            ax.set_xticklabels(ltick,rotation='vertical')
            ax.set_xlim([0,ncx+1])
            ax.set_xlabel('Variables') 
            ax.set_ylabel('Coefficients') 
            ax.set_title('Regression for '+Lcy[0]+' Intercept:  {:10.4f}-{:10.4f}-{:10.4f}'.format
                    (REG.lr.intercept_-REG.dB[0],REG.lr.intercept_,REG.lr.intercept_+REG.dB[0]))
            ax.set_ylabel('Coefficients')
            ax.legend(loc='upper left')
        elif self.resradioButton.isChecked():
            Yfit=REG.lr.predict(X)
            Q=np.squeeze(Y.values)-Yfit
            ind=range(1,nr+1)
            vcol=nr*['blue']
            if self.CcheckBox.isChecked():
                vcol=Cr
            ax.scatter(ind,Q,alpha=0.3,color=vcol,s=30,marker='o')
            if self.VcheckBox.isChecked():
                for i in range(nr):
                    ax.annotate(Lr[i],(ind[i],Q[i]))
            lim=[Q.min(),0, Q.max()]
            vlim=max(abs(np.array(lim)))*1.1
            ax.set_xlim([0,nr+2])
            ax.set_ylim([np.copysign(vlim,lim[0]),np.copysign(vlim,lim[2])])
            ax.set_title('Residual Plot: Model with for '+Lcy[0])
            ax.set_xlabel('Point Index')
            ax.set_ylabel('Residuals')            
        elif self.cvradioButton.isChecked():
            scores=sk.model_selection.cross_val_score(REG.lr,X,Y,cv=self.segmentspinBox.value())
            REG.Ycv=sk.model_selection.cross_val_predict(REG.lr,X,Y,cv=self.segmentspinBox.value())
            if self.CcheckBox.isChecked():
                vcol=Cr
            else:
                vcol='red'
            ax.scatter(Y,REG.Ycv,color=vcol,alpha=0.3,marker='o')
            if self.VcheckBox.isChecked():
                for i in range(nr):
                    ax.annotate(Lr[i],(Y.values[i],REG.Ycv[i]))
            ax.set_xlabel(Yname+' measured')
            ax.set_ylabel(Yname+' CV predicted')
            xmin,xmax=ax.get_xlim()
            ax.set_ylim([xmin,xmax])
            ax.set_title('CV Predicted Plot for '+Lcy[0]+' : Score {:04.2f}'.format(scores.mean()))
            ax.add_line(Line2D([xmin,xmax],[xmin,xmax],color='red'))
        elif self.dispersionradioButton.isChecked():
            fig=plt.figure()
            ax = fig.add_subplot(111)
            cax=ax.matshow(REG.dism)
            fig.colorbar(cax, format='%.2E')
            ax.set_title('Trace = {:10.4E}'.format(np.trace(REG.dism)))
        elif self.leverageradioButton.isChecked():           
            Ftable=surtabDlg.launch(None)
            if len(np.shape(Ftable))==0: return()
            if np.argmax(Ftable['X axis'].values)==np.argmax(Ftable['Y axis'].values):
                QtWidgets.QMessageBox.critical(self,'Error',"Two variables on the same axis",QtWidgets.QMessageBox.Ok)
                return()
            fig=plt.figure()
            ax=fig.add_subplot(111)
            npts=20
            xname=Ftable[(Ftable['X axis']==True).values].index[0]
            yname=Ftable[(Ftable['Y axis']==True).values].index[0]
            cname=Ftable[(Ftable['Constant']==True).values].index.tolist()
            cvalue=Ftable.loc[(Ftable['Constant']==True).values,'value']
            x=np.linspace(float(Ftable['min'][xname]),float(Ftable['max'][xname]),npts)
            y=np.linspace(float(Ftable['min'][yname]),float(Ftable['max'][yname]),npts)
            px=[]
            py=[]
            for i in range(npts):
                for j in range(npts):
                    px.append(x[i])
                    py.append(y[j])
            mx=pd.DataFrame({xname:px,yname:py})
            xtitle=''
            for i in range(len(cname)):
                xtitle=xtitle+cname[i]+' = '+str(cvalue.values.tolist()[i])
                mx[cname[i]]=np.ones(npts**2)*float(cvalue[i])
            mx=mx[Lcx]
            pz=np.diag(np.dot(np.dot(mx,REG.dism),mx.T))
            px=np.array(px)
            py=np.array(py)
            pz=np.array(pz)
            z=plt.mlab.griddata(px,py,pz,x,y,interp='linear')
            plt.contour(x,y,z,15,linewidths=0.5, colors='k')
            plt.contourf(x,y,z,15,cmap=plt.cm.rainbow)
            plt.colorbar()
            ax.set_xlabel(xname)
            ax.set_ylabel(yname)
            ax.set_title(xtitle)
            ax.set_xlim([px.min(),px.max()])
            ax.set_ylim([py.min(),py.max()])
        elif self.surfaceradioButton.isChecked():             
            Ftable=surtabDlg.launch(None)
            if len(np.shape(Ftable))==0: return()
            if np.argmax(Ftable['X axis'].values)==np.argmax(Ftable['Y axis'].values):
                QtWidgets.QMessageBox.critical(self,'Error',"Two variables on the same axis",QtWidgets.QMessageBox.Ok)
                return()
            fig=plt.figure()
            ax=fig.add_subplot(111)
            npts=100
            xname=Ftable[(Ftable['X axis']==True).values].index[0]
            yname=Ftable[(Ftable['Y axis']==True).values].index[0]
            cname=Ftable[(Ftable['Constant']==True).values].index.tolist()
            cvalue=Ftable.loc[(Ftable['Constant']==True).values,'value']
            x=np.linspace(float(Ftable['min'][xname]),float(Ftable['max'][xname]),npts)
            y=np.linspace(float(Ftable['min'][yname]),float(Ftable['max'][yname]),npts)
            px=[]
            py=[]
            for i in range(npts):
                for j in range(npts):
                    px.append(x[i])
                    py.append(y[j])
            mx=pd.DataFrame({xname:px,yname:py})
            xtitle=''
            for i in range(len(cname)):
                xtitle=xtitle+cname[i]+' = '+str(cvalue.values.tolist()[i])
                mx[cname[i]]=np.ones(npts**2)*float(cvalue[i])
            mx=mx[Lcx]
            pz=REG.lr.predict(mx)
            px=np.array(px)
            py=np.array(py)
            pz=np.array(pz)
            z=plt.mlab.griddata(px,py,pz,x,y,interp='linear')
            plt.contour(x,y,z,15,linewidths=0.5, colors='k')
            plt.contourf(x,y,z,15,cmap=plt.cm.rainbow)
            plt.colorbar()
            ax.set_xlabel(xname)
            ax.set_ylabel(yname)
            ax.set_title(xtitle)
            ax.set_xlim([px.min(),px.max()])
            ax.set_ylim([py.min(),py.max()])
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
        try:
            self.rmmpl()
        except:
            pass
        self.addmpl(fig)        
    def reset(self):
        self.TcheckBox.setChecked(True)
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
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
class surtabDlg(QtWidgets.QDialog,Ui_surtab):
    def __init__(self,parent=None):
        super(surtabDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        Lc=DS.Lc[DS.Ic]
        Lcx=Lc[-DS.Gc[DS.Ic]]
        nx=len(Lcx)
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        self.FtableWidget.setRowCount(nx)
        self.FtableWidget.setColumnCount(6)
        self.Ftable=pd.DataFrame(np.zeros((nx,3),dtype='bool'),columns=['X axis','Y axis','Constant'],index=Lcx.tolist())
        self.Ftable['max']=data[Lcx].max()
        self.Ftable['min']=data[Lcx].min()
        self.Ftable['value']=np.zeros(nx)
        self.Ftable.loc[Lcx[0],'X axis']=True
        self.Ftable.loc[Lcx[1],'Y axis']=True
        for i in range(2,nx):
            self.Ftable.loc[Lcx[i],'Constant']=True            
        for r in range(0,nx):
            for c in range(0,6):
                item = QtWidgets.QTableWidgetItem()
                item.setText(str(self.Ftable.ix[r,c]))
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable)
                self.FtableWidget.setItem(r,c,item)
        self.FtableWidget.setHorizontalHeaderLabels([str(x) for x in self.Ftable.columns.tolist()])
        self.FtableWidget.setVerticalHeaderLabels([str(x) for x in self.Ftable.index.tolist()])
        self.accepted.connect(self.close_ok)
        self.FtableWidget.doubleClicked.connect(self.double_click)
    def getValues(self):
        return (self.Ftable)
    @staticmethod
    def launch(parent):
        dlg=QtWidgets.QDialog()
        dlg = surtabDlg(parent)
        r = dlg.exec_()
        if r:
            return dlg.getValues()
        return None
    def double_click(self):
        if self.FtableWidget.currentItem().text()=='True' or self.FtableWidget.currentItem().text()=='False':
            if self.FtableWidget.currentItem().column()<=1:
                for r in range(self.FtableWidget.rowCount()):
                    self.FtableWidget.item(r,self.FtableWidget.currentItem().column()).setText('False')
                    self.Ftable.ix[r,self.FtableWidget.currentItem().column()]=False
                self.Ftable.ix[self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()]=True
                self.FtableWidget.item(self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()).setText('True')
            if self.FtableWidget.currentItem().column()==2:
                if self.FtableWidget.currentItem().text()=='True':
                    self.Ftable.ix[self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()]=False
                    self.FtableWidget.item(self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()).setText('False')                    
                elif self.FtableWidget.currentItem().text()=='False':
                    self.Ftable.ix[self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()]=True
                    self.FtableWidget.item(self.FtableWidget.currentItem().row(),self.FtableWidget.currentItem().column()).setText('True')                    
        else:
            pass
    def close_ok(self):
        for r in range(self.FtableWidget.rowCount()):
            for c in range(self.FtableWidget.columnCount()):
                item=self.FtableWidget.item(r,c)
                try:
                    if c<=2:
                        self.Ftable.ix[r,c]=bool(strtobool(item.text()))
                    else:
                        self.Ftable.ix[r,c]=float(item.text())
                except:
                    QtWidgets.QMessageBox.critical(self,'Error',"Wrong data type",QtWidgets.QMessageBox.Ok)
                    return()

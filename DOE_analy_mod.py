from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from distutils.util import strtobool
from config import DOE,DS
import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import LeaveOneOut
from statsmodels.formula.api import OLS
from patsy import ModelDesc,Term,LookupFactor,EvalFactor,dmatrices,INTERCEPT
from matplotlib.lines import Line2D
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_doeanaly,QDialog=loadUiType('doeanaly.ui')
Ui_surtab,QDialog=loadUiType('surtab.ui')
class doeanalyDlg(QtWidgets.QDialog,Ui_doeanaly):
    def __init__(self,parent=None):
        super(doeanalyDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Lcy=Lc[Gc]
        Lcx=Lc[-Gc]
        self.YcomboBox.addItems(Lcy)
        self.interactionlistWidget.addItem('Intercept')
        for term in DOE.lfac:
            item=''
            for i in range(len(term)):
                if i>0: item=item+':'
                item=item+Lcx[term[i]-1]
            self.interactionlistWidget.addItem(item)
        for term in Lcx:
            item=term+':'+term
            self.interactionlistWidget.addItem(item)
        self.interactionlistWidget.doubleClicked.connect(self.additem_1)
        self.selectedlistWidget.doubleClicked.connect(self.additem_2)
        self.ApplyButton.clicked.connect(self.redraw)
        self.ResetButton.clicked.connect(self.reset)
        self.VcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(True)
        self.YGcheckBox.setChecked(True)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        fig=Figure()
        ax=fig.add_subplot(111)
        ax.plot(np.array(0))
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.addmpl(fig)
    def additem_1(self):
        nrow=self.interactionlistWidget.currentRow()
        item_str=self.interactionlistWidget.item(nrow).text()
        self.interactionlistWidget.takeItem(nrow)
        self.selectedlistWidget.addItem(item_str)
    def additem_2(self):
        nrow=self.selectedlistWidget.currentRow()
        item_str=self.selectedlistWidget.item(nrow).text()
        self.interactionlistWidget.addItem(item_str)
        self.selectedlistWidget.takeItem(nrow)
    def redraw(self):
        variables=[]
        if self.includeallcheckBox.isChecked():
            for i in range(self.interactionlistWidget.count()):
                variables.append(self.interactionlistWidget.item(i).text())
        else:
            for i in range(self.selectedlistWidget.count()):
                variables.append(self.selectedlistWidget.item(i).text())
        nX=len(variables)
        if nX<1:
            QtWidgets.QMessageBox.critical(self,'Error',"Too few variables selected!",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        Yname=self.YcomboBox.currentText()
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        Lcy=Lc[Gc]
        Lcx=Lc[-Gc]
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        Y=data[Lcy]
        X=data[Lcx]             
        if nX>X.shape[0]:
            QtWidgets.QMessageBox.critical(self,'Error',"Factors > Observation! \n Reduce factors.",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        ny=self.YcomboBox.currentIndex()
        Y=Y.values.astype('float')
        X=X.values.astype('float')
        Y=Y[:,ny]
        nr=len(Y)
        basey=[Term([LookupFactor(Yname)])]
        basex=[]
        for term in variables:
            if term=='Intercept':
                basex=[INTERCEPT]
                variables.remove(term)
        for term in variables:
            vterm=term.split(':')
            term_lookup=[LookupFactor(x) for x in vterm]
            if len(term_lookup)>1:
                if vterm[0]==vterm[1]:
                    term_lookup=[EvalFactor(vterm[0]+' ** 2')]
            basex.append(Term(term_lookup))
        desc=ModelDesc(basey,basex)
        data=np.column_stack((X,Y))
        columns=Lcx.tolist()
        columns.append(Yname)
        data=pd.DataFrame(data,columns=columns)
        y,mx=dmatrices(desc,data,return_type='dataframe')
        dism=np.linalg.inv(np.dot(mx.T.values,mx.values))
        mod=OLS(y,mx)
        DOE.res=mod.fit()
        # calculation of cross-validation        
        ypcv=list()
        rcv=list()
        bres=list()
        loo=LeaveOneOut()
        loo.get_n_splits(mx)
        for train_index, test_index in loo.split(mx):
            mx_train=mx.ix[train_index,:]
            mx_test=mx.ix[test_index,:]
            y_train=y.ix[train_index,:]
            y_test=y.ix[test_index,:]
            modcv=OLS(y_train,mx_train)
            rescv=modcv.fit()
            ypcv.append(rescv.predict(mx_test).values[0])
            rcv.append(rescv.predict(mx_test).values[0]-y_test.values[0])
            bres.append((rescv.params-DOE.res.params).values**2)
        bres=pd.DataFrame(bres)
        bres=bres.sum()*nr/(nr-1)
        bres=np.sqrt(bres.values)
        tres=np.abs(DOE.res.params.values/bres)
        pt=2*t.pdf(tres,nr)
        fig=Figure()
        ax=fig.add_subplot(111)       
        if self.coefradioButton.isChecked():
            if DOE.res.params.index[0]=='Intercept':
                ind=np.arange(1,len(DOE.res.params))
                vcol=[]
                for i in ind:
                    if(DOE.res.pvalues[i]<0.05):vcol.append('red')
                    else:vcol.append('blue')
                ax.bar(ind,DOE.res.params[1:],align='center',color=vcol)
                ax.set_title('Coefficient Value : Intercept {:10.4f}-{:10.4f}-{:10.4f}'.\
                format(DOE.res.conf_int().ix[0,0],DOE.res.params[0],DOE.res.conf_int().ix[0,1]))
                ax.set_xticklabels(DOE.res.params.index[1:], rotation='vertical')
                cmin=DOE.res.params[1:]-DOE.res.conf_int().ix[1:,0]
                cmax=DOE.res.conf_int().ix[1:,1]-DOE.res.params[1:]
                ax.errorbar(ind,DOE.res.params[1:],yerr=[cmin.values,cmax.values],fmt='o',ecolor='green')
            else:
                ind=np.arange(1,len(DOE.res.params)+1)
                ax.bar(ind,DOE.res.params,align='center')
                ax.set_title('Coefficient Value : None Intercept')
                ax.set_xticklabels(DOE.res.params.index[0:], rotation='vertical')
                cmin=DOE.res.conf_int().ix[0:,0]-DOE.res.params[0:]
                cmax=DOE.res.conf_int().ix[0:,1]-DOE.res.params[0:]
                ax.errorbar(ind,DOE.res.params[0:],yerr=[cmin.values,cmax.values],fmt='o',ecolor='green')
            ax.set_xticks(ind)
            ax.set_xlabel('Coefficient Number (except Intercept)') 
            ax.annotate('red bar: significance 5%',xy=(0.75,0.95),xycoords='figure fraction',fontsize=8)
        elif self.coefpredradioButton.isChecked():
            if DOE.res.params.index[0]=='Intercept':
                ind=np.arange(1,len(DOE.res.params))
                vcol=[]
                for i in ind:
                    if(pt[i]<0.05):vcol.append('red')
                    else:vcol.append('blue')
                ax.bar(ind,DOE.res.params[1:],align='center',color=vcol)
                ax.set_title('Coefficient Value : Intercept {:10.4f}-{:10.4f}-{:10.4f}'.format
                             (DOE.res.params[0]-tres[0]*bres[0]/np.sqrt(nr),DOE.res.params[0],DOE.res.params[0]+tres[0]*bres[0]/np.sqrt(nr)))
                ax.set_xticklabels(DOE.res.params.index[1:], rotation='vertical')
                ax.errorbar(ind,DOE.res.params[1:],yerr=tres[1:]*bres[1:]/np.sqrt(nr),fmt='o',ecolor='green')
            else:
                ind=np.arange(1,len(DOE.res.params)+1)
                ax.bar(ind,DOE.res.params,align='center')
                ax.set_title('Coefficient Value : None Intercept')
                ax.set_xticklabels(DOE.res.params.index[0:], rotation='vertical')
                ax.errorbar(ind,DOE.res.params[0:],yerr=tres[0:]*bres[0:]/np.sqrt(nr),fmt='o',ecolor='green')
            ax.set_xticks(ind)
            ax.set_xlabel('Coefficient Number (except Intercept)') 
            ax.annotate('red bar: significance 5%',xy=(0.75,0.95),xycoords='figure fraction',fontsize=8)
        elif self.fitradioButton.isChecked():
            yf=DOE.res.fittedvalues.tolist()
            resid=DOE.res.resid.tolist()
            ax.scatter(y,yf,color='red',alpha=0.3,marker='o')
            ax.set_ylabel('Fitted Values',color='red') 
            ax.tick_params('y',colors='red')
            ax1=ax.twinx()
            ax1.scatter(y,resid,color='blue',alpha=0.3,marker='o')
            ax1.set_ylabel('Residuals',color='blue') 
            ax1.tick_params('y',colors='blue')
            xmin,xmax=ax.get_xlim()
            ax.set_ylim([xmin,xmax])
            df=DOE.res.df_resid
            vares=np.sum(DOE.res.resid**2)/df
            rmsef=np.sqrt(vares)
            vary=np.var(y.values)
            evar=(1-vares/vary)*100
            ax.set_title('df {:3.0f};   RMSEF {:6.2f};   Exp.Var.{:5.1f}%'.format(df,rmsef,evar))
            ax.add_line(Line2D([xmin,xmax],[xmin,xmax],color='red')) 
            ax1.add_line(Line2D([xmin,xmax],[0,0],color='blue')) 
            ax.set_xlabel('Measured Values') 
            if self.VcheckBox.isChecked():
                Lr=DOE.res.model.data.row_labels
                for i,txt in enumerate(Lr):
                    ax.annotate(str(txt),(y.ix[i],yf[i]))
        elif self.predradioButton.isChecked():
            ax.scatter(y,ypcv,color='red',alpha=0.3,marker='o')
            ax.set_ylabel('CV Predicted Values',color='red') 
            ax.tick_params('y',colors='red')
            ax1=ax.twinx()
            ax1.scatter(y,rcv,color='blue',alpha=0.3,marker='o')
            ax1.set_ylabel('CV Residuals', color='blue')
            ax1.tick_params('y',colors='blue')
            xmin,xmax=ax.get_xlim()
            ax.set_ylim([xmin,xmax])
            ax.set_xlabel('Measured Values')
            df=DS.Raw.shape[0]
            varcv=np.sum(np.array(rcv)**2)/df
            rmsecv=np.sqrt(varcv)
            vary=np.var(y.values)
            evar=(1-varcv/vary)*100
            ax.set_title('df {:3.0f};   RMSECV {:6.2f};   Exp.Var.{:5.1f}%'.format(df,rmsecv,evar))
            ax.add_line(Line2D([xmin,xmax],[xmin,xmax],color='red')) 
            ax1.add_line(Line2D([xmin,xmax],[0,0],color='blue')) 
            if self.VcheckBox.isChecked():
                Lr=DOE.res.model.data.row_labels
                for i,txt in enumerate(Lr):
                    ax.annotate(str(txt),(y.ix[i],ypcv[i]))
        elif self.levradioButton.isChecked():           
            Ftable=surtabDlg.launch(None)
            if len(np.shape(Ftable))==0: return()
            if np.argmax(Ftable['X axis'].values)==np.argmax(Ftable['Y axis'].values):
                QtWidgets.QMessageBox.critical(self,'Error',"Two variables on the same axis",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            fig=plt.figure()
            ax=fig.add_subplot(111)
            npts=20
            xname=Ftable[(Ftable['X axis']==True).values].index[0]
            yname=Ftable[(Ftable['Y axis']==True).values].index[0]
            cname=Ftable[(Ftable['Constant']==True).values].index.tolist()
            cvalue=Ftable.loc[(Ftable['Constant']==True).values,'value']
            zname=Yname
            x=np.linspace(float(Ftable['min'][xname]),float(Ftable['max'][xname]),npts)
            y=np.linspace(float(Ftable['min'][yname]),float(Ftable['max'][yname]),npts)
            px=[]
            py=[]
            for i in range(npts):
                for j in range(npts):
                    px.append(x[i])
                    py.append(y[j])
            data=pd.DataFrame({xname:px,yname:py,zname:px})
            xtitle=''
            for i in range(len(cname)):
                xtitle=xtitle+cname[i]+' = '+str(cvalue.values.tolist()[i])
                data[cname[i]]=np.ones(npts**2)*float(cvalue[i])
            my,mx=dmatrices(desc,data,return_type='dataframe')
            pz=np.diag(np.dot(np.dot(mx,dism),mx.T))
            px=np.array(px)
            py=np.array(py)
            pz=np.array(pz)
            z=plt.mlab.griddata(px,py,pz,x,y,interp='linear')
            plt.contour(x,y,z,15,linewidths=0.5,colors='k')
            plt.contourf(x,y,z,15,cmap=plt.cm.rainbow)
            plt.colorbar()
            ax.set_xlabel(xname)
            ax.set_ylabel(yname)
            ax.set_title(xtitle)
            ax.set_xlim([px.min(),px.max()])
            ax.set_ylim([py.min(),py.max()])
        elif self.surradioButton.isChecked():
            Ftable=surtabDlg.launch(None)
            if len(np.shape(Ftable))==0: return()
            if np.argmax(Ftable['X axis'].values)==np.argmax(Ftable['Y axis'].values):
                QtWidgets.QMessageBox.critical(self,'Error',"Two variables on the same axis",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            fig=plt.figure()
            ax=fig.add_subplot(111)
            npts=100
            xname=Ftable[(Ftable['X axis']==True).values].index[0]
            yname=Ftable[(Ftable['Y axis']==True).values].index[0]
            cname=Ftable[(Ftable['Constant']==True).values].index.tolist()
            cvalue=Ftable.loc[(Ftable['Constant']==True).values,'value']
            zname=Yname
            x=np.linspace(float(Ftable['min'][xname]),float(Ftable['max'][xname]),npts)
            y=np.linspace(float(Ftable['min'][yname]),float(Ftable['max'][yname]),npts)
            px=[]
            py=[]
            for i in range(npts):
                for j in range(npts):
                    px.append(x[i])
                    py.append(y[j])
            data=pd.DataFrame({xname:px,yname:py,zname:px})
            xtitle=''
            for i in range(len(cname)):
                xtitle=xtitle+cname[i]+' = '+str(cvalue.values.tolist()[i])
                data[cname[i]]=np.ones(npts**2)*float(cvalue[i])
            my,mx=dmatrices(desc,data,return_type='dataframe')
            pz=DOE.res.predict(mx)
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
        elif self.dismradioButton.isChecked():
            fig=plt.figure()
            ax=fig.add_subplot(111)
            cax=ax.matshow(dism)
            fig.colorbar(cax)
            ax.set_title('Trace = {:10.4f}'.format(np.trace(dism)))
        elif self.inflradioButton.isChecked():
            mxc=preprocessing.scale(mx.values,with_mean=True,with_std=False)
            mxc2=mxc**2
            infl=np.sum(mxc2,axis=0)*np.diag(dism)
            fig=plt.figure()
            ax=fig.add_subplot(111)
            cax=ax.matshow(infl.reshape(1,-1),cmap='gray_r')
            fig.colorbar(cax)
            ax.yaxis.grid(False)
            ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
            ax.set_xlabel('Inlaction Factor')
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
        self.VcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(True)
        self.YGcheckBox.setChecked(True)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        Lc=DS.getLc()
        Lcx=Lc[-DS.getGc()]
        lfac=DOE.getlfac()
        self.interactionlistWidget.addItem('Intercept')
        for term in lfac:
            item=''
            for i in range(len(term)):
                if i>0: item=item+':'
                item=item+Lcx[term[i]-1]
            self.interactionlistWidget.addItem(item)
        self.selectedlistWidget.clear()
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
        Gc=DS.Gc[DS.Ic]
        Lcx=Lc[-Gc]
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
               

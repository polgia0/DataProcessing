from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import xlwings as xw
import numpy as np
from random import sample
from math import floor
import matplotlib.pyplot as plt
import scipy.stats as stats
Ui_averagediff,QDialog=loadUiType('averagediff.ui')
class averagediffDlg(QtWidgets.QDialog,Ui_averagediff):
    def __init__(self,parent=None):
        super(averagediffDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(1)
        self.buttonBox.accepted.connect(self.averagediff)
    def averagediff(self):
        data=DS.Raw.loc[DS.Ir,DS.Ic]
        data=data[[self.XcomboBox.currentText(),self.YcomboBox.currentText()]]
        var=np.array(['A','B'])
        var=var.T
        vc=data.count(axis=0)
        nu=vc.sum(axis=0)
        nu=nu-2
        vc=np.array(vc)
        vc=vc.T
        vm=data.mean(axis=0,skipna=True)
        vm=np.array(vm)
        vm=vm.T
        vsum=data.sum(axis=0,skipna=True)
        vsum=np.array(vsum)
        vsum=vsum.T
        difference=vm[1]-vm[0]
        if not self.randomcheckBox.isChecked(): # standard t-Student test on average
            Pvar=data.var(axis=0,skipna=True)
            Pvar=Pvar*(vc-1)
            Pvar=Pvar.sum(axis=0)
            Pvar=Pvar/nu
            Vdiff=Pvar*(1/vc[1]+1/vc[0])
            Serr=np.sqrt(Vdiff)
            tt=abs(difference)/Serr
            p0=stats.t.pdf(tt,nu)
            t1=stats.t.ppf(0.95,nu)
            t2=stats.t.ppf(0.99,nu)
            if(tt>=t1):
                res="Two average are different"
            else:
                res="Two averages are equal"
            self.appExcel=xw.App()
            wb=xw.books.active
            sht=wb.sheets[0]
            sht.range('A1').value='Variable'
            sht.range('B1').value=var
            sht.range('A2').value='Number'
            sht.range('B2').value=vc
            sht.range('A3').value='Sum'
            sht.range('B3').value=vsum
            sht.range('A4').value='Dof'
            sht.range('B4').value=np.array(nu)
            sht.range('A5').value='Difference'
            sht.range('B5').value=difference
            sht.range('A6').value='Average'
            sht.range('B6').value=vm
            sht.range('A7').value='Pooled var.'
            sht.range('B7').value=Pvar
            sht.range('A7').value='Difference Variance'
            sht.range('B7').value=Vdiff
            sht.range('A8').value='Standard Error'
            sht.range('B8').value=Serr
            sht.range('A9').value='t-Student'
            sht.range('B9').value=tt
            sht.range('A10').value='p-Student x100'
            sht.range('B10').value=p0*100
            sht.range('A11').value='t.lim(5%)'
            sht.range('B11').value=t1
            sht.range('A12').value='t.lim(1%)'
            sht.range('B12').value=t2
            sht.range('A13').value=res
        else: # randomizations
            val=np.array(data)
            val=val.flatten()
            nval=vc[1]+vc[0]
            npoints=int(self.spinBox.value())
            x=np.zeros(npoints)
            for i in range(npoints):
                ia=sample(range(nval),vc[0])
                ya=val[ia]
                yb=np.delete(val,ia)
                x[i]=yb.mean()-ya.mean()
            iqr=np.percentile(x, [75, 25])
            iqr=iqr[0]-iqr[1]
            n=x.size
            dx=abs(np.amax(x)-np.amin(x))
            nbins=floor(dx/(2*iqr)*n**(1/3))+1
            bins=np.linspace(np.amin(x),np.amax(x),nbins)
            fig=plt.figure()
            ax=fig.add_subplot(111)
            ax.hist(x,bins=bins,normed=1,histtype='bar',color='b',alpha=0.5,orientation='vertical',label="X")
            ax.axvline(x=difference,linewidth=2, color='red')
            yc,xc=np.histogram(x,bins=bins,normed= True)
            tot=0
            tota=0
            for i in range(len(xc)-1):
                tot=tot+yc[i]
                if(difference<=xc[i]):
                    tota=tota+yc[i]
            pa=tota/tot*100
            ax.set_title('Randomized Histogram : P(x>d)= '+str(round(pa,2))+'%)')
            fig.show()

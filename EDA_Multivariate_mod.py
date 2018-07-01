from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import itertools
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_multivariateplot,QDialog=loadUiType('multivariate.ui')
class multivariateplotDlg(QtWidgets.QDialog,Ui_multivariateplot):
    def __init__(self,parent=None):
        super(multivariateplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.variablelistWidget.addItems(DS.Lc[DS.Ic])
        self.variablelistWidget.doubleClicked.connect(self.additem_1)
        self.selectedlistWidget.doubleClicked.connect(self.additem_2)
        self.vradioButton.clicked.connect(self.allv)
        self.ApplyButton.clicked.connect(self.redraw)
        self.ResetButton.clicked.connect(self.reset)
        fig=Figure()
        ax=fig.add_subplot(111)
        ax.plot(np.array(0))
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        self.addmpl(fig)
    def allv(self):
        for i in range(self.variablelistWidget.count()):
            self.selectedlistWidget.addItem(self.variablelistWidget.item(i).text())
        self.variablelistWidget.clear()
    def additem_1(self):
        nrow=self.variablelistWidget.currentRow()
        item_str=self.variablelistWidget.item(nrow).text()
        if(self.scattermatrixradioButton.isChecked()):
            maxlim=6
            if(self.selectedlistWidget.count()>maxlim):
                QtWidgets.QMessageBox.critical(self,'Error',"Too many variables!",QtWidgets.QMessageBox.Ok)
                return()
        self.variablelistWidget.takeItem(nrow)
        self.selectedlistWidget.addItem(item_str)
    def additem_2(self):
        nrow=self.selectedlistWidget.currentRow()
        item_str=self.selectedlistWidget.item(nrow).text()
        self.variablelistWidget.addItem(item_str)
        self.selectedlistWidget.takeItem(nrow)
    def redraw(self):
        nv=self.selectedlistWidget.count()
        variables=[]
        for i in range(nv):
            variables.append(self.selectedlistWidget.item(i).text())
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data[variables+['Lr','Cr']]
        Nnan=data.isnull().isnull().all().all()
        data=data.dropna()
        Lr=data['Lr'].values
        Cr=data['Cr'].values
        data=data.drop('Lr',axis=1)
        data=data.drop('Cr',axis=1)
        if data.dtypes.all()=='float' and data.dtypes.all()=='int':
            QtWidgets.QMessageBox.critical(self,'Error',"Some values are not numbers!",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        fig=Figure()
        nr,nc=data.shape
        Cc=DS.Cc[DS.Ic]
        Cc=Cc[np.in1d(DS.Lc[DS.Ic],variables)]
        if self.starradioButton.isChecked():
            if(self.selectedlistWidget.count()<3):
                QtWidgets.QMessageBox.critical(self,'Error',"Too few variables!",\
                                               QtWidgets.QMessageBox.Ok)
                return()
            mn=data.min()
            mn[mn==0]=0.001
            mx=data.max()
            mx[mx==0]=0.001
            ranges=list()
            for i in range(len(mn)):
                ranges.append([mn[i],mx[i]])
            radar=ComplexRadar(fig, variables, ranges)
            for i in range(nr):
                y=data.iloc[i,:]
                y[y==0]=0.001
                y=y.tolist()
                radar.plot(y)      
        elif self.scattermatrixradioButton.isChecked():
            fig=scatterplot_matrix(data.T.values,variables,linestyle='none',
                                   marker='o',color='black', mfc='none')
            fig.suptitle('Simple Scatterplot Matrix')
        elif self.magnituderadioButton.isChecked():
            ax=fig.add_subplot(111)
            ax.plot(data.values.min(axis=0),'o',color='red',label='min')
            ax.plot(data.values.max(axis=0),'o',color='green',label='max')
            ax.legend(loc=4)
            for i in range(nv):
                ax.vlines(i,data.values.min(axis=0)[i],
                        data.values.max(axis=0)[i],linestyles='solid',
                        color=Cc[i])
            #ax.tick_params(axis='x',which='both',bottom='off',top='off',labelbottom='off')
            ax.set_xticklabels(['']+variables+[''])
            ax.set_xlabel('Feature Index')
            ax.set_ylabel('Feature Magnitude')
            ax.set_yscale("log")
            ax.set_xlim([-1,nv])
            ax.xaxis.grid(True)
            ax.yaxis.grid(True)
        elif self.corrradioButton.isChecked():
            fig=plt.figure()
            ax = fig.add_subplot(111)
            cax=ax.matshow(np.corrcoef(data))
            fig.colorbar(cax)
            ax.set_title('Correlation Matrix')
        elif self.covradioButton.isChecked():
            fig=plt.figure()
            ax = fig.add_subplot(111)
            cax=ax.matshow(np.cov(data))
            fig.colorbar(cax)
            ax.set_title('Covariance Matrix')
        elif self.trendradioButton.isChecked():
            ax=fig.add_subplot(111)
            ncol=nc
            nrow=nr
            Lrow=Lr
            color_point=Cr
            color_line=Cc
            if self.rowcheckBox.isChecked():
                ncol=nr
                nrow=nc
                Lrow=np.array(variables)
                color_point=Cc
                color_line=Cr
                data=data.T
            ind=np.array(range(1,nrow+1))
            for i in range(ncol):
                if self.PcheckBox.isChecked():
                    ax.scatter(ind,data.iloc[:,i],marker='o',color=color_point)
                if self.LcheckBox.isChecked():
                    ax.plot(ind,data.iloc[:,i],color=color_line[i])
                if(nrow>30):
                    itick=np.linspace(0,nrow-1,20).astype(int)
                    ltick=Lrow[itick]
                else:
                    itick=ind
                    ltick=Lrow
                ax.set_xticks(itick)
                ax.set_xticklabels(ltick, rotation='vertical')
                ax.set_xlabel('Object')
        if Nnan:
            ax.annotate('{:04.2f} NaN'.format(Nnan),xy=(0.80,0.95),xycoords='figure fraction')
        self.rmmpl()
        self.addmpl(fig)        
    def reset(self):
        self.variablelistWidget.addItems(DS.getLc().tolist())
        self.selectedlistWidget.clear()
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
# freely adapted from:
# http://datascience.stackexchange.com/questions/6084/how-do-i-create-a-complex-radar-chart
def _scale_data(data, ranges):
    def _invert(x, limits):
        """inverts a value x on a scale from
        limits[0] to limits[1]"""
        return limits[1] - (x - limits[0])
    """scales data[1:] to ranges[0],
    inverts if the scale is reversed"""
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        assert (y1 <= d <= y2) or (y2 <= d <= y1)
    x1, x2 = ranges[0]
    d = data[0]
    if x1 > x2:
        d =_invert(d, (x1, x2))
        x1, x2 = x2, x1
    sdata = [d]
    for d, (y1, y2) in zip(data[1:], ranges[1:]):
        if y1 > y2:
            d = _invert(d, (y1, y2))
            y1, y2 = y2, y1
        sdata.append((d-y1) / (y2-y1) 
                     * (x2 - x1) + x1)
    return sdata
class ComplexRadar():
    def __init__(self, fig, variables, ranges,
                 n_ordinate_levels=6):
        angles=np.arange(0, 360, 360./len(variables))

        axes=[fig.add_axes([0.1,0.1,0.80,0.80],polar=True,
                label = "axes{}".format(i)) 
                for i in range(len(variables))]
        l, text=axes[0].set_thetagrids(angles, 
                                         labels=variables)
        [txt.set_rotation(angle-90) for txt, angle 
             in zip(text, angles)]
        for ax in axes[1:]:
            ax.patch.set_visible(False)
            ax.grid("off")
            ax.xaxis.set_visible(False)
        for i, ax in enumerate(axes):
            grid=np.linspace(*ranges[i], 
                               num=n_ordinate_levels)
            gridlabel=["{}".format(round(x,1)) 
                         for x in grid]
            if ranges[i][0] > ranges[i][1]:
                grid=grid[::-1] 
            gridlabel[0]= ""
            ax.set_rgrids(grid,labels=gridlabel,
                         angle=angles[i])
            ax.set_ylim(*ranges[i])
        self.angle=np.deg2rad(np.r_[angles,angles[0]])
        self.ranges=ranges
        self.ax=axes[0]
    def plot(self,data,*args,**kw):
        sdata=_scale_data(data,self.ranges)
        self.ax.plot(self.angle,np.r_[sdata,sdata[0]],*args,**kw)
    def fill(self,data,*args,**kw):
        sdata=_scale_data(data,self.ranges)
        self.ax.fill(self.angle,np.r_[sdata, sdata[0]],*args,**kw)
def scatterplot_matrix(data, names, **kwargs):
    """Plots a scatterplot matrix of subplots.  Each row of "data" is plotted
    against other rows, resulting in a nrows by nrows grid of subplots with the
    diagonal subplots labeled with "names".  Additional keyword arguments are
    passed on to matplotlib's "plot" command. Returns the matplotlib figure
    object containg the subplot grid."""
    numvars, numdata = data.shape
    fig, axes = plt.subplots(nrows=numvars, ncols=numvars, figsize=(8,8))
    fig.subplots_adjust(hspace=0.05, wspace=0.05)
    for ax in axes.flat:
        # Hide all ticks and labels
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)
        # Set up ticks only on one side for the "edge" subplots...
        if ax.is_first_col():
            ax.yaxis.set_ticks_position('left')
        if ax.is_last_col():
            ax.yaxis.set_ticks_position('right')
        if ax.is_first_row():
            ax.xaxis.set_ticks_position('top')
        if ax.is_last_row():
            ax.xaxis.set_ticks_position('bottom')
    # Plot the data.
    for i, j in zip(*np.triu_indices_from(axes, k=1)):
        for x, y in [(i,j), (j,i)]:
            axes[x,y].plot(data[x], data[y], **kwargs)
    # Label the diagonal subplots...
    for i, label in enumerate(names):
        y=data[i,:]
        iqr=np.percentile(y, [75, 25])
        iqr=iqr[0]-iqr[1]
        n=y.shape[0]
        dy=abs(np.amax(y)-np.amin(y))
        nbins=np.floor(dy/(2*iqr)*n**(1/3))+1
        nbins=10*nbins
        bins=np.linspace(np.amin(y),np.amax(y),nbins)
        axes[i,i].hist(y,bins=bins,histtype='bar',color='green',alpha=0.5,orientation='vertical',label="X")
        axes[i,i].annotate(label, (0.5, 0.5), xycoords='axes fraction',
                ha='center', va='center')
    # Turn on the proper x or y axes ticks.
    for i, j in zip(range(numvars), itertools.cycle((-1, 0))):
        axes[j,i].xaxis.set_visible(True)
        axes[i,j].yaxis.set_visible(True)
    return fig

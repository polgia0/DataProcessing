from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUiType
from config import DS
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.proj3d import proj_transform
from matplotlib.text import Annotation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
Ui_trivariateplot,QDialog=loadUiType('trivariateplot.ui')
class trivariateplotDlg(QtWidgets.QDialog,Ui_trivariateplot):
    def __init__(self,parent=None):
        super(trivariateplotDlg,self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |
            QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowCloseButtonHint |
            QtCore.Qt.WindowMaximizeButtonHint)
        self.XcomboBox.addItems(DS.Lc[DS.Ic])
        self.YcomboBox.addItems(DS.Lc[DS.Ic])
        self.ZcomboBox.addItems(DS.Lc[DS.Ic])
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
    def reset(self):
        self.XcomboBox.setCurrentIndex(0)
        self.YcomboBox.setCurrentIndex(0)
        self.ZcomboBox.setCurrentIndex(0)
        self.XlineEdit.setText('')
        self.YlineEdit.setText('')
        self.ZlineEdit.setText('')
        self.TlineEdit.setText('')
        self.VcheckBox.setChecked(False)
        self.XGcheckBox.setChecked(False)
        self.YGcheckBox.setChecked(False)
        self.XMcheckBox.setChecked(True)
        self.YMcheckBox.setChecked(True)
        self.XcheckBox.setChecked(True)
        self.YcheckBox.setChecked(True)
        self.update()                
    def redraw(self):
        def annotate3D(ax, s, *args, **kwargs):
            '''add anotation text s to to Axes3d ax'''
            tag = Annotation3D(s, *args, **kwargs)
            ax.add_artist(tag)
        if self.XcomboBox.currentText()==self.YcomboBox.currentText() or \
           self.YcomboBox.currentText()==self.ZcomboBox.currentText() or \
           self.YcomboBox.currentText()==self.ZcomboBox.currentText():
            QtWidgets.QMessageBox.critical(self,'Error',"Variables must be different",\
                                           QtWidgets.QMessageBox.Ok)
            return()
        data=DS.Raw.iloc[DS.Ir,DS.Ic]
        data=data.assign(Lr=DS.Lr[DS.Ir])
        data=data.assign(Cr=DS.Cr[DS.Ir])
        data=data[[self.XcomboBox.currentText(),self.YcomboBox.currentText(), \
                   self.ZcomboBox.currentText(),'Lr','Cr']]
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
        x=data[self.XcomboBox.currentText()].values
        y=data[self.YcomboBox.currentText()].values
        z=data[self.ZcomboBox.currentText()].values
        npts=int(self.spinBox.value())
        color_point='blue'
        if self.CcheckBox.isChecked():
             color_point=Cr
        if self.scatterradioButton.isChecked():
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            ax.scatter(x,y,z,c=color_point,marker='o')
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_zlabel(self.ZcomboBox.currentText())
            ax.view_init(elev=self.elevationspinBox.value(),azim=self.azimutspinBox.value())
            ax.dist=self.distancespinBox.value()
            if self.VcheckBox.isChecked():
                xyzn=zip(x,y,z)
                for j,xyz_ in enumerate(xyzn): 
                    annotate3D(ax, s=Lr[j], xyz=xyz_, fontsize=10, xytext=(-3,3),
                               textcoords='offset points', ha='right',va='bottom')  
        if self.contouradioButton.isChecked():
            fig=plt.figure()
            ax = fig.add_subplot(111)
            xi=np.linspace(x.min(),x.max(),npts)
            yi=np.linspace(y.min(),y.max(),npts)
            zi=plt.mlab.griddata(x, y, z, xi, yi, interp='linear')
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_title(self.ZcomboBox.currentText() +' : griddata test (%d points)' % npts)
            plt.contour(xi,yi,zi,15,linewidths=0.5, colors='k')
            plt.contourf(xi,yi,zi,15,cmap=plt.cm.rainbow)
            plt.colorbar()
            ax.scatter(x,y,marker='o',c=color_point,s=7,zorder=10)
            ax.set_xlim(x.min(),x.max())
            ax.set_ylim(y.min(),y.max())
        if self.surfaceradioButton.isChecked():
            fig = plt.figure()
            ax = fig.gca(projection='3d')
            xi=np.linspace(x.min(),x.max(),npts)
            yi=np.linspace(y.min(),y.max(),npts)
            zi=plt.mlab.griddata(x,y,z,xi,yi,interp='linear')
            xi,yi=np.meshgrid(xi,yi)
            ax.view_init(elev=self.elevationspinBox.value(),azim=self.azimutspinBox.value())
            surf=ax.plot_surface(xi,yi,zi, rstride=10, cstride=10, cmap=cm.rainbow,
                    linewidth=0, antialiased=False)
            surf.set_clim(vmin=zi.min(), vmax=zi.max())
            ax.set_zlim3d(zi.min(),zi.max())
            fig.colorbar(surf,orientation='vertical',shrink=0.5, format='%.2f')
            ax.set_xlabel(self.XcomboBox.currentText())
            ax.set_ylabel(self.YcomboBox.currentText())
            ax.set_zlabel(self.ZcomboBox.currentText())
        if Nnan:
            ax.annotate('{:04.2f} NaN'.format(Nnan),xy=(0.80,0.95),xycoords='figure fraction')
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

class Annotation3D(Annotation):
    '''Annotate the point xyz with text s'''

    def __init__(self, s, xyz, *args, **kwargs):
        Annotation.__init__(self,s, xy=(0,0), *args, **kwargs)
        self._verts3d = xyz        

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.xy=(xs,ys)
        Annotation.draw(self, renderer)

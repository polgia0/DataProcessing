from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from sklearn.neighbors import KNeighborsClassifier
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import DS
Ui_neighbors,QDialog=loadUiType('neighbors.ui')
class neighborsDlg(QtWidgets.QDialog,Ui_neighbors):
    def __init__(self,parent=None):
        super(neighborsDlg,self).__init__(parent)
        self.setupUi(self)
        self.XcomboBox.addItem('None')
        self.YcomboBox.addItem('None')
        self.XcomboBox.addItems(DS.Lc)
        self.YcomboBox.addItems(DS.Lc)
        self.accepted.connect(self.neighbors)
    def neighbors(self):
        nx=self.XcomboBox.currentIndex()
        ny=self.YcomboBox.currentIndex()
        if nx==ny and nx!=0 and ny!=0:
            QtWidgets.QMessageBox.critical(self,'Error','Factors must be different!',QtWidgets.QMessageBox.Ok)
            return()
        if (nx!=0 and ny==0) or (nx==0 and ny!=0):
            QtWidgets.QMessageBox.critical(self,'Error','You must chose both or none factors!',QtWidgets.QMessageBox.Ok)
            return()
        nx=nx-1
        ny=ny-1
        if self.balltreeradioButton.isChecked():
            algo='ball_tree'
        elif self.kdtreeradioButton.isChecked():
            algo='kd_tree'
        elif self.bruteradioButton.isChecked():
            algo='brute'
        else:
            algo='auto'
        if self.mahattanradioButton.isChecked():
            metric='mahattan'
        elif self.chebyshevradioButton.isChecked(): 
            metric='chebyshev'
        elif self.minkowskiradioButton.isChecked(): 
            metric='minkowski'
        else:
            metric='euclidean'
        if (metric=='mahattan')& (algo=='ball_tree')is None:
            QtWidgets.QMessageBox.critical(self,'Error',"Metric inconpatible for Algorithm",QtWidgets.QMessageBox.Ok)
            return()
        Gr=DS.Gr
        X=DS.Raw.loc[DS.Ir,DS.Ic].values
        Lc=DS.Lc
        fig,ax=plt.subplots()
        if(nx<0)&(ny<0): # all data matrix is used
            if not np.isnan(Gr.all()) : # all group are done so  we do a validation if a test set is defined
                if np.all(DS.Ts==False):
                    QtWidgets.QMessageBox.critical(self,'Error',"There is not any Test Set",QtWidgets.QMessageBox.Ok)
                    return()
                Xtrain=X[-DS.Ts,:]
                Xtest=X[DS.Ts,:]
                ytrain=Gr[-DS.Ts]
                ytest=Gr[DS.Ts]
                clf=KNeighborsClassifier(algorithm=algo,leaf_size=30,metric=metric,
                                         metric_params=None,
                                         n_jobs=-1,
                                         n_neighbors=self.knspinBox.value(),
                                         p=self.mpspinBox.value(),
                                         weights='uniform')
                clf.fit(Xtrain,ytrain.tolist())
                yf=clf.predict(Xtest)
                mask=ytest==yf
                ax.matshow(mask.reshape(1,-1),cmap='gray_r')
                fig.suptitle('Test Set Score {:.2f}'.format(clf.score(Xtest,ytest.tolist())))
                ax.tick_params(axis='y',which='both',left='off',right='off',labelleft='off')
                ax.set_xlabel('Sample Index')
            else: # some groups are missing so we do a prediction
                Lr=DS.Lr[pd.isnull(Gr)]
                Xtest=X[pd.isnull(Gr),:]
                Xtrain=X[-pd.isnull(Gr),:]
                ytrain=Gr[-pd.isnull(Gr)]
                clf=KNeighborsClassifier(algorithm=algo,leaf_size=30,metric=metric,
                                         metric_params=None,
                                         n_jobs=-1,
                                         n_neighbors=self.knspinBox.value(),
                                         p=self.mpspinBox.value(),
                                         weights='uniform')
                clf.fit(Xtrain,ytrain.tolist())
                ytest=clf.predict(Xtest)
                ind=range(1,len(ytest)+1)
                ax.scatter(ind,ytest,marker='o')
                ax = plt.gca()
                ax.set_xticks(ind)
                ax.set_xticklabels(map(str,Lr.tolist()),rotation='vertical')
                ax.set_xgrid()
                ax.set_ygrid()
        else:
            X=X[:,(nx,ny)]
            # Create color maps
            cmap_light=ListedColormap(['#FFAAAA','#AAFFAA','#AAAAFF'])
            cmap_bold=ListedColormap(['#FF0000','#00FF00','#0000FF'])
            h=0.02  # step size in the mesh
            # we create an instance of Neighbours Classifier and fit the data.
            clf=KNeighborsClassifier(algorithm=algo,leaf_size=30,metric=metric,
                                     metric_params=None,
                                     n_jobs=-1,
                                     n_neighbors=self.knspinBox.value(),
                                     p=self.mpspinBox.value(),
                                     weights='uniform')
            clf.fit(X,Gr.tolist())
            # Plot the decision boundary. For that, we will assign a color to each
            # point in the mesh [x_min, x_max]x[y_min, y_max].
            x_min,x_max=X[:,0].min()-1,X[:, 0].max()+1
            y_min,y_max=X[:,1].min()-1,X[:, 1].max()+1
            xx,yy=np.meshgrid(np.arange(x_min,x_max,h),np.arange(y_min,y_max, h))
            Z=clf.predict(np.c_[xx.ravel(), yy.ravel()])
            # Put the result into a color plot
            Z=Z.reshape(xx.shape)
            plt.pcolormesh(xx,yy,Z,cmap=cmap_light)
            # Plot also the training points
            ax.scatter(X[:,0],X[:,1],c=Gr,cmap=cmap_bold)
            ax.set_xlim(xx.min(),xx.max())
            ax.set_ylim(yy.min(),yy.max())
            ax.set_xlabel(Lc[nx])
            ax.set_ylabel(Lc[ny])
            ax.set_title("3-Class classification (k = %i)" % (self.knspinBox.value()))
        fig.show()

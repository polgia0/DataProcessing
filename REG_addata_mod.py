from config import DS,REG
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
def regaddata(self):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    data=DS.Raw.loc[DS.Ir,DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Ts=DS.Ts[DS.Ir]
    X=data.loc[:,-Gc]
    Y=data.loc[:,Gc]
    Xtrain=X[-Ts]
    Ytrain=Y[-Ts]
    Xtest=X[Ts]
    Ytest=Y[Ts]
    Lr=DS.Lr[DS.Ir]
    Lrt=Lr[-Ts]
    Lrs=Lr[Ts]
    Lc=DS.Lc[DS.Ic]
    Lcx=Lc[-Gc]
    ncx=len(Lcx)
    Lcy=Lc[Gc]
    scoretr=REG.lr.score(Xtrain,Ytrain)
    if len(Ytest)>0:
        if ncx==1:
            ax.scatter(Xtrain,Ytrain,marker='o',color='blue',label='Train Score: {:04.2f}'.format(scoretr))
            if self.VcheckBox.isChecked():
                for i,txt in enumerate(Lrt):
                    ax.annotate(txt,(Xtrain.iloc[i],Ytrain.iloc[i]),color='blue')
            if len(Ytest)>0:
                scorets=REG.lr.score(Xtest,Ytest)
                ax.scatter(Xtest,Ytest,marker='o',color='green',label='Test Score: {:04.2f}'.format(scorets))
                if self.VcheckBox.isChecked():
                    for i,txt in enumerate(Lrs):
                        ax.annotate(txt,(Xtest.iloc[i],Ytest.iloc[i]),color='green')
            Yfit=REG.lr.predict(Xtrain)
            ax.plot(Xtrain,Yfit,color='red')
            ax.set_title('Intercept: {:06.2e}'.format(REG.lr.intercept_)+
            ' Coefficient: {:06.2e}'.format(REG.lr.coef_[0]))
            ax.set_xlabel(Lcx[0])
            ax.set_ylabel(Lcy[0])
        else:
            scorets=REG.lr.score(Xtest,Ytest)
            REG.TXt=REG.lr.predict(Xtest)
            ax.scatter(Ytest,REG.TXt,marker='o',color='red',label='Test Score: {:04.2f}'.format(scorets))
            if REG.model=='lasso':
                nscore=np.sum(REG.lr.coef_ !=0)
                ax.scatter(Ytest,REG.TXt,marker='o',color='red',label='Variable used: {:04.2f}'.format(nscore))
            Dmin=min([float(Ytest.min()),float(REG.TXt.min())])
            Dmax=max([float(Ytest.max()),float(REG.TXt.min())])
            ax.set_xlim([Dmin,Dmax])
            ax.set_ylim([Dmin,Dmax])
            ax.set_title('Predicted vs. Measured Plot for '+Lcy[0])
            ax.add_line(Line2D([Dmin,Dmax],[Dmin,Dmax],color='red')) 
            ax.set_xlabel(Lcy[0]+' measured')
            ax.set_ylabel(Lcy[0]+' predicted')
    if len(Ytest)==0:
        width=0.35
        ind=np.arange(1,ncx+1)
        ax.bar(ind,REG.lr.coef_,width,color='b',label='Train Score: {:04.2f}'.format(scoretr))
        ax.set_title('Regression for '+Lcy[0]+': Intercept: {:04.2f}'.format(REG.lr.intercept_))
        ax.set_xticks(ind+width/4)
        ax.set_xticklabels(Lcx, rotation='vertical')
        ax.set_xlabel('Factors')
        ax.set_ylabel('Coefficients')
    ax.legend(loc='upper left')
    ax.xaxis.grid()
    ax.yaxis.grid()
    fig.show()


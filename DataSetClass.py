class OSint(object):
    def __init__(self,os='nt',d=',',s=';',sep='\t',nl='\n',f='FALSO',t='VERO'):
        self.os=os
        self.d=d
        self.s=s
        self.sep=sep
        self.nl=nl
        self.f=f
        self.t=t
class Fit(object):
    def __init__(self,model=None,x=None,y=False,p=None,jac=None,res=None):
        self.model=model
        self.x=x
        self.y=y
        self.p=p
        self.jac=jac
        self.res=res
class Reg(object):
    def __init__(self,model=None,lr=None,normalize=False,alpha=None,maxiter=None,
                 seed=None,Ycv=None,TXt=None,dB=None,dism=None,pS=None):
        self.model=model
        self.lr=lr
        self.normalize=normalize
        self.alpha=alpha
        self.maxiter=maxiter
        self.seed=seed
        self.Ycv=Ycv
        self.TXt=TXt
        self.dB=dB
        self.dism=dism
        self.pS=pS
class Doe(object):
    def __init__(self,coded=False,lfac=None,res=None):
        self.lfac=lfac
        self.coded=coded
        self.res=res
class Pls(object):
    def __init__(self,ncp=None,Xc=None,Yc=None,Xm=None,Ym=None,
                 Sx=None,Sy=None,SSX=None,SSY=None,P=None,C=None,U=None,
                 T=None,Q=None,W=None,WS=None,B=None,Ysc=None,Ys=None,
                 R2=None,SPEX=None,SPEY=None,HT2=None,VIP=None,T95=None,
                 T99=None,bc=None,bs=None,bp=None,Ycv=None,Ycvs=None,TXt=None):
        self.ncp=ncp
        self.Xc=Xc
        self.Yc=Yc
        self.Xm=Xm
        self.Ym=Ym
        self.Sx=Sx
        self.Sy=Sy
        self.SSX=SSX
        self.SSY=SSY
        self.P=P
        self.C=C
        self.U=U
        self.T=T
        self.Q=Q
        self.W=W
        self.WS=WS
        self.B=B
        self.Ysc=Ysc
        self.Ys=Ys
        self.R2=R2
        self.SPEX=SPEX
        self.SPEY=SPEY
        self.HT2=HT2
        self.VIP=VIP
        self.T95=T95
        self.T99=T99
        self.bc=bc
        self.bp=bp
        self.bs=bs
        self.Ycv=Ycv
        self.Ycvs=Ycvs
class Pca(object):
    def __init__(self,ncp=None,Xc=None,sco=None,lo=None,ei=None,rv=None,sse=None,
                 ssx=None,ht2=None,Q=None,res=None,cres=None,Xm=None,Xstd=None,
                 MQ=None,MT=None,Q95=None,Q99=None,T95=None,T99=None,bc=None,
                 bs=None,bp=None,Xcv=None,TXt=None):
        self.ncp=ncp
        self.Xc=Xc
        self.sco=sco
        self.lo=lo
        self.ei=ei
        self.rv=rv
        self.ssx=ssx
        self.sse=sse
        self.ht2=ht2
        self.Q=Q
        self.res=res
        self.cres=cres
        self.Xm=Xm
        self.Xstd=Xstd
        self.MQ=MQ
        self.MT=MT
        self.Q95=Q95
        self.Q99=Q99
        self.T95=T95
        self.T99=T99
        self.bc=bc
        self.bp=bp
        self.bs=bs
        self.Xcv=Xcv
        self.TXt=TXt
class Dataset(object):
    def __init__(self,Raw=None,Ir=None,Ic=None,Gr=None,Gc=None,Lr=None,
                 Lc=None,Cr=None,Cc=None,Ts=None,Ty=None,Cl=None):
        self.Raw=Raw
        self.Ir=Ir
        self.Ic=Ic
        self.Gr=Gr
        self.Gc=Gc
        self.Lr=Lr
        self.Lc=Lc
        self.Cr=Cr
        self.Cc=Cc
        self.Ts=Ts
        self.Ty=Ty
        self.Cl=Cl

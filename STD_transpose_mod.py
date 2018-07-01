from config import DS
import numpy as np
def transpose(self):
    DS.Raw=DS.Raw.transpose()
    Ir=DS.Ir
    Ic=DS.Ic
    DS.Ir=Ic
    DS.Ic=Ir
    DS.Gr=np.ones(len(DS.Ir),dtype=int)
    DS.Gc=np.zeros(len(DS.Ic),dtype=bool)
    Lr=DS.Lr
    Lc=DS.Lc
    DS.Lr=Lc
    DS.Lc=Lr
    Cr=DS.Cr
    Cc=DS.Cc
    DS.Cr=Cc
    DS.Cc=Cr
    DS.Ts=np.array(np.zeros(len(DS.Ir)),dtype=bool)
    DS.Ty=DS.Raw.dtypes.values
    return(True)

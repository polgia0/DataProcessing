from config import PLS,DS
import xlwings as xw
import numpy as np
def plssave(self):  
    self.appExcel=xw.App()
    wb=xw.books.active
    Lr=DS.Lr[DS.Ir]
    Ts=DS.Ts[DS.Ir]
    Lrtr=Lr[-Ts][np.newaxis]
    Lrts=Lr[Ts][np.newaxis]
    Lc=DS.Lc[DS.Ic]
    Gc=DS.Gc[DS.Ic]
    Lcx=Lc[-Gc,]
    Lcy=Lc[Gc,]
    Lcx=Lcx[np.newaxis]
    Lcy=Lcy[np.newaxis]
    Lc=Lc[np.newaxis]
    sht=wb.sheets[0]
    sht.name='DataSet'
    sht.range('B1').value= Lcx.ravel().tolist()+Lcy.ravel().tolist()
    sht.range('B2').value=np.concatenate((PLS.Xm.ravel(),PLS.Ym.ravel()),axis=0)  
    sht.range('B3').value= np.concatenate((PLS.Sx.ravel(),PLS.Sy.ravel()),axis=0) 
    sht.range('B4').value=np.concatenate((PLS.SSX.ravel(),PLS.SSY.ravel()),axis=0) 
    sht.range('A2').value='mean'
    sht.range('A3').value='std'
    sht.range('A4').value='ssm'
    if(DS.Cl!=None):
        sht.range('B5').value=range(len(DS.Cl))  
        sht.range('A6').value='Group Class'
        sht.range('B6').value=DS.Cl
    sht.range('A8').value=Lrtr.T
    sht.range('B8').value=np.concatenate((PLS.Xc,PLS.Yc),axis=1)
    sht=wb.sheets[1]
    sht.name='Loading'
    sht.range('A1').value='n.comp.'
    sht.range('A2').value=Lcx.T
    sht.range('B1').value=np.array(range(1,PLS.ncp+1))
    sht.range('B2').value=PLS.P
    sht=wb.sheets[2]
    sht.name='Y-Loading'
    sht.range('A1').value='n.comp.'
    sht.range('A2').value=Lcy.T
    sht.range('B1').value=np.array(range(1,PLS.ncp+1))
    sht.range('B2').value=PLS.Q
    wb.sheets.add(name='X-Scores')
    sht=wb.sheets['X-Scores']
    sht.range('A1').value='n.comp.'
    sht.range('B1').value=np.array(range(1,PLS.ncp+1))
    sht.range('A2').value=Lrtr.T
    sht.range('B2').value=PLS.T
    wb.sheets.add(name='Y-Scores')
    sht=wb.sheets['Y-Scores']
    sht.range('A1').value='n.comp.'
    sht.range('B1').value=np.array(range(1,PLS.ncp+1))
    sht.range('A2').value=Lrtr.T
    sht.range('B2').value=PLS.U
    wb.sheets.add(name='Weight')
    sht=wb.sheets['Weight']
    sht.range('A1').value='n.comp.'
    sht.range('A2').value='Reg.Coef.'
    sht.range('A4').value=Lcx.T
    sht.range('B1').value=np.array(range(1,PLS.ncp+1))
    sht.range('B2').value=np.diag(PLS.C).T
    sht.range('B4').value=PLS.W
    wb.sheets.add(name='Coefficient')
    sht=wb.sheets['Coefficient']
    sht.range('A2').value=Lcx.T
    sht.range('B1').value=Lcy
    sht.range('B2').value=PLS.B
    wb.sheets.add(name='H2-SPE')
    sht=wb.sheets['H2-SPE']
    sht.range('A2').value=Lrtr.T
    sht.range('B1').value='Ht^2'
    sht.range('B2').value=PLS.HT2
    sht.range('C1').value='SPEX'
    sht.range('C2').value=PLS.SPEX[np.newaxis].T   
    sht.range('D1').value='SPEY'
    sht.range('D2').value=PLS.SPEY[np.newaxis].T
    wb.sheets.add(name='Fitting Centered')
    sht=wb.sheets['Fitting Centered']
    sht.range('B1').value=Lcy
    sht.range('A2').value=Lrtr.T
    sht.range('B2').value=PLS.Ysc
    wb.sheets.add(name='Fitting Original')
    sht=wb.sheets['Fitting Original']
    sht.range('B1').value=Lcy
    sht.range('A2').value=Lrtr.T
    sht.range('B2').value=PLS.Ys
    wb.sheets.add(name='VIP')
    sht=wb.sheets['VIP']
    sht.range('A1').value=Lcx.T
    sht.range('B1').value=PLS.VIP[np.newaxis].T
    try:
        wb.sheets.add(name='CV centered')
        sht=wb.sheets['CV centered']
        sht.range('B2').value=PLS.Ycv
        sht.range('B1').value=Lcy
        sht.range('A2').value=Lrtr.T
        wb.sheets.add(name='CV original')
        sht=wb.sheets['CV original']
        sht.range('B2').value=PLS.Ycvs
        sht.range('B1').value=Lcy
        sht.range('A2').value=Lrtr.T
    except:
        pass
    try:
        wb.sheets.add(name='Additional')
        sht=wb.sheets['Additional']
        sht.range('B2').value=PLS.TXt
        sht.range('B1').value=Lcy
        sht.range('A2').value=Lrts.T
    except:
        pass

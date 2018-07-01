from config import DS
import xlwings as xw
import numpy as np
def sendexcel(self):
    try:
        self.appExcel=xw.App()
        wb=xw.books.active
        sht=wb.sheets[0]
        sht.range('E1').value='Type'
        sht.range('E1').color=(255,51,255)
        sht.range('F1').value=[str(x) for x in DS.Ty]
        sht.range('E2').value='Y'
        sht.range('E2').color=(160,160,160)
        sht.range('F2').value=DS.Gc
        sht.range('E3').value='Label'
        sht.range('E3').color=(0,102,204)
        sht.range('F3').value=DS.Lc
        sht.range('E4').value='Include'
        sht.range('E4').color=(255,51,51)
        sht.range('F4').value=DS.Ic
        sht.range('E5').value='Colors'
        sht.range('E5').color=(128,255,0)
        sht.range('F5').value=DS.Cc
        sht.range('F6').options(index=False, header=False).value=DS.Raw
        sht.range('E6').value=DS.Cr[np.newaxis].T
        sht.range('A5').value='Group'
        sht.range('A5').color=(255,51,255)
        sht.range('A6').value=DS.Gr[np.newaxis].T
        sht.range('B5').value='Test'
        sht.range('B5').color=(160,160,160)
        sht.range('B6').value=DS.Ts[np.newaxis].T
        sht.range('C5').value='Label'
        sht.range('C5').color=(0,102,204)
        sht.range('C6').value=DS.Lr[np.newaxis].T
        sht.range('D5').value='Include'
        sht.range('D5').color=(255,51,51)
        sht.range('D6').value=DS.Ir[np.newaxis].T
    except:
        pass


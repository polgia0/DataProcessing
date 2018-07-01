#Language: python3.4
# main module of : DataProcessing
AUTHOR="Gianmarco Polotti"
LICENCE="GNU GPL v.3"
VERSION="3.00"
import sys
from config import DS,PCA,PLS,REG
from PyQt5 import QtWidgets,QtCore
from PyQt5.uic import loadUiType
from show_dataset_mod import show_dataset,prepare_show,operate_show
from File_opencsv_mod import opencsvDlg
from File_openxls_mod import openxlsDlg
from Data_export_mod import exportDlg
from Data_exclude_mod import excludeDlg
from Data_missing_mod import missingDlg
from Data_groups_mod import groupsDlg
from Data_split_mod import splitDlg
from Data_getexcel_mod import getexcel
from Data_sendexcel_mod import sendexcel
from EDA_Univariateplot_mod import univariateplotDlg
from EDA_Univariategroup_mod import univariategroupDlg
from EDA_Univariaterow_mod import univariaterowDlg
from EDA_Bivariateplot_mod import bivariateplotDlg
from EDA_Bivariategroup_mod import bivariategroupDlg
from EDA_Bivariaterow_mod import bivariaterowDlg
from EDA_Trivariate_mod import trivariateplotDlg
from EDA_Multivariate_mod import multivariateplotDlg
from EDA_Timeseriesplot_mod import timeseriesplotDlg
from STD_summary_mod import summary
from STD_binning_mod import binningDlg
from STD_averagediff_mod import averagediffDlg
from STD_Rowunfolding_mod import rowunfolding
from STD_transpose_mod import transpose
from CLA_neighbors_mod import neighborsDlg
from CLA_linear_mod import linearDlg
from REG_model_mod import regmodelDlg
from REG_plot_mod import regplotDlg
from REG_addata_mod import regaddata
from REG_save_mod import regsave
from PCA_component_mod import pcacomp
from PCA_model_mod import pcamodelDlg
from PCA_plot_mod import pcaplotDlg
from PCA_score_mod import pcascoreDlg
from PCA_mixed_mod import pcamixedplotDlg
from PCA_addata_mod import pcaaddataDlg
from PCA_save_mod import pcasave
from PLS_model_mod import plsmodelDlg
from PLS_plot_mod import plsplotDlg
from PLS_weight_mod import plsweightDlg
from PLS_component_mod import plscomp
from PLS_addata_mod import plsaddata
from PLS_save_mod import plssave
from DOE_plot_mod import doeplotDlg
from DOE_analy_mod import doeanalyDlg
from DOE_matrix_mod import doematrixDlg
from DOE_model_mod import doemodel
from DOE_save_mod import doesave
Ui_MainWindow,QMainWindow=loadUiType('dataprocessing.ui')
class MainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    from table_dataset_mod import show_dataMenu,show_barMenu,hide_Ir,hide_Ic,hide_Gr,hide_Gc,hide_Cr,hide_Cc,hide_Ts,hide_Ty
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setGeometry(5,5,650,50)
        self.actionGroups.triggered.connect(self.groups_dialog)
        self.actionCSV.triggered.connect(self.opencsv_dialog)
        self.actionXLS.triggered.connect(self.openxls_dialog)
        self.actionGet_from_Excel.triggered.connect(self.getexcel_dialog)
        self.actionSend_to_Excel.triggered.connect(self.sendexcel_dialog)
        self.actionExport.triggered.connect(self.export_dialog)
        self.actionExclude.triggered.connect(self.exclude_dialog)
        self.actionMissing.triggered.connect(self.missing_dialog)
        self.actionSplit.triggered.connect(self.split_dialog)
        self.actionSummary.triggered.connect(self.summary_dialog)
        self.actionTranspose.triggered.connect(self.transpose_dialog)
        self.actionBinning.triggered.connect(self.binning_dialog)
        self.actionAverage_difference.triggered.connect(self.averagediff_dialog)
        self.actionRow_Unfolding.triggered.connect(self.rowunfolding_dialog)
        self.actionUnivariate_Plot.triggered.connect(self.univariate_plot_dialog)
        self.actionUnivariate_by_Groups.triggered.connect(self.univariate_group_dialog)
        self.actioUnivariate_by_Row.triggered.connect(self.univariate_row_dialog)
        self.actionBivariate_Plot.triggered.connect(self.bivariateplot_dialog)
        self.actionBivariate_by_Groups.triggered.connect(self.bivariate_group_dialog)
        self.actionBivariate_by_Row.triggered.connect(self.bivariate_row_dialog)
        self.actionTrivariate_Plot.triggered.connect(self.trivariateplot_dialog)
        self.actionMultivariate.triggered.connect(self.multivariateplot_dialog)
        self.actionTime_Series.triggered.connect(self.timeseriesplot_dialog)
        self.actionK_Neighbors.triggered.connect(self.neighbors_dialog)
        self.actionLinear_models.triggered.connect(self.linear_dialog)
        self.actionREGmodel.triggered.connect(self.regmodel_dialog)
        self.actionREGeneral_Plots.triggered.connect(self.regplot_dialog)
        self.actionREGSave_Results_2.triggered.connect(self.regsave_dialog)
        self.actionREGAdditional_Data.triggered.connect(self.regaddata_dialog)
        self.actionPCAcompo.triggered.connect(self.pcacomp_dialog)
        self.actionPCAmodel_2.triggered.connect(self.pcamodel_dialog)
        self.actionPCAplot_2.triggered.connect(self.pcaplot_dialog)
        self.actionPCAscore_2.triggered.connect(self.pcascore_dialog)
        self.actionPCAadditional_2.triggered.connect(self.pcaaddata_dialog)
        self.actionPCAmixed_2.triggered.connect(self.pcamixedplot_dialog)
        self.actionPCASave_Results_3.triggered.connect(self.pcasave_dialog)
        self.actionPLSmodel.triggered.connect(self.plsmodel_dialog)
        self.actionPLSplot.triggered.connect(self.plsplot_dialog)
        self.actionPLScompo.triggered.connect(self.plscomp_dialog)
        self.actionPLSweight.triggered.connect(self.plsweight_dialog)
        self.actionPLSadditional.triggered.connect(self.plsaddata_dialog)
        self.actionPLSSave_Results_4.triggered.connect(self.plssave_dialog)
        self.actionDOEplots.triggered.connect(self.doeplot_dialog)
        self.actionDOEanalysis.triggered.connect(self.doeanaly_dialog)
        self.actionDOExp_Matrix.triggered.connect(self.doematrix_dialog)
        self.actionDOESave_Results_5.triggered.connect(self.doesave_dialog)
        self.actionAbout.triggered.connect(self.about)
        self.progressBar.valueChanged.connect(self.onProgressBarValueChanged)
        self.view.hide()
        self.progressBar.hide()        
        self.pushButton_Ir.hide()
        self.pushButton_Ic.hide()
        self.pushButton_Cr.hide()
        self.pushButton_Cc.hide()
        self.pushButton_Ts.hide()
        self.pushButton_Ty.hide()
        self.pushButton_Gc.hide()
        self.pushButton_Gr.hide()
        self.setGeometry(300,300,500, 10)
    def onProgressBarValueChanged(self,value):
        if value >= DS.Raw.shape[0]:
            self.progressBar.hide()
    def timerEvent(self,event):
        model=self.view.model()
        if model == None: 
            self.timer.stop()
        if not model.canFetchMore(QtCore.QModelIndex()):
            self.onProgressBarValueChanged(DS.Raw.shape[0])
            self.timer.stop()
        model.fetchMore(QtCore.QModelIndex())
        self.progressBar.setValue(self.model.rowCount(QtCore.QModelIndex()))
        if not self.timer.isActive():
            self.timer.start(self.timerPeriod,self)
    def checkDS(self):
        if DS.Raw is None:
            QtWidgets.QMessageBox.critical(self,'Error',"No Data Set \n Loaded !",\
                                           QtWidgets.QMessageBox.Ok)
            return(True)
        else:
            return(False)
    def checkPCA(self):
        if PCA.ncp is None:
            QtWidgets.QMessageBox.critical(self,'Error',"No Model \n Run Model First !",\
                                           QtWidgets.QMessageBox.Ok)
            return(True)
        else:
            return(False)
    def checkPLS(self):
        if PLS.ncp is None:
            QtWidgets.QMessageBox.critical(self,'Error',"No Model \n Run Model First !"\
                                           ,QtWidgets.QMessageBox.Ok)
            return(True)
        else:
            return(False)
    def checkREG(self):
        if REG.model is None:
            QtWidgets.QMessageBox.critical(self,'Error',"No Model \n Run Model First !"\
                                           ,QtWidgets.QMessageBox.Ok)
            return(True)
        else:
            return(False)
    def checkDOE(self):
        Lc=DS.Lc[DS.Ic]
        Gc=DS.Gc[DS.Ic]
        if len(Lc[-Gc]) < 1:
            QtWidgets.QMessageBox.critical(self,'Error',"Any factor available",\
                                           QtWidgets.QMessageBox.Ok)
            return(True)
        if len(Lc[Gc]) < 1:
            QtWidgets.QMessageBox.critical(self,'Error',"Any responce available",\
                                           QtWidgets.QMessageBox.Ok)
            return(True)
        return(False)
    def opencsv_dialog(self):
        opencsv=QtWidgets.QDialog()
        opencsv=opencsvDlg()
        opencsv.exec_()
        opencsv.show()
        if DS.Raw is not None:
            prepare_show(self)
            show_dataset(self)
            operate_show(self)
    def openxls_dialog(self):
        openxls=QtWidgets.QDialog()
        openxls=openxlsDlg()
        openxls.exec_()
        openxls.show()
        if DS.Raw is not None:
            prepare_show(self)
            show_dataset(self)
            operate_show(self)
    def sendexcel_dialog(self):
        if self.checkDS():return()
        sendexcel(self)
    def getexcel_dialog(self):
        if self.checkDS():return()
        getexcel(self)
        show_dataset(self)
    def export_dialog(self):
        export=QtWidgets.QDialog()
        export=exportDlg()
        export.exec_()
        export.show()
    def missing_dialog(self):
        if self.checkDS():return()
        missing=QtWidgets.QDialog()
        missing=missingDlg()
        missing.exec_()
        missing.show()
        show_dataset(self)
    def groups_dialog(self):
        if self.checkDS():return()
        groups=QtWidgets.QDialog()
        groups=groupsDlg()
        groups.exec_()
        groups.show()
        show_dataset(self)
    def exclude_dialog(self):
        if self.checkDS():return()
        exclude=QtWidgets.QDialog()
        exclude=excludeDlg()
        exclude.exec_()
        exclude.show()
        show_dataset(self)
    def split_dialog(self):
        if self.checkDS():return()
        split=QtWidgets.QDialog()
        split=splitDlg()
        split.exec_()
        split.show()
        show_dataset(self)
    def univariate_plot_dialog(self):
        if self.checkDS():return()
        univariate=QtWidgets.QDialog()
        univariate=univariateplotDlg()
        univariate.exec_()
        univariate.show()
    def univariate_group_dialog(self):
        if self.checkDS():return()
        univariate_group=QtWidgets.QDialog()
        univariate_group=univariategroupDlg()
        univariate_group.exec_()
        univariate_group.show()
    def univariate_row_dialog(self):
        if self.checkDS():return()
        univariate_row=QtWidgets.QDialog()
        univariate_row=univariaterowDlg()
        univariate_row.exec_()
        univariate_row.show()
    def bivariateplot_dialog(self):        
        if self.checkDS():return()
        bivariateplot=QtWidgets.QDialog()
        bivariateplot=bivariateplotDlg()
        bivariateplot.exec_()
        bivariateplot.show()
    def bivariate_group_dialog(self):        
        if self.checkDS():return()
        bivariate_group=QtWidgets.QDialog()
        bivariate_group=bivariategroupDlg()
        bivariate_group.exec_()
        bivariate_group.show()
    def bivariate_row_dialog(self):        
        if self.checkDS():return()
        bivariate_row=QtWidgets.QDialog()
        bivariate_row=bivariaterowDlg()
        bivariate_row.exec_()
        bivariate_row.show()
    def trivariateplot_dialog(self):        
        if self.checkDS():return()
        trivariateplot=QtWidgets.QDialog()
        trivariateplot=trivariateplotDlg()
        trivariateplot.exec_()
        trivariateplot.show()
    def multivariateplot_dialog(self):
        if self.checkDS():return()
        multivariateplot=QtWidgets.QDialog()
        multivariateplot=multivariateplotDlg()
        multivariateplot.exec_()
        multivariateplot.show()
    def timeseriesplot_dialog(self):
        if self.checkDS():return()
        timeseriesplot=QtWidgets.QDialog()
        timeseriesplot=timeseriesplotDlg()
        timeseriesplot.exec_()
        timeseriesplot.show()
    def summary_dialog(self):
        if self.checkDS():return()
        summary(self)
    def transpose_dialog(self):
        if self.checkDS():return()
        r=transpose(self)
        if r:
            show_dataset(self)
    def averagediff_dialog(self):
        if self.checkDS():return()
        averagediff=QtWidgets.QDialog()
        averagediff=averagediffDlg()
        averagediff.exec_()
        averagediff.show()
    def binning_dialog(self):
        if self.checkDS():return()
        binning=QtWidgets.QDialog()
        binning=binningDlg()
        binning.exec_()
        binning.show()
    def rowunfolding_dialog(self):
        if self.checkDS():return()
        rowunfolding(self)
    def linear_dialog(self):
        if self.checkDS():return()
        linear=QtWidgets.QDialog()
        linear=linearDlg()
        linear.exec_()
        linear.show()
    def neighbors_dialog(self):
        if self.checkDS():return()
        neighbors=QtWidgets.QDialog()
        neighbors=neighborsDlg()
        neighbors.exec_()
        neighbors.show()
    def regplot_dialog(self):
        if self.checkDS():return()
        if self.checkREG():return()
        regplot=QtWidgets.QDialog()
        regplot=regplotDlg()
        regplot.exec_()
        regplot.show()
    def regmodel_dialog(self):
        if self.checkDS():return()
        regmodel=QtWidgets.QDialog()
        regmodel=regmodelDlg()
        r=regmodel.exec_()
        regmodel.show()
        if r:
            show_dataset(self)
    def regaddata_dialog(self):
        if self.checkDS():return()
        if self.checkREG():return()
        regaddata(self)
    def regsave_dialog(self):
        if self.checkDS():return()
        if self.checkREG():return()
        regsave(self)
    def pcacomp_dialog(self):
        if self.checkDS():return()
        pcacomp(self)
    def pcamodel_dialog(self):
        if self.checkDS():return()
        pcamodel=QtWidgets.QDialog()
        pcamodel=pcamodelDlg()
        r=pcamodel.exec_()
        pcamodel.show()
        print(r)
        if r:
            QtWidgets.QMessageBox.information(self,                           \
            'Message','The PCA Model is done !\n Now choose a plot',          \
            QtWidgets.QMessageBox.Ok)
            show_dataset(self)
    def pcaplot_dialog(self):
        if self.checkDS():return()
        if self.checkPCA():return()
        pcaplot=QtWidgets.QDialog()
        pcaplot=pcaplotDlg()
        pcaplot.exec_()
        pcaplot.show()
    def pcascore_dialog(self):
        if self.checkDS():return()
        if self.checkPCA():return()
        pcascore=QtWidgets.QDialog()
        pcascore=pcascoreDlg()
        pcascore.exec_()
        pcascore.show()
    def pcamixedplot_dialog(self):
        if self.checkDS():return()
        if self.checkPCA():return()
        pcamixedplot=QtWidgets.QDialog()
        pcamixedplot=pcamixedplotDlg()
        pcamixedplot.exec_()
        pcamixedplot.show()
    def pcaaddata_dialog(self):
        if self.checkDS():return()
        if self.checkPCA():return()
        pcaaddata=QtWidgets.QDialog()
        pcaaddata=pcaaddataDlg()
        pcaaddata.exec_()
        pcaaddata.show()
    def pcasave_dialog(self):
        if self.checkDS():return()
        if self.checkPCA():return()
        pcasave(self)
    def plscomp_dialog(self):
        if self.checkDS():return()
        plscomp(self)
    def plsweight_dialog(self):
        if self.checkDS():return()
        if self.checkPLS():return()
        plsweight=QtWidgets.QDialog()
        plsweight=plsweightDlg()
        plsweight.exec_()
        plsweight.show()
    def plsplot_dialog(self):
        if self.checkDS():return()
        if self.checkPLS():return()
        plsplot=QtWidgets.QDialog()
        plsplot=plsplotDlg()
        plsplot.exec_()
        plsplot.show()
    def plsmodel_dialog(self):
        if self.checkDS():return()
        plsmodel=QtWidgets.QDialog()
        plsmodel=plsmodelDlg()
        r=plsmodel.exec_()
        plsmodel.show()
        if r:
            QtWidgets.QMessageBox.information(self,                           \
            'Message','The PLS Model is done !\n Now choose a plot',          \
            QtWidgets.QMessageBox.Ok)
            show_dataset(self)
    def plsaddata_dialog(self):
        if self.checkDS():return()
        if self.checkPLS():return()
        plsaddata(self)
    def plssave_dialog(self):
        if self.checkDS():return()
        if self.checkPLS():return()
        plssave(self)
    def doematrix_dialog(self):
        doematrix=QtWidgets.QDialog()
        doematrix=doematrixDlg()
        doematrix.exec_()
        doematrix.show()
    def doeanaly_dialog(self):
        if self.checkDS():return()
        if self.checkDOE():return()
        doemodel(self)
        doeanaly=QtWidgets.QDialog()
        doeanaly=doeanalyDlg()
        doeanaly.exec_()
        doeanaly.show()
    def doeplot_dialog(self):
        if self.checkDS():return()
        if self.checkDOE():return()
        doemodel(self)
        doeplot=QtWidgets.QDialog()
        doeplot=doeplotDlg()
        doeplot.exec_()
        doeplot.show()
    def doesave_dialog(self):
        if self.checkDS():return()
        if self.checkDOE():return()
        doesave(self)
    def about(self):
        QtWidgets.QMessageBox.information(self,'DataProcessing',
            'Author: ' + AUTHOR+
            '\nLicence: ' + LICENCE+
            '\nVersion: ' + VERSION,QtWidgets.QMessageBox.Ok)
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

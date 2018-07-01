import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages":[],"excludes": ["tkinter"], \
"includes": ["PyQt5","sklearn","matplotlib","mglearn","numpy","pandas",  \
 "xlwings","distutils","patsy","xlwings","pyDOE","itertools","math"],\
"include_files":["1.png","2.png","3.png","about.png","add.png","analysis.png", \
"Arrowl.png","Arrowr.png","bin.png","color.png","csv.png","dpf.png","exclude.png","exit.png", \
"export.png","get.png","group.png","Help.png","LT.png","M.png","matrix.png","miss.png","mixed.png", \
"model.png","number.png","open.png","plot.png","regre.png","row.png","save.png","score.png",\
"send.png","split.png","summary.png","trans.png","xls.png",\
"averagediff.ui","binning.ui","bivariategroup.ui","bivariateplot.ui","bivariaterow.ui",\
"dataprocessing.ui","doeanaly.ui","doematrix.ui","doeplot.ui","exclude.ui","export.ui", \
"fitmodel.ui","fitplot.ui","groups.ui","linear.ui","linear.ui","matout.ui","missing.ui", \
"multivariate.ui","neighbors.ui","openCSV.ui","openXLS.ui","pcaaddata.ui","pcamixed.ui",\
"pcamixed.ui","pcamodel.ui","pcaplot.ui","pcascore.ui","plsmodel.ui","plsplot.ui","plsweight.ui",\
"regmodel.ui","regplot.ui","scatterplot.ui","split.ui","surtab.ui","test.ui","timeseriesplot.ui",\
"trivariateplot.ui","univariategroup.ui","univariateplot.ui","univariaterow.ui"] }

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "DataProcessing",
        version = "3.0",
        description = "Multivariate Data Analyser",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
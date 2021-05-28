from .functions import add_keyword
import numpy as np
import os

# data file for GMIN
def make_gmin_data(nin,nhidden,nout,norm=True,ndata="MLP_LINES",l2lambda="0.00001",nsteps=100000,f_outname='data.template'):
    fname = f_outname
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    add_keyword("SLOPPYCONV", fname, ["1.0D-6"])
    add_keyword("TIGHTCONV", fname, ["1.0D-9"])
    if norm==True:
        add_keyword("MLPNORM",fname)
    add_keyword("SAVE", fname,[1000])
    add_keyword("UPDATES", fname,[500])
    add_keyword("MAXIT", fname,[5000,5000])
    add_keyword("EDIFF", fname, ["1.0D-04"])
    add_keyword("STEPS", fname, [nsteps, 1.0])
    add_keyword("STEP", fname, ["1.0"])
    add_keyword("TEMPERATURE", fname, ["2.0"])
    add_keyword("DUMPINT", fname,[100])
    add_keyword("FIXBOTH",fname)
    add_keyword("MLPVB3", fname,[nin,1,nhidden,nout,ndata,l2lambda])

# odata dumpdata file to generate pathsample database
def make_odata_dumpdata(nin,nhidden,nout,norm=True,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'odata.dumpdata.template'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    if norm==True:
        add_keyword("MLPNORM",fname)
    add_keyword("SEARCH",fname,[0])
    add_keyword("DUMPDATA",fname)
    add_keyword("ENDHESS",fname)
    add_keyword("MAXBFGS",fname,["0.1","0.1"])
    add_keyword("UPDATES",fname,[1000,1000])
    add_keyword("BFGSMIN",fname,["1.0D-10"])
    add_keyword("STEPS",fname,[10000])
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword("VARIABLES",fname)

# write dumped minima from lowest to pathsample db
def make_pathdata_addmin(nin,nhidden,nout,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'pathdata.template.ADDMIN'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword("ALLTS",fname)    
    add_keyword('EVCUT',fname,['1.0D-7'])
    add_keyword('COPYFILES',fname,['MLPdata'])
    add_keyword('EDIFFTOL',fname,['1.0D-4'])
    add_keyword('GEOMDIFFTOL',fname,['1.0D2'])
    add_keyword('EXEC',fname,['OPTIM'])
    add_keyword("TEMPERATURE", fname, ["0.1"])
    add_keyword('PAIRLIST',fname,[1])
    add_keyword('ADDMIN',fname,['min.data.info.all'])

# extend pathsample db with one of the 4 keywords (3 commented out)
def make_pathdata_newconnections(nin,nhidden,nout,ndata="MLP_LINES",l2lambda="0.00001",curr_min=1):
    fname = 'pathdata.template.NEWCONNECTIONS'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword("ALLTS",fname)
    add_keyword('EVCUT',fname,['1.0D-7'])
    add_keyword('COPYFILES',fname,['MLPdata'])
    add_keyword('EDIFFTOL',fname,['1.0D-4'])
    add_keyword('GEOMDIFFTOL',fname,['1.0D2'])
    add_keyword('EXEC',fname,['OPTIM'])
    add_keyword("TEMPERATURE", fname, ["0.1"])
    add_keyword('CYCLES',fname,[5000])
    add_keyword('PAIRLIST',fname,[1])
    add_keyword('NEWCONNECTIONS',fname,[10000000,1000,curr_min])    
    add_keyword('comment UNTRAP',fname,['0.001','0.001'])
    add_keyword('comment CONNECTUNC',fname,['EREF','2'])
    add_keyword('comment CONNECTREGION',fname,['1','58','1.0D100'])
    add_keyword('SEED',fname,[str(np.random.randint(100000))])

# for pathsample db extension
def make_odata_connect(nin,nhidden,nout,norm=True,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'odata.connect.template'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    if norm==True:
        add_keyword("MLPNORM",fname)
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword('STEPMIN',fname,[100])
    add_keyword('NEWCONNECT',fname,[100,1,10.0,20.0,50,5.0,0.025])
    add_keyword('MAXERISE',fname,['1.0D-6','1.0D-3'])
    add_keyword('REOPTIMISEENDPOINTS',fname)
    add_keyword('NEWNEB',fname,[100,350,0.0001])
    add_keyword('DIJKSTRA',fname,['EXP'])
    add_keyword('MAXBFGS',fname,[0.1,0.1])
    add_keyword('EDIFFTOL',fname,['1.0D-4'])
    add_keyword('GEOMDIFFTOL',fname,['1.0D2'])
    add_keyword('DUMPALLPATHS',fname)
    add_keyword('MAXSTEP',fname,[0.01])
    add_keyword('MAXMAX',fname,[0.2])
    add_keyword('TRAD',fname,[1.0])
    add_keyword('NEBK',fname,[50.0])
    add_keyword('BFGSTS',fname,[5000,1,10,0.002])
    add_keyword('NOIT',fname)
    add_keyword('UPDATES',fname,[10,10])
    add_keyword('BFGSMIN',fname,['1.0D-9'])
    add_keyword('CONVERGE',fname,['1.0','1.0D-9'])
    add_keyword('PUSHOFF',fname,[0.2])
    add_keyword('STEPS',fname,[1000])
    add_keyword('BFGSSTEPS',fname,[50000])
    add_keyword('VARIABLES',fname)

# for pathsample db extension
def make_odata_tspath(nin,nhidden,nout,norm=True,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'odata.tspath.template'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    if norm==True:
        add_keyword("MLPNORM",fname)
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword('DUMPALLPATHS',fname)
    add_keyword('BFGSMIN',fname,['1.0D-9'])
    add_keyword('CONVERGE',fname,['1.0','1.0D-9'])
    add_keyword('EDIFFTOL',fname,['1.0D-4'])
    add_keyword('GEOMDIFFTOL',fname,['1.0D2'])
    add_keyword('BFGSTS',fname,[5000,1,10,0.002])
    add_keyword('NOIT',fname)
    add_keyword('PATH',fname,[3,0.0])
    add_keyword('SHIFT',fname,['1.0D10'])
    add_keyword('MAXSTEP',fname,[0.02])
    add_keyword('MAXMAX',fname,[0.04])
    add_keyword('TRAD',fname,['1.0D0'])
    add_keyword('STEPS',fname,[1000])
    add_keyword('UPDATES',fname,[10,10])
    add_keyword('BFGSSTEPS',fname,[50000])
    add_keyword('VARIABLES',fname)


def make_odata_auc(nin,nhidden,nout,norm=True,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'odata.AUC.template'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    if norm==True:
        add_keyword("MLPNORM",fname)
    add_keyword('MLPPROB',fname)
    add_keyword('BFGSMIN',fname,['1.0D100'])
    add_keyword('MULTIJOB',fname,['extractedmin'])
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword('VARIABLES',fname)


def make_pathdata_extractmin(nin,nhidden,nout,ndata="MLP_LINES",l2lambda="0.00001"):
    fname = 'pathdata.template.EXTRACTMIN'
    # remove old file
    if os.path.isfile(fname): os.remove(fname)
    # write new file
    add_keyword("MLPVB3",fname,[nin,1,nhidden,nout,ndata,l2lambda])
    add_keyword("ALLTS",fname)
    add_keyword('EVCUT',fname,['1.0D-7'])
    add_keyword('COPYFILES',fname,['MLPdata'])
    add_keyword('EDIFFTOL',fname,['1.0D-4'])
    add_keyword('GEOMDIFFTOL',fname,['1.0D2'])
    add_keyword('EXEC',fname,['OPTIM'])
    add_keyword("TEMPERATURE", fname, ["0.1"])
    add_keyword('PAIRLIST',fname,[1])
    add_keyword('EXTRACTMIN',fname,['EXTRACT_NO'])

def make_dinfo():
    fname='dinfo.template'
    add_keyword("DELTA",fname,['ENERGY_DIFFERENCE'])
    add_keyword("FIRST",fname,['HIGHEST_ENERGY'])
    add_keyword("comment MAXTSENERGY",fname,[0.395])
    add_keyword("CENTREGMIN",fname)
    add_keyword("comment CONNECTMIN",fname,[1])
    add_keyword("LEVELS",fname,['NO_OF_LEVELS'])
    add_keyword("MINIMA",fname,['min.data'])
    add_keyword("TS",fname,['ts.data'])
    add_keyword("comment IDENTIFY",fname)
    add_keyword("comment LOWEST",fname,[5000])
    add_keyword("comment MONOTONIC",fname)
    add_keyword("comment NCONNMIN",fname,[0])
    add_keyword("comment SCALEBAR",fname,[1])
    add_keyword("comment LABELFORMAT",fname,['E12.4'])
    add_keyword("comment TRMIN",fname,['2','NO_OF_MIN','AUCs2','AUCs1']) 
    add_keyword("comment TRMIN",fname,['1','NO_OF_MIN','AUCs1'])
    add_keyword("comment CHOOSECOLOURS",fname)








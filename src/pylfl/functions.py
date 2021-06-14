import numpy as np
import os
import os.path
import subprocess
import platform
import sys
import pkgutil
import re
import pylfl 
import shutil 
import glob

# determine platform at runtime
system = platform.system()
#arch, _ = platform.architecture()
if system == 'Linux':
    opsys='linux'
if system == 'Windows':
    opsys='win'
if system == 'Darwin':
    opsys='mac'
# determine relative path at runtime
path = pylfl.__path__[0]

# Adds a line to some *data file.
def add_keyword(keyword, filename:str, params=None):
    data_file = open(filename, "a")
    data_file.write(keyword)
    if params is not None:
        for p in params:
            data_file.write(" " + str(p))
    data_file.write("\n")

# Creates random coords file
def random_starting_coords(nweights):
    starting_coords = np.random.uniform(-5.0, 5.0,nweights)
    np.savetxt('coords',starting_coords[:,None], fmt='%.10f')
    
# change placeholders in some document
def fill_placeholders(fname:str, newfname:str, keyword:str, var):
    with open(fname, "r") as template:
        template_lines = template.readlines()
    with open(newfname, "w") as newtemp:
        for line in template_lines:
            edited_line = re.sub(keyword, str(var), line)
            newtemp.write(edited_line) 

# Run GMIN
def gmin():
    if os.path.isfile('data') and os.path.isfile('coords') and os.path.isfile('MLPdata'):
        # write output to file
        fl = open("gmin_output.txt", "w")
        # execute GMIN binary as defined by setup.py for correct OS
        if opsys != 'win':
            subprocess.call(path+f'/bin/{opsys}/GMIN', stdout=fl)
        else:
            subprocess.call(path+'/bin/win/GMIN.exe', stdout=fl)
    else:
        print('Data or coords file are missing')		

#run OPTIM
def optim(outfile='optim_output.txt'):
    if os.path.isfile('odata') and os.path.isfile('MLPdata'):
        # write output to file
        fl = open(outfile, "w")
        # execute OPTIM binary as defined by setup.py for correct OS
        if opsys != 'win':
            subprocess.call(path+f'/bin/{opsys}/OPTIM', stdout=fl)
        else:
            subprocess.call(path+'/bin/win/OPTIM.exe', stdout=fl)
    else:
        print('odata file is missing')

#run PATHSAMPLE
def pathsample():
    if os.path.isfile('pathdata') and os.path.isfile('MLPdata'):
        # write output to file
        fl = open("pathsample_output.txt", "w")
        # execute PS binary as defined by setup.py for correct OS
        if opsys != 'win':
            subprocess.call(path+f'/bin/{opsys}/PATHSAMPLE', stdout=fl)
#            shutil.copyfile(path+f'/bin/{opsys}/OPTIM',path+'/../../../../bin/OPTIM')
#            shutil.copymode(path+f'/bin/{opsys}/OPTIM',path+'/../../../../bin/OPTIM')
        else:
            subprocess.call(path+'/bin/win/PATHSAMPLE.exe', stdout=fl)
#            shutil.copyfile(path+f'/bin/win/OPTIM',path+'/../../../../bin/OPTIM')
#            shutil.copymode(path+f'/bin/win/OPTIM',path+'/../../../../bin/OPTIM')
    else:
        print('pathdata file is missing')


#initiate PATHSAMPLE database from lowest
def initpdb(dof): 
    lowest_lines=dof+2
    nlines=sum(1 for line in open('lowest'))
    nmin=int(nlines/lowest_lines)
    mlp_lines=sum(1 for line in open('MLPdata'))
    # edit dumpdata file
    fill_placeholders("odata.dumpdata.template","odata.dumpdata","MLP_LINES",mlp_lines)
    # extract minima one by one and write to pathsample db afterwards
    cdir = os.getcwd()
    for lmin in range(nmin):
        shutil.copyfile(cdir+'/odata.dumpdata',(cdir+'/odata'))
        head_lines=(lmin+1)*lowest_lines
        open("odata", "a").writelines([l for n,l in enumerate(open("lowest").readlines()) if n < head_lines if n >= (head_lines-dof)])
        # run OPTIM now
        optim()
        # reformat OPTIM output
        open("min.data.info.all","a").writelines([l for l in open("min.data.info").readlines()])
        lmin+=1
    # edit pathdata file
    fill_placeholders("pathdata.template.ADDMIN","pathdata","MLP_LINES",mlp_lines)
    # run PATHSAMPLE
    pathsample()
    open("min.A",'w').writelines("1\n1")
    open("min.B",'w').writelines("1\n2")
    os.remove('min.data.info')
    os.remove('min.data.info.all')


def extendpdb(curr_min=1):
    mlp_lines=sum(1 for line in open('MLPdata'))
    # first write pathdata file
    fill_placeholders("pathdata.template.NEWCONNECTIONS","pathdata","MLP_LINES",mlp_lines)
    fill_placeholders("pathdata","pathdata","CURR_MIN",curr_min)
    # next do both odata files
    fill_placeholders("odata.tspath.template","odata.tspath","MLP_LINES",mlp_lines)
    fill_placeholders("odata.connect.template","odata.connect","MLP_LINES",mlp_lines)
    # need to add OPTIM binary to PATH
    if opsys != 'win':
        sys.path.insert(0,path+f'/bin/{opsys}/OPTIM')
    else:
        sys.path.insert(0,path+f'/bin/win/OPTIM')
    # finally just run PATHSAMPLE
    pathsample()
    for fl in glob.glob('path.info.*'):
        os.remove(fl)
    for fl in glob.glob('submit_*'):
        os.remove(fl) 
    

def auc():
    mlp_lines=sum(1 for line in open('MLPdata'))
    fill_placeholders("pathdata.template.EXTRACTMIN","pathdata","MLP_LINES",mlp_lines)
    nmin=sum(1 for line in open('min.data'))
    fill_placeholders("odata.AUC.template","odata.AUC","MLP_LINES",mlp_lines)
    fill_placeholders("odata.AUC","odata","START_NO",str(1))
    if os.path.isfile('extractedmin.all'): os.remove('extractedmin.all')
    if os.path.isfile('extractedmin'): os.remove('extractedmin')
    for ind in range(nmin):
        minind=ind+1
        fill_placeholders("pathdata","pathdata","EXTRACT_NO",minind)
        pathsample()
        if minind == 1:
            open("odata", "a").writelines([l for l in open("extractedmin").readlines()])
        else:
            open("extractedmin.all","a").writelines([l for l in open("extractedmin").readlines()])
    open("extractedmin", "w").writelines([l for l in open("extractedmin.all").readlines()])   
    os.remove('extractedmin.all')
    optim(outfile='auc_logfile')
    # extract AUCs from optim logfile
    with open("auc_logfile","r") as f:
        auclist=[]
        for line in f:
            if line.startswith("energy, AUC="):
                auclist.append(line[8:])
    aucs = [elem.split()[2] for elem in auclist]
    aucs = list(map(float,aucs))
    np.savetxt('AUCs_unsorted',aucs,fmt='%.10f')
    sorted_aucs = np.sort(aucs)[::-1]
    np.savetxt('AUCs_sorted',sorted_aucs,fmt='%.10f')
    best_auc = np.max(aucs)
    return(best_auc) 













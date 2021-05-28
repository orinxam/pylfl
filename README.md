# pylfl
A tool for loss function landscape (LFL) exploration in Python. This package provides a Python interface for the software developed by the [Wales group](https://www.ch.cam.ac.uk/group/wales/index) including, [GMIN](http://www-wales.ch.cam.ac.uk/GMIN/),[OPTIM](http://www-wales.ch.cam.ac.uk/OPTIM/),[PATHSAMPLE](http://www-wales.ch.cam.ac.uk/PATHSAMPLE/) and visualisation using [disconnectivity graphs](http://www-wales.ch.cam.ac.uk/pdf/NATURE.394.758.1998.pdf).

The standard workflow of landscape exploration using the Wales software is the following.
1. Find minima of the LFL using GMIN
2. Write found minima to a pathsample database - this is needed to find transition states
3. Extend pathsample db and find transition states
4. Visualise LFL using disconnectivity graph (and calculate AUC of minima)

Below, each step is explained in detail. Please note that currently, only cross-entropy and approximated-AUC loss functions are supported. The below also considers a single hidden layer only, but more layers can be added with minimal effort. 

To install the package, simply 
```pip install pylfl```

You can load it into your session by
```import pylfl as pl```

## 1) GMIN: Finding minima of the LFL 
GMIN requires three files to be present. A _data_ file containing GMIN parameters,a _coords_ file containing the starting coordinates and a file _MLPdata_ containing the training data. All these must be present inside the directory from which GMIN is run (and have the exact names specified above). 
We provide templates for _data_ and _coords_ files, which can be simply generated by:
```
import pylfl as pl
import numpy as np

nin=2 #no. of input nodes
nhidden=3 #no. of hidden nodes
nout=2 #no. of output nodes
dof=17 #degree of freedom = no. of weights
ndata==sum(1 for line in open('MLPdata')) #count no. of data items
f_outname='data'

pl.make_gmin_data(nin,nhidden,nout,ndata=ndata,f_outname)
pl.random_starting_coords(dof)
```
Note that information about the individual keywords of the _data_ file can be found [here](http://www-wales.ch.cam.ac.uk/GMIN.doc/node7.html).
If all the files are present, you can simply execute
``` pl.gmin()```
which will run GMIN and upon completion return a file called _lowest_ that contains the energy (loss value) and coordinates of all found minima. 

## 2) Initiate PATHSAMPLE database
To find transition states, we need to convert the lowest file into a memory-efficient format that can be read by PATHSAMPLE. To do this, we require two more files to be present in the current directory, `odata.dumpdata` and `pathdata.addmin`. Again, we provide templates for these and they can be easily generated using
```
pl.make_odata_dumpdata(nin,nhidden,nout)
pl.make_pathdata_addmin(nin,nhidden,nout)
```
Information about the keywords in both files can be found in the respective [OPTIM keywords](http://www-wales.ch.cam.ac.uk/OPTIM.doc/node4.html) and [PATHSAMPLE keywords](http://www-wales.ch.cam.ac.uk/PATHSAMPLE.2.1.doc/node6.html) documentations.
To run this step, simply execute
```
pl.initpdb(dof)
```
This will return four different files: min.data (containing one line per minimum in _lowest_), ts.data (which will be empty as no transition state search has happened yet), and min.point/ts.points which will contain the coordinates of minima and ts (with ts again being empty for now).

## 3) Extend PATHSAMPLE database
To fill ts.data (and ts.points), we need to grow our PATHSAMPLE database using methods described in detail in the PATHSAMPLE documentation. In this step we now need three different files, templates of which can as before simply be obtained by
```
pl.make_pathdata_newconnections(nin,nhidden,nout)
pl.make_odata_connect(nin,nhidden,nout)
pl.make_odata_tspath(nin,nhidden,nout)
```
With the keywords again explained in the respective documentations. The 4 keywords `NEWCONNECTIONS, UNTRAP, CONNECTUNC, CONNECTREGION` are of special importance as they describe the four most commonly used ways to connect minima. Only one can be used at a time, and for a first run, `NEWCONNECTIONS` should be used. T
This step can then be executed by
```
pl.extendpdb()
```
which will search connections between minima as specified in the `pathdata.NEWCONNECTIONS` file. his step can be repeated multiple time with different to continuously grow the PATHSAMPLE database.  

In general, note that the `data,odata,pathdata` files provided by us are merely first templates to get a system working. As can be seen from the respective documentations, many more options exist to fine-tune the different programs. 

## 4) Compute AUC of all minima
To evaluate the minima for their AUC, the test dataset must now be written to the _MLPdata_ file (and hence replace the training data). The two files needed for AUC computation are `odata.AUC` and `pathdata.EXTRACTMIN`. The templates for both can be obtained via
```
pl.make_odata_auc(nin,nhidden,nout)
pl.make_pathdata_extractmin(nin,nhidden,nout)
```
and the AUC is then computed by
```
pl.auc()
```
This returns the maximum AUC as well as two files, AUCs_unsorted (which is a in-place bijection to the minima in min.data - i.e. the AUC of the minimum in line 25 of min.data is in line 25 of AUCs_unsorted), and AUCs_sorted, which is self-explanatory. 

## 5) Disconnectivity graphs
To visualise the landscapes, disconnectivity graphs can be computed using `pl.maketree()` with a _dinfo_ file. A template _dinfo_ file can be created by
```
pl.make_dinfo()
```
The disconnectivity graph is written to a file named _tree.ps_.









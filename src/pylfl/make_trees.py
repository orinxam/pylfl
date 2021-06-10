import math
import os
import os.path
import re
import subprocess
import platform
import pylfl

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


def maketree():
    with open("dinfo.template", "r") as template:
        template_lines = template.readlines()

    min_energies = []
    try:
        with open("min.data", "r") as f:
            for line in f:
                min_energies.append(float(line.split()[0]))
    except IOError:
        print(working_dir + ": min.data does not exist")
        os.chdir("..")
    min_count = len(min_energies)

    ts_energies = []
    try:
        with open("ts.data", "r") as f:
            for line in f:
                ts_energies.append(float(line.split()[0]))
    except IOError:
        print(working_dir + ": ts.data does not exist")
        os.chdir("..")

    if len(min_energies) == 1 and len(ts_energies) == 0:
        print(working_dir + ": database has 1 minimum and 0 ts")
        os.chdir("..")

    highest_energy = max(ts_energies)
    levels = 30
    delta = (highest_energy - min(min_energies)) / (levels - 1)
    # Round up to one significant figure (assumes 0 < delta < 1)
    mag = 0
    while (delta < 1):
        delta *= 10
        mag += 1
    delta = math.ceil(delta)
    while (mag > 0):
        delta /= 10
        mag -= 1

    with open("dinfo", "w") as dinfo:
        for line in template_lines:
            edited_line = re.sub("HIGHEST_ENERGY", str(highest_energy), line)
            edited_line = re.sub("ENERGY_DIFFERENCE", str(delta), edited_line)
            edited_line = re.sub("NO_OF_LEVELS", str(levels), edited_line)
            edited_line = re.sub("NO_OF_MIN", str(min_count), edited_line)
            dinfo.write(edited_line)

    if opsys != 'win':
        subprocess.call(path+f'/bin/{opsys}/disconnectionDPS', stdout=f)
    else:
        subprocess.call(path+'/bin/win/disconnectionDPS.exe', stdout=f)

    # Substitute the scale epsilon
    try:
        with open("tree.ps", "r") as tree:
            tree_lines = tree.readlines()
        with open("tree.ps", "w") as tree:
            for line in tree_lines:
                edited_line = re.sub("epsilon", str(delta), line)
                tree.write(edited_line)
    except (IOError):
      print("tree.ps does not exist")


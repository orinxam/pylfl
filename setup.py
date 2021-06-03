import setuptools
import platform
from glob import glob

# Determine the correct platform for binaries
system = platform.system()
#arch, _ = platform.architecture()
if system == 'Linux':
    GMIN = 'bin/linux/GMIN'
    OPTIM = 'bin/linux/OPTIM'
    PATHSAMPLE = 'bin/linux/PATHSAMPLE'
    disconnectionDPS = 'bin/linux/disconnectionDPS'
    os='linux'
if system == 'Windows':
    GMIN = 'bin/win/GMIN.exe'
    OPTIM = 'bin/win/OPTIM.exe'
    PATHSAMPLE = 'bin/win/PATHSAMPLE.exe'
    disconnectionDPS = 'bin/win/disconnectionDPS.exe'
    os='win'
if system == 'Darwin':
    GMIN = 'bin/mac/GMIN'
    OPTIM = 'bin/mac/OPTIM'
    PATHSAMPLE = 'bin/mac/PATHSAMPLE'
    disconnectionDPS = 'bin/mac/disconnectionDPS'
    os='mac'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylfl",
    version="0.1.4",
    author="Max Niroomand",
    author_email="mpn26@cam.ac.uk",
    description="A package to survey LFLs in ML models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/orinxam/pylfl",
    project_urls={
        "Bug Tracker": "https://github.com/orinxam/pylfl/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    data_files = [('bin',glob(f'{os}/*'))],
)




import setuptools
import platform


# Determine the correct platform for binaries
system = platform.system()
#arch, _ = platform.architecture()
if system == 'Linux':
    gmin = 'bin/linux/GMIN'
    optim = 'bin/linux/OPTIM'
    pathsample = 'bin/linux/PATHSAMPLE'
    disconnectionDPS = 'bin/linux/disconnectionDPS'
if system == 'Windows':
    gmin = 'bin/win/GMIN'
    optim = 'bin/win/OPTIM'
    pathsample = 'bin/win/PATHSAMPLE'
    disconnectionDPS = 'bin/win/disconnectionDPS'
if system == 'Darwin':
    gmin = 'bin/mac/GMIN'
    optim = 'bin/mac/OPTIM'
    pathsample = 'bin/mac/PATHSAMPLE'
    disconnectionDPS = 'bin/mac/disconnectionDPS'

print(gmin)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pylfl",
    version="0.1.0",
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
    data_files = [('bin', [gmin,optim,pathsample,disconnectionDPS])],
)




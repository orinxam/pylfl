import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="pylfl",
    version="0.2.5",
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
    #data_files = [('bin',glob(f'{os}/*'))],
    #data_files = [('bin', [GMIN,OPTIM,PATHSAMPLE,disconnectionDPS])],
    include_package_data=True,
    #package_data={"pylfl":[f'bin/{os}/*']},
    #scripts=[GMIN],#,OPTIM,PATHSAMPLE,disconnectionDPS],
    #data_files=[('bin/mac',['GMIN'])], #,'OPTIM','PATHSAMPLE','disconnectionDPS'])],
)




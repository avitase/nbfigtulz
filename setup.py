from os import path

from setuptools import setup, find_packages

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="nbfigtulz",
    version="0.5",
    description="Collection of tools to generate and display visualizations in JupyterLab",
    url="https://github.com/avitase/nbfigtulz",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Nis Meinert",
    author_email="nis.meinert@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license_files=[
        "LICENSE.txt",
    ],
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "ipython",
        "Pillow",
    ],
    extras_require={
        "jupyterlab": [
            "jupyterlab",
        ]
    },
    setup_requires=[
        "pytest-runner",
    ],
    tests_require=["pytest"],
)

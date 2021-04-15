# nbfigtulz
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Documentation Status](https://readthedocs.org/projects/nbfigtulz/badge/?version=latest)](http://nbfigtulz.readthedocs.io/?badge=latest)
[![PyPI](https://img.shields.io/pypi/v/nbfigtulz)](https://pypi.org/project/nbfigtulz/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`nbfigtulz` is a small library to show and save visualizations made via [matplotlib](https://matplotlib.org/) with the aim to let the user conveniently render publication ready images by default while working in [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/). The main features of `nbfigtulz` are:
- Images are generated and stored in the [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics) and [PGF](https://en.wikipedia.org/wiki/Progressive_Graphics_File) format which lends itself perfectly for inclusion in [PDF/A-1b](https://de.wikipedia.org/wiki/PDF/A) documents.
- [PNGs](https://en.wikipedia.org/wiki/Portable_Network_Graphics) are saved [Base64](https://en.wikipedia.org/wiki/Base64) encoded within a notebook. This makes the notebook free-standing and one can send raw notebooks to fellow researchers without having to remember to include various additional files such as images. Note that **one does not have to re-run the notebook to display the images**.
- Users are encouraged to render small images with high-resolution. Ideally, these images can be included without rescaling into a document.

## Documentation
Find our documentation [here](https://nbfigtulz.readthedocs.io).

## Installation
`nbfigtulz` releases are available as wheel packages for macOS, Windows and Linux on [PyPI](https://pypi.org/project/nbfigtulz/).
Install it using pip:
```
python -m pip install -U pip
python -m pip install -U nbfigtulz
```

## Examples
In addition to our [documentation](https://nbfigtulz.readthedocs.io) we provide a short notebook with a few examples:
- [example/notebook.ipynb](https://github.com/avitase/nbfigtulz/blob/main/example/notebook.ipynb)

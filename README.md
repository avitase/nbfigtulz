# `nbfigtulz`
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`nbfigtulz` is a small library to show and save visualizations made via [matplotlib](https://matplotlib.org/) with the aim to let the user conveniently render publication ready images by default while working in [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/). The main features of `nbfigtulz` are:
- Images are generate and stored in the [PNG](https://en.wikipedia.org/wiki/Portable_Network_Graphics) and [PGF](https://en.wikipedia.org/wiki/Progressive_Graphics_File) format which lends itself perfectly for inclusion in [PDF/A-1b](https://de.wikipedia.org/wiki/PDF/A) documents.
- [PNGs](https://en.wikipedia.org/wiki/Portable_Network_Graphics) are saved [Base64](https://en.wikipedia.org/wiki/Base64) encoded within a notebook. This makes the notebook free-standing and one can send raw notebooks to colleagues without having to remember to include various additional files such as images. Note that no JavaScript is required and **one does not have to re-run the notebook to display the images**.
- Users are encouraged to render small images with high-resolution. Ideally, these images can be included without rescaling into a document.

We provide a short description of all features in a notebook:
- [example/notebook.html](example/notebook.html) or
- [example/notebook.ipynb](example/notebook.ipynb)

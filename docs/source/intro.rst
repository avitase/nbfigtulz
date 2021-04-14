Introduction
============

``nbfigtulz`` tries to be a lightweight annotation to your already existing routines to render and display images in JupyterLab:

.. code-block:: python
  :linenos:
  :emphasize-lines: 1, 5, 10

  import nbfigtulz as ftl
  import numpy as np
  import matplotlib.pyplot as plt

  @ftl.with_context
  def make_fig(x, *, file_name):
    fig, ax = plt.subplots()
    ax.plot(x, np.sin(x))

    return ftl.save_fig(fig, file_name)

  make_fig(np.linspace(0, 50, 500), file_name='test')

By annotating with :class:`nbfigtulz.figtools.with_context` ``make_fig`` is wrapped with a context manager that temporally overwrites, e.g., ``matplotlib.rcParams``.
This configuration is then used by :class:`nbfigtulz.figtools.save_fig` to save ``fig`` in the PNG and PGF format.
(Note that our annotation also temporally sets the backend to ``"pgf"``, i.e., calling ``make_fig`` without the annotation might only generate a PNG file.)
The return value of :class:`nbfigtulz.figtools.save_fig` is a :class:`nbfigtulz.thumbnail.Thumbnail` instance that is drawn to your notebook if its ``__repr__`` overload is called.
This thumbnail is clickable & downloadable, is inlined into the notebook and thus will be displayed without needing to re-run the notebook!

The implicitly used defaults such as the image size and resolution, or the root directory where the generated images are stored, can be changed globally in :class:`nbfigtulz.config.config`:

.. code-block:: python
  :linenos:

  ftl.config['img_dir'] = '/tmp/my_fancy_dump_location/'
  flt.config['dpi'] = 150

Note that ``nbfigtulz`` will not try to create the image directory! It is your obligation to do this before :class:`nbfigtulz.figtools.save_fig` is called for the first time.

If needed, thumbnails can be arranged in a grid by using :class:`nbfigtulz.figtools.img_grid`.
In the following example we generate 3 plots and arrange them in a 2x2 grid (the last cell is empty):

.. code-block:: python
  :linenos:

  x = np.linspace(0, 50, 500)
  ftl.grid([make_fig(x * i, f'test{i}') for i in range(1, 4)], n_columns=2)

Technically, :class:`nbfigtulz.figtools.img_grid` generates a table in HTML where each image stays separately clickable and downloadable.
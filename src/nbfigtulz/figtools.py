import enum
import functools
import io
import pathlib
from typing import Any, Callable, Dict, Optional, Tuple

import matplotlib as mpl
from IPython.display import HTML

from . import config as cfg
from . import thumbnail


class Size(enum.Enum):
    """Common image sizes.

    This is nothing but a convenient wrapper for the image sizes stored inside of :class:`nbfigtulz.config.config`.
    Possible values are :class:`Size.SMALL` and :class:`Size.LARGE`.
    """

    SMALL = 1
    """Refers to ``size_small`` in :class:`nbfigtulz.config.config`.
    """

    LARGE = 2
    """Refers to ``size_large`` in :class:`nbfigtulz.config.config`.
    """

    def get_size(self) -> Tuple[float, float]:
        """Returns the image size as a tuple of width and height.

        :return: The width and height as a tuple of floats in units of inches.
        """
        if self == Size.SMALL:
            return cfg["size_small"]
        if self == Size.LARGE:
            return cfg["size_large"]

        raise Exception("Unknown size")


class FigContext:
    """Context manager that temporally overwrites ``matplotlib.rcParams`` and the backend.

    :param backend: The new backend, defaults to ``"pgf"``.
    :param rcParams: The temporal ``rcParams``, defaults to ``lualatex`` for ``pgf.texsystem``.
    """

    def __init__(
        self, backend: str = "", rcParams: Optional[Dict[str, Any]] = None
    ) -> None:
        self.backend = backend if backend else "pgf"
        self.old_backend = mpl.get_backend()

        self.rcParams = {
            "font.family": "serif",
            "text.usetex": True,
            "pgf.texsystem": "lualatex",
            "pgf.rcfonts": False,
        }

        if rcParams:
            for k in rcParams:
                self.rcParams[k] = rcParams[k]

        self.old_rcParams = {k: mpl.rcParams[k] for k in self.rcParams}

    def __enter__(self):
        mpl.use(self.backend)
        for k in self.rcParams:
            mpl.rcParams[k] = self.rcParams[k]

    def __exit__(self, exc, *args, **kwargs) -> bool:
        mpl.use(self.old_backend)
        for k in self.rcParams:
            mpl.rcParams[k] = self.old_rcParams[k]

        return exc is None


def with_context(func: Callable) -> Callable:
    """Wraps a function call inside the :class:`FigContext` context.

    :param func: A function.
    :return: The wrapped function.
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with FigContext():
            return func(*args, **kwargs)

    return wrapped


def save_fig(
    fig: Any,
    filename_base: str,
    resize: Any = Size.SMALL,
    suppress_pgf: bool = False,
    quiet: bool = False,
    thumbnail_scale: Optional[float] = None,
    **kwargs,
) -> thumbnail.Thumbnail:
    """The provided figure is stored to disk in the PNG and PGF (optional) format.

    :param fig: A ``matplotlib.pyplot.figure`` instance.
    :param filename_base: Base name (w/o file type suffix) of the PNG and PGF file.
    :param resize: If not ``None`` this will resize the figure. Pass anything with a ``get_size() -> Tuple[float, float]`` member function (e.g., :class:`Size`) or a tuple of two floats. Those floats are interpreted as the new width and height in units of inches, respectively.
    :param suppress_pgf: Suppress the generation of the PGF file.
    :param quiet: Do not print the FQNs of the generated files.
    :param thumbnail_scale: If not ``None`` this overwrites the default thumbnail scaling in :class:`nbfigtulz.config.config`.
    :param kwargs: Arguments passed to ``matplotlib.pyplot.savefig``.
    :return: The rendered PNG image.
    """
    if "dpi" not in kwargs:
        kwargs["dpi"] = cfg["dpi"]

    if resize:
        size = resize.get_size() if hasattr(resize, "get_size") else resize
        fig.set_size_inches(size)

    ftypes = [
        "png",
    ]
    if mpl.get_backend() == "pgf":
        if not suppress_pgf:
            ftypes.append("pgf")

        fig.tight_layout()

    for ftype in ftypes:
        filename = str(pathlib.Path(cfg["img_dir"]) / f"{filename_base}.{ftype}")
        fig.savefig(filename, **kwargs)

        if not quiet:
            print(filename)

    img_bytes = io.BytesIO()
    fig.savefig(img_bytes, format="png", **kwargs)
    img_bytes.seek(0)

    width, _ = fig.get_size_inches() * 100

    if not thumbnail_scale:
        thumbnail_scale = cfg["thumbnail_scale"]

    return thumbnail.Thumbnail(
        img_bytes.read(),
        filename_base,
        width=width,
        thumbnail_scale=thumbnail_scale,
        thumbnail_quality=cfg["thumbnail_quality"],
    )


def img_grid(
    images: Tuple[thumbnail.Thumbnail, ...],
    *,
    n_columns: int,
    width: Optional[int] = None,
) -> HTML:
    """Arranges images in a grid.

    :param images: List of images.
    :param n_columns: Number of columns.
    :param width: If not ``None`` the width of the grid in units of pixels.
    :return: The image grid.
    """
    cells = [img.to_html() if img else "" for img in images]

    n_rows = len(cells) // n_columns
    if n_rows * n_columns < len(cells):
        n_rows += 1

    rows = []
    for i in range(n_rows):
        start = i * n_columns
        end = start + n_columns
        row = [
            f'<td style="text-align:center">{cell}</td>' for cell in cells[start:end]
        ]
        rows.append("".join(row))

    body = "".join([f'<tr style="background-color: white">{row}</tr>' for row in rows])

    table_temp = "<table "
    if width:
        table_temp += f'style="width: {width}px"'
    table_temp += ">{body}</table>"

    return HTML(table_temp.format(body=body))

import enum
import functools
import io
import pathlib

import matplotlib as mpl
from IPython.display import HTML

from . import config as cfg
from . import image


class Size(enum.Enum):
    SMALL = 1
    LARGE = 2

    def get_size(self):
        if self == Size.SMALL:
            return cfg["size_small"]
        if self == Size.LARGE:
            return cfg["size_large"]

        raise Exception("Unknown size")


class FigContext:
    def __init__(self, backend="", rcParams=None):
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

    def __exit__(self, *args):
        mpl.use(self.old_backend)
        for k in self.rcParams:
            mpl.rcParams[k] = self.old_rcParams[k]


def with_context(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        with FigContext():
            return func(*args, **kwargs)

    return wrapped


def save_fig(
    fig, filename_base, resize=Size.SMALL, suppress_pgf=False, quiet=False, **kwargs
):
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
    return image.PNGImage(img_bytes.read(), filename_base, width=width)


def img_grid(images, *, n_columns, width=None):
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

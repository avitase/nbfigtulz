from typing import Any, Dict

config: Dict[str, Any] = {
    "img_dir": "img",
    "size_small": (4.0, 3.0),
    "size_large": (8.0, 6.0),
    "dpi": 300,
    "thumbnail_scale": 0.5,
    "thumbnail_quality": 42,
}
"""Configuration used in :class:`nbfigtulz.figtools.save_fig`.

- ``img_dir``: The directory where the generated images are stored. This directory is not created by ``nbfigtulz`` and has to exist before :class:`nbfigtulz.figtools.save_fig` is called for the first time.
- ``size_small``: Default width and height of small images in units of inches.
- ``size_large``: Default width and height of large images in units of inches.
- ``dpi``: DPI used to store images.
- ``thumbnail_scale``: The thumbnail can be scaled w.r.t. the generated PNG to save space. Setting the scale to, e.g., 0.5 shrinks the PNG by a factor of 2.
- ``thumbnail_quality``: The image quality of the thumbnail, on a scale from 1 (worst) to 95 (best). 
"""

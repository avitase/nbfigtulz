import base64
from typing import Any, Optional

from IPython.display import display, HTML


class PNGImage:
    """Wrapper for a PNG image.

    :param bytes: Bytes of the PNG image.
    :param file_name: The file name.
    :param width: If not ``None`` the image is rescaled to the given width in units of pixels.
    """

    def __init__(self, bytes: Any, file_name: str, width: Optional[int] = None):
        self.b64encoded = base64.b64encode(bytes).decode("ascii")
        self.file_name = file_name
        self.width = width

    def to_html(self, link: bool = True) -> str:
        """Renders the image into an HTML image tag.

        :param link: Whether or not to make the image tag a downloadable file link.
        :return: An HTML image tag.
        """
        img = "<img "
        if self.width:
            img += f"width={self.width} "
        img += f'src="data:image/png;base64, {self.b64encoded}" />'

        if not link:
            return img

        link_temp = (
            f'<a download="{self.file_name}.png" '
            + f'href="data:image/png;base64, {self.b64encoded}">'
            + "{body}</a>"
        )
        return link_temp.format(body=img)

    def __repr__(self):
        display(HTML(self.to_html(link=True)))
        return self.file_name + ".png"

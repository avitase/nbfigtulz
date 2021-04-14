import base64
import io
from typing import Any, Optional

from IPython.display import display, HTML
from PIL import Image


class Thumbnail:
    """Wrapper for a PNG image.

    :param bytes: Bytes of the PNG image.
    :param file_name: The file name.
    :param thumbnail_scale: Scaling factor for thumbnail.
    :param thumbnail_quality: Image quality of the thumbnail.
    :param width: If not ``None`` the image is rescaled to the given width in units of pixels.
    :param print_compression: Print the compression rate of the thumbnail w.r.t. the PNG.
    """

    def __init__(
        self,
        bytes: Any,
        file_name: str,
        thumbnail_scale: float,
        thumbnail_quality: int,
        width: Optional[int] = None,
        print_compression: bool = False,
    ):
        self.b64encoded = Thumbnail._bytes_to_decoded_b64(bytes)
        self.file_name = file_name
        self.width = width

        png = Image.open(io.BytesIO(bytes))
        w, h = png.size
        size = int(w * thumbnail_scale), int(h * thumbnail_scale)

        quality = int(thumbnail_quality)
        if quality < 1:
            quality = 1
        elif quality > 95:
            quality = 95

        buffer = io.BytesIO()
        png.resize(size).convert("RGB").save(
            buffer, format="JPEG", optimize=True, quality=quality
        )
        self.thumbnail = Thumbnail._bytes_to_decoded_b64(buffer.getvalue())

        if print_compression:
            rate = len(self.b64encoded) / len(self.thumbnail)
            print(f"Compression rate: {rate:.1f}")

    @staticmethod
    def _bytes_to_decoded_b64(bytes):
        return base64.b64encode(bytes).decode("ascii")

    def to_html(self, link: bool = True) -> str:
        """Renders the image into an HTML image tag.

        :param link: Whether or not to make the image tag a downloadable file link.
        :return: An HTML image tag.
        """
        img = "<img "
        if self.width:
            img += f"width={self.width} "
        img += f'src="data:image/jpeg;base64, {self.thumbnail}" />'

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

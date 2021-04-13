import base64

from IPython.display import display, HTML


class PNGImage:
    def __init__(self, bytes, file_name, width=None):
        self.b64encoded = base64.b64encode(bytes).decode("ascii")
        self.file_name = file_name
        self.width = width

    def to_html(self, link=True):
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

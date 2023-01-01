from typing import Tuple
from PIL import Image, ImageColor
from pathlib import Path


class Pycture():
    def __init__(self, path: Path, tdir: Path = "resized") -> None:
        self.tdir: Path = path.parent / tdir
        if not tdir.exists():
            tdir.mkdir()

        self.img = Image.open(path)
        self.path = path

    def resize(self, size: Tuple) -> None:
        width, height = size

        self.img.resize((width, height)).save(self.tdir / path.name)

    def crop(self, box: Tuple) -> None:
        left, top, right, bottom = box

        self.img.crop((left, top, right, bottom)).save(self.tdir / path.name)


path = Path(
    "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop")

# tdir = "resized"

# for images in path.glob("*.*"):
#     Pycture(images, tdir).crop((50, 50, 50, 50))

img = Image.open(next(path.glob("*.*")))
print(img.size)

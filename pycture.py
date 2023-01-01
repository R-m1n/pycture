from typing import Tuple
from PIL import Image, ImageColor
from pathlib import Path


def resize(path: Path, size: Tuple) -> None:
    img = Image.open(path)
    width, height = size

    img.resize((width, height)).save(tdir / path.name)


def crop(path: Path, box: Tuple) -> None:
    img = Image.open(path)
    left, top, right, bottom = box

    img.crop((left, top, right, bottom)).save(tdir / path.name)


parent_path = Path(
    "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop")

tdir: Path = parent_path / "resized"
if not tdir.exists():
    tdir.mkdir()

for images in parent_path.glob("*.*"):
    crop(images, (20, 20, 100, 100))

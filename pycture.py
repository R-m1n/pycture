import sys
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


def overlay(path: Path, rgba: Tuple) -> None:
    img = Image.open(path)
    red, green, blue, alpha = rgba
    width, height = img.size[0], img.size[1]

    for x in range(1, width):
        for y in range(1, height):
            img.putpixel((x, y), (red, green, blue, alpha))

    img.save(tdir / path.name)


def remove_bg(path: Path) -> None:
    img = Image.open(path)
    width, height = img.size[0], img.size[1]

    for x in range(1, width):
        for y in range(1, height):
            img.getpixel((x, y))

    img.save(tdir / path.name)


if __name__ == "__main__":
    path = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop/photo_2022-11-27_11-36-02.jpg")

    tdir = Path("resized")

    tdir = path.parent / tdir
    if not tdir.exists():
        tdir.mkdir()

    if path.is_dir():
        for images in path.glob("*.*"):
            overlay(images, (211, 211, 211, 50))

    else:
        overlay(path, (211, 211, 211, 50))

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
    img = Image.open(path).convert("RGBA")
    red, green, blue, alpha = rgba
    width, height = img.size[0], img.size[1]

    for x in range(1, width):
        for y in range(1, height):
            img.putpixel((x, y), (red, green, blue, alpha))

    img.save(tdir / path.name)


def remove_bg(path: Path) -> None:
    img = Image.open(path).convert("RGBA")
    width, height = img.size[0], img.size[1]

    colors = dict()
    for x in range(1, width):
        for y in range(1, height):
            if img.getpixel((x, y)) not in colors:
                colors[img.getpixel((x, y))] = 0

            else:
                colors[img.getpixel((x, y))] += 1

    bg_color = sorted(
        colors.items(), key=lambda item: item[0], reverse=True)[0][0]

    for x in range(1, width):
        for y in range(1, height):
            if img.getpixel((x, y)) == bg_color:
                img.putpixel((x, y), (0))

    img.save(tdir / path.name.replace(path.suffix, ".png"))


if __name__ == "__main__":
    path = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop/photo_2022-11-27_11-32-46.jpg")

    tdir = Path("resized")

    tdir = path.parent / tdir
    if not tdir.exists():
        tdir.mkdir()

    if path.is_dir():
        for images in path.glob("*.*"):
            remove_bg(images)

    else:
        remove_bg(path)

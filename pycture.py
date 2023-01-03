from argparse import ArgumentParser
import sys
from typing import Tuple
from PIL import Image, ImageColor
from pathlib import Path


def resize(img: Image.Image, size: Tuple) -> Image.Image:
    width, height = size

    return img.resize((width, height))


def crop(img: Image.Image, box: Tuple) -> Image.Image:
    left, top, right, bottom = box

    return img.crop((left, top, right, bottom))


def overlay(img: Image.Image, rgba: Tuple) -> Image.Image:
    overlay = Image.new("RGBA", img.size, rgba)

    img.paste(overlay, mask=overlay)
    return img


def remove_bg(img: Image.Image) -> Image.Image:
    bg_color = img.getpixel((0, 0))

    return replace_color(img, bg_color, (0))


def replace_color(img: Image.Image, old: Tuple, new: Tuple) -> Image.Image:  # needs conversion
    width, height = img.size[0], img.size[1]

    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) == old:
                img.putpixel((x, y), new)

    return img


def watermark(img: Image.Image, logo: Image.Image, position: str = None) -> Image.Image:  # needs conversion
    position = getCoordinates(position, img, logo)

    img.paste(logo, position, logo)
    return img


def getCoordinates(position: str, img: Image.Image, logo: Image.Image) -> Tuple:
    if isinstance(position, str):
        position = position.lower()

    width, height = img.size[0], img.size[1]
    logo_width, logo_height = logo.size[0], logo.size[1]

    if position == "top left" or position == "tl":
        return (0, 0)

    elif position == "top" or position == "t":
        return (width // 2 - (logo_width // 2), 0)

    elif position == "top right" or position == "tr":
        return (width - logo_width, 0)

    elif position == "center left" or position == "cl":
        return (0, height // 2 - (logo_height // 2))

    elif position == "center" or position == "c":
        return (width // 2 - (logo_width // 2), height // 2 - (logo_height // 2))

    elif position == "center right" or position == "cr":
        return (width - logo_width, height // 2 - (logo_height // 2))

    elif position == "bottom left" or position == "bl":
        return (0, height - logo_height)

    elif position == "bottom" or position == "b":
        return (width // 2 - (logo_width // 2), height - logo_height)

    else:
        return (width - logo_width, height - logo_height)


if __name__ == "__main__":
    path = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop")

    logo = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop/photo_2022-11-27_11-36-02.jpg")

    tdir = Path("resized")

    tdir = path / tdir
    if not tdir.exists():
        tdir.mkdir()

    images = []
    if path.is_dir():
        for image in path.glob("*.*"):
            images.append(image)

    else:
        images.append(path)

    parser = ArgumentParser(
        prog="Pycture",
        description="Simple Image Manipulation Tools.",
        epilog="\"Aesthetics is subjective\", is it??")

    parser.add_argument("path", help="path of the to be manipulated image")
    parser.add_argument("-r", "--resize")

    # function implementation
    logo = Image.open(logo)

    if logo.format != "png":
        logo = logo.convert("RGBA")

    logo = remove_bg(resize(logo, (300, 300)))

    for image in images:
        watermark(Image.open(image), logo).save(tdir / image.name)

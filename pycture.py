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
    img = img.convert("RGBA")
    width, height = img.size[0], img.size[1]
    bg_color = img.getpixel((0, 0))

    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) == bg_color:
                img.putpixel((x, y), (0))

    return img


def watermark(img: Image.Image, logo: Image.Image, logo_box: Tuple) -> Image.Image:
    width, height = img.size[0], img.size[1]

    logo = remove_bg(resize(logo, logo_box))
    logo_width, logo_height = logo.size[0], logo.size[1]
    paste_position = (width - logo_width, height - logo_height)

    img.paste(logo, paste_position, logo)
    return img


if __name__ == "__main__":
    path = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop")

    logo = Path(
        "/home/armin/Repository/Businesses/Web Business/Clients/Silk Flower International/Desktop/photo_2022-11-27_11-33-36.jpg")

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

    for image in images:
        watermark(Image.open(image), Image.open(logo),
                  (300, 300)).save(tdir / image.name)

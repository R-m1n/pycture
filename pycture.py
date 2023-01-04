from argparse import ArgumentParser
from time import sleep
from typing import Iterable, Tuple
from PIL import Image
from pathlib import Path

from tqdm import trange


def resize(img: Image.Image, size: Iterable) -> Image.Image:
    width, height = size

    return img.resize((width, height))


def crop(img: Image.Image, box: Iterable) -> Image.Image:
    left, top, right, bottom = box

    return img.crop((left, top, right, bottom))


def overlay(img: Image.Image, rgba: Iterable) -> Image.Image:
    overlay = Image.new("RGBA", img.size, rgba)

    img.paste(overlay, mask=overlay)

    return img


def remove_bg(img: Image.Image) -> Image.Image:
    bg_color = img.getpixel((0, 0))

    return replace_color(img, bg_color, (0))


def replace_color(img: Image.Image, old: Iterable, new: Iterable) -> Image.Image:
    width, height = img.size[0], img.size[1]

    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) == old:
                img.putpixel((x, y), new)

    return img


def watermark(img: Image.Image, logo: Image.Image, position: str = None) -> Image.Image:
    position = getCoordinates(position, img, logo)

    img.paste(logo, position, logo)

    return img


def getCoordinates(position: str, img: Image.Image, logo: Image.Image) -> Tuple:
    if isinstance(position, str):
        position = position.lower()

    width, height = img.size[0], img.size[1]
    logo_width, logo_height = logo.size[0], logo.size[1]

    if position == "top-left" or position == "tl":
        return (0, 0)

    elif position == "top" or position == "t":
        return (width // 2 - (logo_width // 2), 0)

    elif position == "top-right" or position == "tr":
        return (width - logo_width, 0)

    elif position == "center-left" or position == "cl":
        return (0, height // 2 - (logo_height // 2))

    elif position == "center" or position == "c":
        return (width // 2 - (logo_width // 2), height // 2 - (logo_height // 2))

    elif position == "center-right" or position == "cr":
        return (width - logo_width, height // 2 - (logo_height // 2))

    elif position == "bottom-left" or position == "bl":
        return (0, height - logo_height)

    elif position == "bottom" or position == "b":
        return (width // 2 - (logo_width // 2), height - logo_height)

    else:
        return (width - logo_width, height - logo_height)


def getArgs():
    parser = ArgumentParser(
        prog="Pycture",
        description="Simple Image Manipulation Tools.",
        epilog="\"Aesthetics is subjective\", is it??")

    parser.add_argument("path",
                        help="path of the image(s)")

    parser.add_argument("-r", "--resize", nargs=2, metavar=("width", "height"),
                        help="resize the image(s) to the given size %(metavar)s")

    parser.add_argument("-c", "--crop", nargs=4, metavar=("left", "top", "right", "bottom"),
                        help="crop a given box on the image(s) %(metavar)s")

    parser.add_argument("-o", "--overlay", nargs=4, metavar=("red", "green", "blue", "alpha"),
                        help="adds an overlay %(metavar)s on the image(s)")

    parser.add_argument("-rb", "--remove-background", action="store_true",
                        help="removes the background of the image(s)")

    parser.add_argument("-rc", "--replace-color", nargs=8, metavar=("red", "green", "blue", "alpha", "red", "green", "blue", "alpha"),
                        help="replaces given color on the image(s) with a new color")

    parser.add_argument("-wm", "--watermark", nargs=2, metavar=("logo", "position"),
                        help="watermarks the image(s) with a logo at a given position")

    return parser.parse_args()


def pbar(length, desc, filename):
    for img in trange(length, desc=desc + " " + filename, colour="#84ceeb"):
        sleep(.006)


if __name__ == "__main__":
    args = getArgs()
    path = Path(args.path)

    tdir = path / Path("pycture")
    if not tdir.exists():
        tdir.mkdir()

    images = []
    if path.is_dir():
        for image in path.glob("*.*"):
            images.append(image)

    else:
        images.append(path)

    if args.resize:
        for image in images:
            pbar(100, "Resizing", image.name)
            resize(Image.open(image),
                   map(lambda arg: int(arg), args.resize)).save(tdir / image.name)

    elif args.crop:
        for image in images:
            pbar(100, "Croping", image.name)
            crop(Image.open(image),
                 map(lambda arg: int(arg), args.crop)).save(tdir / image.name)

    elif args.overlay:
        for image in images:
            pbar(100, "Overlaying", image.name)
            overlay(Image.open(image),
                    tuple(map(lambda arg: int(arg), args.overlay))).save(tdir / image.name)

    elif args.remove_background:
        for image in images:
            filename = image.name.replace(Path(image.name).suffix, ".png")

            pbar(100, "Removing Background", image.name)
            remove_bg(Image.open(image)
                      .convert("RGBA")).save(tdir / filename)

    elif args.replace_color:
        for image in images:
            oldColor = tuple(map(lambda arg: int(arg), args.overlay))[:4]
            newColor = tuple(map(lambda arg: int(arg), args.overlay))[4:]

            pbar(100, "Replacing Color", image.name)
            replace_color(Image.open(image),
                          oldColor,
                          newColor).save(tdir / image.name)

    elif args.watermark:
        logo, position = args.watermark[0], args.watermark[1]
        logo = Image.open(Path(logo))

        if logo.format != "png":
            logo = logo.convert("RGBA")

        # logo = remove_bg(resize(logo, (300, 300)))

        for image in images:
            filename = image.name.replace(Path(image.name).suffix, ".png")

            pbar(100, "Watermarking", image.name)
            watermark(Image.open(image),
                      logo,
                      position).save(tdir / filename)

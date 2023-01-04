import os
from argparse import ArgumentParser, Namespace
from time import sleep
from typing import Iterable, List
from PIL import Image
from pathlib import Path
from tqdm import trange


"""
    A Simple Image Manipulating Script.

    Pycture is a simple script intended to automate easy, yet time consuming image related chores,
    namely watermarking, background removal, format conversion, ... .


    Functions
    ---------
    resize(image, size)
        Return a resized version of the input image according to the input size = (width, height).

    crop(image, box)
        Return a cropped version of the input image with respect to the input box = (left, top, right, bottom).

    overlay(image, rbga)
        Return an overlayed version of the input image according to the input RGBA value.

    remove_bg(image)
        Return an image with removed background.

    replace_color(image, old, new)
        Return an image with pixels containing the old RGBA value in the image replaced with pixels containing the new RGBA value.

    watermark(image, logo, position)
        Return an image with a watermark at the designated position.
"""


def resize(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """
        Return a resized version of the input image according to the input size = (width, height).

        Parameters
        ----------
        image: Image

        size: tuple[int, int]
    """

    return image.resize(size)


def crop(image: Image.Image, box: tuple[int, int, int, int]) -> Image.Image:
    """
        Return a cropped version of the input image with respect to the input box = (left, top, right, bottom).

        Parameters
        ----------
        image: Image

        box: tuple[int, int, int, int]
    """

    return image.crop(box)


def overlay(image: Image.Image, rgba: tuple[int, int, int, int]) -> Image.Image:
    """
        Return an overlayed version of the input image according to the input RGBA value.

        Parameters
        ----------
        image: Image

        rgba: tuple[int, int, int, int]
    """

    overlay = Image.new("RGBA", image.size, rgba)

    image.paste(overlay, mask=overlay)

    return image


def remove_bg(image: Image.Image) -> Image.Image:
    """
        Return an image with removed background.

        Parameters
        ----------
        image: Image
    """

    bg_color = image.getpixel((0, 0))

    return replace_color(image, bg_color, (0))


def replace_color(image: Image.Image, old: tuple[int, int, int, int], new: tuple[int, int, int, int]) -> Image.Image:
    """
        Return an image with pixels containing the old RGBA value in the image replaced with pixels containing the new RGBA value.

        Parameters
        ----------
        image: Image

        old: tuple[int, int, int, int]

        new: tuple[int, int, int, int]
    """

    width, height = image.size[0], image.size[1]

    for x in range(width):
        for y in range(height):
            if image.getpixel((x, y)) == old:
                image.putpixel((x, y), new)

    return image


def watermark(image: Image.Image, logo: Image.Image, position: str = None) -> Image.Image:
    """
        Return an image with a watermark at the designated position.

        Parameters
        ----------
        image: Image

        logo: Image

        position: str
    """

    position = _getCoordinates(position, image, logo)

    image.paste(logo, position, logo)

    return image


def _getSize(path: str) -> int:
    return os.stat(path).st_size // 1024


def _getCoordinates(position: str, image: Image.Image, logo: Image.Image) -> tuple[int, int]:
    if isinstance(position, str):
        position = position.lower()

    width, height = image.size[0], image.size[1]
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


def _getArgs() -> None:
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


def _pbar(length: int, desc: str, filename: str) -> None:
    for image_size in trange(length, desc=desc + " " + filename, colour="#84ceeb", unit="kB", ncols=100):
        sleep(.004)


def _getPaths(path: Path) -> List[Path]:
    if path.is_dir():
        for path in path.glob("*.*"):
            paths.append(path)

    else:
        paths.append(path)


def _switch(args: Namespace, path: Path) -> None:
    if args.resize:
        for path in paths:
            _pbar(_getSize(path), "Resizing", path.name)
            resize(Image.open(path),
                   map(lambda arg: int(arg), args.resize)).save(tdir / path.name)

    elif args.crop:
        for path in paths:
            _pbar(_getSize(path), "Croping", path.name)
            crop(Image.open(path),
                 map(lambda arg: int(arg), args.crop)).save(tdir / path.name)

    elif args.overlay:
        for path in paths:
            _pbar(_getSize(path), "Overlaying", path.name)
            overlay(Image.open(path),
                    tuple(map(lambda arg: int(arg), args.overlay))).save(tdir / path.name)

    elif args.remove_background:
        for path in paths:
            filename = path.name.replace(Path(path.name).suffix, ".png")

            _pbar(_getSize(path), "Removing Background", path.name)
            remove_bg(Image.open(path)
                      .convert("RGBA")).save(tdir / filename)

    elif args.replace_color:
        for path in paths:
            oldColor = tuple(map(lambda arg: int(arg), args.overlay))[:4]
            newColor = tuple(map(lambda arg: int(arg), args.overlay))[4:]

            _pbar(_getSize(path), "Replacing Color", path.name)
            replace_color(Image.open(path),
                          oldColor,
                          newColor).save(tdir / path.name)

    elif args.watermark:
        logo, position = args.watermark[0], args.watermark[1]
        logo = Image.open(Path(logo))

        if logo.format != "png":
            logo = logo.convert("RGBA")

        for path in paths:
            filename = path.name.replace(Path(path.name).suffix, ".png")

            _pbar(_getSize(path), "Watermarking", path.name)
            watermark(Image.open(path),
                      logo,
                      position).save(tdir / filename)


if __name__ == "__main__":
    args = _getArgs()

    path = Path(args.path)

    paths = _getPaths(path)

    tdir = path / Path("pycture")

    if not tdir.exists():
        tdir.mkdir()

    _switch(args, path)

    print(f"\nImages saved to: {tdir}")

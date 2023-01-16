from functools import cache
from pathlib import Path

from PIL import Image


def get_res_path() -> Path:
    return Path(__file__).parent.parent / 'res'


@cache
def load_image(image_path: Path) -> Image.Image:
    return Image.open(image_path)


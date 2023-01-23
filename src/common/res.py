from functools import cache
from pathlib import Path

from PIL import Image


def get_repo_dir() -> Path:
    return Path(__file__).parent.parent.parent


def get_res_path() -> Path:
    return get_repo_dir() / 'res'


def walkthrough_dir() -> Path:
    return get_repo_dir() / 'walkthrough'


@cache
def load_image(image_path: Path) -> Image.Image:
    return Image.open(image_path)


walkthrough_dir().mkdir(exist_ok=True)


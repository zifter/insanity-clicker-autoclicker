from pathlib import Path


def get_res_path() -> Path:
    return Path(__file__).parent.parent / 'res'

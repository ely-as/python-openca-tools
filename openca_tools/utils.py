import hashlib
from pathlib import Path
from typing import Union

CHUNK_SIZE: int = 4096


def create_checksum_sidecar_file(filepath: Path, hash_algorithm: str) -> None:
    checksum = compute_checksum(filepath, hash_algorithm)
    sidecar_filepath = (
        filepath.parent / (filepath.name + '.' + hash_algorithm.lower())
    )
    with open(sidecar_filepath, 'w') as file:
        file.write(f'{checksum}\n')


def compute_checksum(filepath: Union[Path, str], hash_algorithm: str) -> str:
    """Compute the checksum of a file.

    Supported hash algorithms depend on Python version:
    https://docs.python.org/3/library/hashlib.html#hash-algorithms
    """
    try:
        hash = getattr(hashlib, hash_algorithm.lower())()
    except AttributeError as exc:
        new_exc_msg = (
            f"Could not find hash algorithm '{hash_algorithm}'. Algorithms "
            "available: "
            + ", ".join(getattr(hashlib, 'algorithms_available', []))
        )
        raise ValueError(new_exc_msg) from exc
    with open(filepath, 'rb') as file:
        for chunk in iter(lambda: file.read(CHUNK_SIZE), b''):
            hash.update(chunk)
    return hash.hexdigest()

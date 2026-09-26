import os
from pathlib import Path

from fastapi import HTTPException


def safe_filename(filename: str) -> str:
    if not filename or filename.strip() == "":
        raise HTTPException(status_code=400, detail="Filename is required.")

    safe_name = os.path.basename(filename.strip())

    if safe_name in ("", ".", ".."):
        raise HTTPException(status_code=400, detail="Invalid filename.")

    if ".." in safe_name or "/" in safe_name or "\\" in safe_name:
        raise HTTPException(status_code=400, detail="Invalid filename.")

    return safe_name


def safe_path(base_dir: str, filename: str) -> Path:
    safe_name = safe_filename(filename)
    base = Path(base_dir).resolve()
    full_path = (base / safe_name).resolve()

    if not str(full_path).startswith(str(base)):
        raise HTTPException(status_code=400, detail="Invalid file path.")

    return full_path

from pathlib import Path
import subprocess


GENERATED_DIR = Path("generated")


def save_code(
    filename: str,
    code: str
):

    if not filename:

        raise ValueError(
            "Filename cannot be empty."
        )

    if not code:

        raise ValueError(
            "Code cannot be empty."
        )

    GENERATED_DIR.mkdir(
        exist_ok=True
    )

    file_path = GENERATED_DIR / filename

    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(code)

    return file_path


def run_python_file(
    filename: str
):

    file_path = GENERATED_DIR / filename

    if not file_path.exists():

        raise FileNotFoundError(
            f"{filename} not found."
        )

    result = subprocess.run(
        ["python", str(file_path)],
        capture_output=True,
        text=True,
        timeout=10
    )

    if result.returncode == 0:

        return result.stdout

    return result.stderr
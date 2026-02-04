import os
import sys
import warnings
from pathlib import Path
from rasterio.errors import NotGeoreferencedWarning


def suppress_warnings() -> None:
    """Suppress known non-critical warnings to keep notebooks readable."""
    warnings.filterwarnings("ignore", category=NotGeoreferencedWarning)


def find_repo_root(start: Path | None = None, max_up: int = 8) -> Path:
    """
    Find repository root by looking for expected folders.
    Assumes repo root contains both 'src' and 'notebooks'.
    """
    start = start or Path.cwd()
    p = start.resolve()
    for _ in range(max_up):
        if (p / "src").exists() and (p / "notebooks").exists():
            return p
        p = p.parent
    raise RuntimeError("Repository root not found (expected 'src' and 'notebooks' folders).")


def set_working_directory_to_repo_root() -> Path:
    """
    Set CWD to repo root and ensure it's on sys.path (so `import src...` works).
    Returns the repo root path.
    """
    root = find_repo_root()
    os.chdir(root)
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    return root

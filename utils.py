# add this helper once (top of file is fine)
from pathlib import Path
import sys

def resource_path(rel: str) -> str:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
    return str((base / rel).resolve())

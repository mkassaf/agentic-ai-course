#!/usr/bin/env python3
"""Execute practice notebooks in clean directories without changing published outputs."""
from pathlib import Path
import tempfile

import nbformat
from nbclient import NotebookClient

ROOT = Path(__file__).resolve().parents[1]


def main():
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(paths) != 8:
        raise SystemExit(f"Expected 8 notebooks, found {len(paths)}")
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        with tempfile.TemporaryDirectory(prefix="agentic-course-") as directory:
            NotebookClient(
                notebook,
                timeout=90,
                kernel_name="python3",
                resources={"metadata": {"path": directory}},
                allow_errors=False,
            ).execute()
        code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
        print(f"PASS {path.name}: {code_cells} code cells, isolated practice run", flush=True)
    print("All 8 notebooks executed. Live university API calls were not tested.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Execute practice notebooks in clean directories without changing published outputs."""
from pathlib import Path
import sys
import tempfile

import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]


def main():
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if len(paths) != 8:
        raise SystemExit(f"Expected 8 notebooks, found {len(paths)}")
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        with tempfile.TemporaryDirectory(prefix="agentic-course-") as directory:
            manager = KernelManager(kernel_name="python3")
            # Use the interpreter whose dependencies were installed for this check.
            manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
            executor = NotebookClient(
                notebook,
                timeout=90,
                kernel_name="python3",
                resources={"metadata": {"path": directory}},
                allow_errors=False,
                km=manager,
            )
            try:
                executor.execute()
            finally:
                if executor.kc is not None:
                    executor.kc.stop_channels()
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
        code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
        print(f"PASS {path.name}: {code_cells} code cells, isolated practice run", flush=True)
    print("All 8 notebooks executed. Live model API calls were not tested.")


if __name__ == "__main__":
    main()

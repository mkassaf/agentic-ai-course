#!/usr/bin/env python3
"""Compile all notebooks and execute model-free labs in isolated kernels."""
from pathlib import Path
import ast
import json
import sys
import tempfile

import nbformat
from IPython.core.interactiveshell import InteractiveShell
from nbclient import NotebookClient
from jupyter_client import KernelManager

ROOT = Path(__file__).resolve().parents[1]
MODEL_FREE = {"11_tools_mcp", "13_a2a_protocol", "16_learning_curve_trust"}


def main():
    expected = set(json.loads((ROOT / "course.json").read_text())["labs"])
    paths = sorted((ROOT / "notebooks").glob("*.ipynb"))
    if {path.stem for path in paths} != expected:
        raise SystemExit("Notebook filenames do not match the course sequence")
    shell = InteractiveShell.instance()
    for path in paths:
        notebook = nbformat.read(path, as_version=4)
        for i, cell in enumerate(notebook.cells):
            if cell.cell_type == "code":
                source = shell.input_transformer_manager.transform_cell(cell.source)
                compile(source, f"{path.name}:cell {i}", "exec", flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT)
        print(f"PASS {path.name}: code cells compile", flush=True)
        if path.stem not in MODEL_FREE:
            continue
        with tempfile.TemporaryDirectory(prefix="agentic-course-") as directory:
            manager = KernelManager(kernel_name="python3")
            manager.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
            executor = NotebookClient(notebook, timeout=90, kernel_name="python3",
                                      resources={"metadata": {"path": directory}}, allow_errors=False, km=manager)
            try:
                executor.execute()
            finally:
                if executor.kc is not None:
                    executor.kc.stop_channels()
                if manager.has_kernel:
                    manager.shutdown_kernel(now=True)
        print(f"PASS {path.name}: model-free execution", flush=True)
    print(f"All {len(paths)} notebooks compiled; {len(MODEL_FREE)} model-free labs executed. No provider calls were made.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build portable notebooks from small lesson sources and one shared model adapter."""
from pathlib import Path
import hashlib
import json
import textwrap

import nbformat

ROOT = Path(__file__).resolve().parents[1]

SETUP = '''\
# Run all examples without a key first. Change only MODE for a live model run.
MODE = "practice"  # "live" uses the API key supplied through Colab Secrets
BASE_URL = "https://freeinference.org/v1"
MODEL = "qwen3.6-35b"
SECRET_NAME = "FREEINFERENCE_API_KEY"

client = Client(mode=MODE, base_url=BASE_URL, model=MODEL,
                api_key=secret(SECRET_NAME) if MODE == "live" else "",
                max_calls=24, max_tokens=512)
print("Mode:", MODE)
'''


def source_cell(kind, source, hidden=False):
    source = textwrap.dedent(source).strip()
    cell = (nbformat.v4.new_markdown_cell(source) if kind == "markdown"
            else nbformat.v4.new_code_cell(source))
    if hidden:
        cell.metadata.update(collapsed=True, jupyter={"source_hidden": True},
                             colab={"cellView": "form"})
    return cell


def build(lesson, runtime):
    slug = lesson["slug"]
    number = slug.split("_", 1)[0]
    intro = f'''# Lab {number} · {lesson["title"]}

**Prepared by Mustafa Assaf** · Beginner level · 60–90 minute session

Start with the small worked example, read the expected output, then change one thing.
Use a CPU runtime and run the cells from top to bottom. No repository clone is needed.

**Practice mode:** model answers are explicitly scripted so you can inspect the code
without a key. They demonstrate control flow, not model quality. MCP, A2A and LangGraph
examples run their actual libraries locally even in practice mode; their setup cells
install pinned packages if needed.

**Optional live calls:** add `FREEINFERENCE_API_KEY` in Colab's Secrets panel, allow
this notebook access, and change `MODE` to `"live"`. The initial model is
`qwen3.6-35b` on FreeInference; `BASE_URL`, `MODEL` and `SECRET_NAME` can be changed
for another compatible provider. Keep the key out of cells and outputs.
'''
    cells = [source_cell("markdown", intro),
             source_cell("markdown", "### Shared setup\nThe next cell contains the reusable model client. Run it as supplied; the short teaching examples follow below."),
             source_cell("code", runtime, hidden=True), source_cell("code", SETUP)]
    for cell in lesson["cells"]:
        if cell["type"] not in ("markdown", "code"):
            raise ValueError(f"Unknown cell type in {slug}")
        cells.append(source_cell(cell["type"], cell["source"], cell.get("hidden", False)))
    cells.append(source_cell("markdown", "### Finish\nExplain the result in your own words. Make the small change suggested above and rerun its check. If you use a live model, save the actual result and trace; a different or failed response is something to investigate."))
    for index, cell in enumerate(cells):
        cell.id = hashlib.sha256(f"{slug}:{index}".encode()).hexdigest()[:12]
    notebook = nbformat.v4.new_notebook(cells=cells, metadata={
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
        "colab": {"name": slug + ".ipynb", "provenance": []},
        "authors": [{"name": "Mustafa Assaf"}],
    })
    nbformat.validate(notebook)
    nbformat.write(notebook, ROOT / "notebooks" / (slug + ".ipynb"))
    print(f"Built {slug}.ipynb")


def main():
    (ROOT / "notebooks").mkdir(exist_ok=True)
    config = json.loads((ROOT / "course.json").read_text())
    runtime = (ROOT / "coursekit/runtime.py").read_text()
    for slug in config["labs"]:
        lesson = json.loads((ROOT / "lessons" / (slug + ".json")).read_text())
        if lesson["slug"] != slug:
            raise ValueError(f"Lesson/file slug mismatch: {slug}")
        build(lesson, runtime)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build the lab notebooks; reusable implementation belongs in the course package."""
from pathlib import Path
import hashlib
import json
import re
import textwrap

import nbformat

ROOT = Path(__file__).resolve().parents[1]
EXTRAS = {
    "02_rag_systems": ("rag", "chromadb"),
    "06_human_feedback_memory": ("rag", "chromadb"),
    "09_tools_mcp": ("mcp", "mcp"),
    "11_a2a_protocol": ("a2a", "a2a"),
    "12_frameworks_langgraph": ("framework", "langgraph"),
}
NO_MODEL_LABS = {"09_tools_mcp"}  # these labs never call ask()


def source_cell(kind, source):
    source = textwrap.dedent(source).strip()
    return (nbformat.v4.new_markdown_cell(source) if kind == "markdown"
            else nbformat.v4.new_code_cell(source))


def setup_for(slug, revision):
    extra, module = EXTRAS.get(slug, ("", ""))
    package = "agentic-ai-coursekit" + (f"[{extra}]" if extra else "")
    url = f"https://github.com/mkassaf/agentic-ai-course/archive/{revision}.zip"
    modules = ["coursekit"] + ([module] if module else [])
    source = ("from importlib.util import find_spec\n"
              f"if not all(find_spec(name) for name in {modules!r}):\n"
              f'    %pip install -q "{package} @ {url}"')
    if slug not in NO_MODEL_LABS:
        source += '\nfrom coursekit import make_ask\nMODE = "practice"\nask = make_ask(mode=MODE)'
    return source


def build(lesson, revision):
    slug = lesson["slug"]
    number = slug.split("_", 1)[0]
    intro = (f'# Lab {number} · {lesson["title"]}\n\n'
             f'**Prepared by Mustafa Assaf** · {lesson["section"]} · 15–20 minute lab')
    setup_note = '## Setup\nRun this cell once to load the course helpers, then run the steps below in order.'
    if slug not in NO_MODEL_LABS:
        setup_note += (' Practice answers are scripted. For a live model, save '
                       '`FREEINFERENCE_API_KEY` in Colab Secrets and change `MODE` to `"live"`. '
                       '`ask` stops after 12 calls; run this cell again to reset the count.')
    else:
        setup_note += ' This lab needs no model key.'
    # The lesson's first cell states the idea, so learners read it before the setup boilerplate.
    overview, *steps = lesson["cells"]
    if overview["type"] != "markdown":
        raise ValueError(f"{slug}: the first lesson cell must be a markdown overview")
    cells = [source_cell("markdown", intro), source_cell("markdown", overview["source"]),
             source_cell("markdown", setup_note), source_cell("code", setup_for(slug, revision))]
    cells[-1].metadata["tags"] = ["setup"]
    for cell in steps:
        if cell["type"] not in ("markdown", "code"):
            raise ValueError(f"Unknown cell type in {slug}")
        cells.append(source_cell(cell["type"], cell["source"]))
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
    revision = (ROOT / "coursekit-ref.txt").read_text().strip()
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("coursekit-ref.txt must contain a published commit SHA")
    for slug in config["labs"]:
        lesson = json.loads((ROOT / "lessons" / (slug + ".json")).read_text())
        if lesson["slug"] != slug:
            raise ValueError(f"Lesson/file slug mismatch: {slug}")
        build(lesson, revision)


if __name__ == "__main__":
    main()

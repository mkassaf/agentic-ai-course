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
    "07_observe_trace_swap": ("framework", "langsmith"),  # langgraph brings the LangSmith SDK
    "08_human_feedback_memory": ("rag", "chromadb"),
    "11_tools_mcp": ("mcp", "mcp"),
    "13_a2a_protocol": ("a2a", "a2a"),
    "14_frameworks_langgraph": ("framework", "langgraph"),
}
# Labs that install their SDK straight from PyPI (publish-independent), not as a coursekit extra.
# Lab 17 uses no coursekit helper, so it installs typesafe-sdk directly from PyPI.
DIRECT_SDKS = {
    "17_weighted_decision_jev": ("typesafe_sdk", "typesafe-sdk==0.7.2"),
}
NO_MODEL_LABS = {"11_tools_mcp", "16_learning_curve_trust", "17_weighted_decision_jev"}  # these labs never call ask()
# Diagrams are exported by scripts/export_diagrams.js and served by the course site (GitHub Pages).
DIAGRAM_URL = "https://mkassaf.github.io/agentic-ai-course/assets/diagrams/{number}.svg"


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
    direct_sdk = DIRECT_SDKS.get(slug)
    if direct_sdk:
        module, pip_spec = direct_sdk
        source += (f"\nif not find_spec({module!r}):\n"
                   f"    %pip install -q {pip_spec!r}")
    if slug not in NO_MODEL_LABS:
        source += ('\nfrom coursekit import make_ask\nMODE = "practice"\n'
                   'PROVIDER = "freeinference"  # or "gemini" or "deepseek"\n'
                   'ask = make_ask(mode=MODE, provider=PROVIDER)')
    return source


def build(lesson, revision, diagrams, site_lab):
    slug = lesson["slug"]
    number = slug.split("_", 1)[0]
    intro = (f'# Lab {number} · {lesson["title"]}\n\n'
             f'**Prepared by Mustafa Assaf** · {lesson["section"]} · 15–20 minute lab')
    setup_note = '## Setup\nRun this cell once to load the course helpers, then run the steps below in order.'
    if slug not in NO_MODEL_LABS:
        setup_note += (' Practice answers are scripted. For a live model, choose `PROVIDER` '
                       '(`"freeinference"`, `"gemini"`, or `"deepseek"`), save its key in Colab Secrets '
                       '(`FREEINFERENCE_API_KEY`, `GEMINI_API_KEY`, or `DEEPSEEK_API_KEY`), and change `MODE` to '
                       '`"live"`. `ask` stops after 12 calls; run this cell again to reset the count.')
    else:
        setup_note += ' This lab needs no model key.'
    # The lesson's first cell states the idea, so learners read it before the setup boilerplate.
    overview, *steps = lesson["cells"]
    if overview["type"] != "markdown":
        raise ValueError(f"{slug}: the first lesson cell must be a markdown overview")
    patterns = []  # field-guide pattern cards follow the overview, before the setup
    while steps and steps[0]["type"] == "markdown" and steps[0]["source"].startswith("## Pattern · "):
        patterns.append(source_cell("markdown", steps.pop(0)["source"]))
    alt = diagrams[number].replace("[", "(").replace("]", ")")
    picture = f'\n\n**At a glance**\n\n![Lab {number} at a glance: {alt}]({DIAGRAM_URL.format(number=number)})'
    # The background and key terms are shared with the course site (assets/course.js).
    terms = "\n".join(f"| **{term}** | {meaning} |" for term, meaning in site_lab["terms"])
    context = ("## The idea in context\n\n" + "\n\n".join(site_lab["background"])
               + f"\n\n| Key term | Meaning |\n| --- | --- |\n{terms}")
    cells = [source_cell("markdown", intro), source_cell("markdown", overview["source"] + picture),
             source_cell("markdown", context), *patterns,
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
    diagrams = json.loads((ROOT / "assets" / "diagrams" / "descriptions.json").read_text())
    site = (ROOT / "assets" / "course.js").read_text()
    site_labs = {lab["file"]: lab for lab in json.loads(re.search(r"const labs = (\[.*?\n\]);", site, re.S)[1])}
    for slug in config["labs"]:
        lesson = json.loads((ROOT / "lessons" / (slug + ".json")).read_text())
        if lesson["slug"] != slug:
            raise ValueError(f"Lesson/file slug mismatch: {slug}")
        build(lesson, revision, diagrams, site_labs[slug])


if __name__ == "__main__":
    main()

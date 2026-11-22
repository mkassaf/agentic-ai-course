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
NO_MODEL_LABS = {"11_tools_mcp", "13_a2a_protocol", "16_learning_curve_trust", "17_weighted_decision_jev"}  # these labs never call ask()
# Diagrams are exported by scripts/export_diagrams.js and served by the course site (GitHub Pages).
DIAGRAM_URL = "https://mkassaf.github.io/agentic-ai-course/assets/diagrams/{number}.svg"
DECKS = {
    "microservices": ("Microservices & Their Patterns", 53),
    "ddd": ("Microservices Lecture 2 - Condensed DDD", 92),
}


EXAMPLE_CONTEXT = {
    "00": "A retry repeats a failed request; a timeout can leave the result uncertain. Bulkheads separate resources, an API gateway handles shared edge concerns, and a BFF adapts an API to a client.",
    "01": "An API gateway can route requests and apply common policies. A backend for frontend (BFF) can tailor an API to one client, such as a mobile app. A system may use both.",
    "02": "API composition asks services for data and joins their responses. CQRS maintains a separate read model for queries, which can lag behind writes. A citation identifies a source; it does not prove the answer follows from it.",
    "03": "A technical-layer split places UI, business logic, and data access in different services. A bounded context defines where one business model and language apply; its deployment boundary still needs review.",
    "04": "An Order has a stable identity and contains order lines. Its root is responsible for keeping the total equal to the sum of its lines. Money is compared by amount and currency.",
    "05": "A slow dependency can occupy callers while they wait. Retrying adds more requests. A repeated card charge can have a second financial effect when the operation is not idempotent.",
    "06": "ShopEasy support needs to search orders, payments, and deliveries by customer name. API composition joins responses; CQRS provides a searchable read model that may lag behind writes.",
    "07": "An agent review contains several messages about one decision. A trace ID groups the run; a message ID identifies one message. A source link records what a claim is based on.",
    "08": "Pricing and Catalog perform read-only lookups, while Payments performs a card charge. A timed-out charge may already have succeeded, so repeating it blindly can charge twice.",
    "09": "A small order-details lookup needs data for one ID; a support search must filter across many records. API composition handles small joins; CQRS adds a searchable read model. Event sourcing keeps an event history that can be replayed to recover past state.",
    "10": "A Pricing lookup is a read. A Payments charge can change a customer's balance even if the response times out. A router itself can add model calls before a case reaches review.",
    "11": "Orders owns its private data. Reporting can use an exposed API or published events. A broad search across services may benefit from a CQRS read model, while a small lookup can use API composition.",
    "12": "Checkout creates an order, verifies the customer, reserves stock, and requests payment. A failed authorization is not a completed charge; completed writes may need compensating actions while other services can observe intermediate states.",
    "13": "A payment provider and ShopEasy may use different field names and representations. An anti-corruption layer translates between them; A2A describes how agents discover and exchange messages.",
    "14": "Payment reads the total field in an OrderPlaced event. Renaming or removing that field breaks its existing contract. A new optional field can be added without requiring existing consumers to use it.",
    "15": "Checkout depends on critical Inventory and Payments services and optional Recommendations. Their latency and failure effects differ; a payment charge is not idempotent. The example's targets are assumptions to validate.",
    "16": "A price lookup is a read, but a card charge changes money and might already have succeeded after a timeout. Feedback cases update trust; separate test cases measure results without influencing the update.",
    "17": "A task queue distributes work among competing workers. A retained event log lets separate subscriber groups read events independently. A record key groups related records; eventId identifies a fact for deduplication.",
}


def review_note(lesson):
    """Keep the Colab revision questions traceable to the supplied lecture decks."""
    review = lesson["review"]
    for source in review["sources"]:
        _, count = DECKS[source["deck"]]
        if not source["slides"] or any(type(n) is not int or not 1 <= n <= count for n in source["slides"]):
            raise ValueError(f"Invalid teaching-source reference in {lesson['slug']}")
    questions = "\n".join(f"{i}. {q}" for i, q in enumerate(review["questions"], 1))
    return ("## Think about the example\n\n"
            + EXAMPLE_CONTEXT[lesson["slug"][:2]] + "\n\n"
            + "**Concepts:** " + "; ".join(review["concepts"]) + "."
            + "\n\nUse the scenario above to consider these questions before running the code:\n\n"
            + questions)



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
    if slug == "01_prompting_evaluation":
        source += ('\nMODE = "practice"  # change to "live" for real model calls\n'
                   'PROVIDER = "deepseek"  # or "gemini" or "freeinference" for Steps 1–3\n'
                   'if MODE == "live" and find_spec("transformers") is None:\n'
                   '    %pip install -q "transformers>=4.45,<5" torch\n'
                   'from coursekit.runtime import Client, secret\n'
                   'from coursekit.notebook import PROVIDERS\n'
                   'settings = PROVIDERS[PROVIDER]\n'
                   'key = secret(settings["secret_name"]) if MODE == "live" else ""\n'
                   'plain = Client(mode=MODE, model=settings["model"], base_url=settings["base_url"],\n'
                   '               api_key=key, max_calls=12, extra_body=settings.get("extra_body"))\n'
                   'thinking = None\n'
                   'if PROVIDER == "deepseek":\n'
                   '    thinking = Client(mode=MODE, model=settings["model"], base_url=settings["base_url"],\n'
                   '                      api_key=key, max_calls=12, max_tokens=4096, timeout=120,\n'
                   '                      extra_body={"thinking": {"type": "enabled"}, "reasoning_effort": "low"})')
    elif slug not in NO_MODEL_LABS:
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
    if slug == "01_prompting_evaluation":
        setup_note += (' Practice mode uses scripted answers without a key. For live mode, save '
                       '`DEEPSEEK_API_KEY` in Colab Secrets, keep `PROVIDER="deepseek"`, set '
                       '`MODE="live"`, and rerun this setup cell. Live Step 4 downloads a small '
                       'local model; Step 5 uses DeepSeek thinking mode. Other providers work in '
                       'Steps 1–3; Step 5 requires DeepSeek. Each client stops after 12 calls.')
    elif slug not in NO_MODEL_LABS:
        setup_note += (' Practice answers are scripted. For a live model, choose `PROVIDER` '
                       '(`"freeinference"`, `"gemini"`, or `"deepseek"`), save its key in Colab Secrets '
                       '(`FREEINFERENCE_API_KEY`, `GEMINI_API_KEY`, or `DEEPSEEK_API_KEY`), and change `MODE` to '
                       '`"live"`. `ask` stops after 12 calls; run this cell again to reset the count.')
    elif slug == '17_weighted_decision_jev':
        setup_note += ' Practice scores need no key. Optional live scoring uses TYPESAFE_API_KEY and explicit live mode in the lab.'
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
             source_cell("markdown", review_note(lesson)),
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
    rows = []
    for slug in config["labs"]:
        lesson = json.loads((ROOT / "lessons" / (slug + ".json")).read_text())
        review = lesson["review"]
        readings = "; ".join(f"{DECKS[s['deck']][0]}: {', '.join(map(str, s['slides']))}"
                             for s in review["sources"])
        rows.append(f"| {slug[:2]} · {lesson['title']} | {'; '.join(review['concepts'])} | {readings} |")
    (ROOT / "docs" / "slide-map.md").write_text(
        "# Microservices lecture review map\n\n"
        "Each Colab lab has two goals: build one agentic mechanism and revisit a concrete "
        "microservices or DDD decision from the supplied lectures. Its opening review names the "
        "slides and asks two recall questions; its code, checks, and exercises apply those ideas.\n\n"
        "Slide numbers include each deck's title slide and appendices. The PowerPoint files remain "
        "class materials and are not redistributed here. The examples are small adaptations; "
        "scripted replies, scores, workloads, and timing fixtures are not empirical results.\n\n"
        "| Lab / agentic mechanism | Microservices / DDD revision | Lecture slides |\n"
        "| --- | --- | --- |\n" + "\n".join(rows) + "\n")


if __name__ == "__main__":
    main()

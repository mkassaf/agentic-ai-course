#!/usr/bin/env python3
"""Build Lab 00's independent comparisons of demonstrations and persona prompts."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'images' / 'prompt-techniques.svg'

ROUTING_QUESTION = "My package hasn't arrived."
ROUTING_INSTRUCTION = 'Choose one category: Billing, Delivery, or Login. Reply with the category only.'
ARCHITECTURE_QUESTION = 'ShopEasy has phone and browser clients that need different tailored APIs. Which pattern fits?'
ARCHITECTURE_LABELS = 'Bulkhead · API gateway · BFF'
DEMOS = (
    ('My package arrived at the wrong address.', 'Delivery'),
    ('I was charged twice.', 'Billing'),
    ("I can't sign in.", 'Login'),
)
PERSONA = 'You are a mobile developer.'


def wrap_text(value, width, size, bold=False):
    """Wrap words using conservative Helvetica/Arial-like advance widths.

    Keep a margin for platform font substitutions. No browser-only foreignObject
    is needed, so the SVG also works in notebook and static-image renderers.
    """
    narrow = set("ilIjtfr.,:;!'| ")
    wide = set('MW@%&QO')

    def advance(word):
        units = sum(.30 if c in narrow else .90 if c in wide else .58 for c in word)
        return units * size * (1.06 if bold else 1)

    lines, line = [], ''
    for word in value.split():
        candidate = f'{line} {word}' if line else word
        if line and advance(candidate) > width * .96:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def paragraph(x, y, width, value, cls='body', size=20, bold=False, line_height=None):
    """Return wrapped SVG text and the first baseline available below it."""
    line_height = line_height or round(size * 1.35)
    lines = wrap_text(value, width, size, bold)
    spans = ''.join(f'<tspan x="{x}" dy="{0 if i == 0 else line_height}">{escape(line)}</tspan>'
                    for i, line in enumerate(lines))
    return f'<text x="{x}" y="{y}" class="{cls}">{spans}</text>', y + len(lines) * line_height


def rect(x, y, width, height, cls='card', radius=16):
    return f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="{radius}" class="{cls}"/>'


def render():
    desc = (
        'Panel A compares three prompts for the same customer message about a missing package. '
        'The categories are Billing, Delivery, and Login. Zero-shot gives no examples. '
        'One-shot shows a package sent to the wrong address, categorized as Delivery. '
        'Few-shot adds a double charge for Billing and a sign-in problem for Login. '
        'The expected category is Delivery. Panel B asks '
        'both prompts which API pattern supports phone and browser clients with different '
        'needs and asks for one operational trade-off. The persona prompt adds the role '
        'of a mobile developer. Both prompts give zero worked examples.'
    )
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 1450" role="img" aria-labelledby="title desc">
<title id="title">Prompting techniques: demonstrations and persona are separate choices</title>
<desc id="desc">{escape(desc)}</desc>
<style>
  text {{ font-family: "Helvetica Neue", Arial, sans-serif; fill: #000000; }}
  .title {{ font-size: 36px; font-weight: 700; }}
  .intro {{ font-size: 21px; fill: #5C5C5C; }}
  .section {{ font-size: 28px; font-weight: 700; }}
  .body {{ font-size: 20px; }}
  .label {{ font-size: 20px; font-weight: 700; }}
  .small {{ font-size: 18px; fill: #5C5C5C; }}
  .badge {{ font-size: 20px; font-weight: 700; }}
  .card {{ fill: #FFFFFF; stroke: #D4DBE2; stroke-width: 1.5; }}
  .soft {{ fill: #F3F5F7; }}
  .row {{ fill: #F9FAFB; }}
  .line {{ stroke: #E0E6EB; stroke-width: 1.5; }}
</style>
<rect width="1100" height="1450" rx="24" fill="#F3F5F7"/>''']

    def put(x, y, width, value, cls='body', size=20, bold=False):
        element, below = paragraph(x, y, width, value, cls, size, bold)
        parts.append(element)
        return below

    put(40, 62, 1020, 'Examples and roles change different parts of a prompt', 'title', 36, True)
    put(40, 126, 1020, 'Two comparisons. Change one ingredient at a time.', 'intro', 21)

    parts += [rect(40, 158, 1020, 718),
              '<circle cx="79" cy="202" r="19" fill="#14A800"/>']
    put(72, 209, 22, 'A', 'badge', 20, True)
    put(112, 211, 895, 'Compare the number of worked examples', 'section', 28, True)
    put(64, 251, 972, 'Keep the same customer message, category choices, and response format.', 'intro', 21)

    parts.append(rect(64, 272, 972, 140, 'soft', 12))
    put(84, 302, 932, 'Customer message', 'label', 20, True)
    put(84, 332, 932, ROUTING_QUESTION)
    put(84, 366, 932, ROUTING_INSTRUCTION, 'small', 18)

    put(84, 453, 185, 'Prompt variant', 'label', 20, True)
    put(297, 453, 710, 'Worked examples before the new message', 'label', 20, True)

    rows = [
        (472, 76, 'Zero-shot', '0 examples', []),
        (560, 94, 'One-shot', '1 example', DEMOS[:1]),
        (666, 142, 'Few-shot', '3 examples', DEMOS),
    ]
    for y, height, name, count, demos in rows:
        parts.append(rect(64, y, 972, height, 'row', 12))
        put(84, y + 29, 185, name, 'label', 20, True)
        put(84, y + 57, 185, count, 'small', 18)
        parts.append(f'<path d="M275 {y+14} V{y+height-14}" class="line"/>')
        if not demos:
            put(297, y + 43, 715, 'No examples.', 'body', 20)
        else:
            baseline = y + 29
            for question, answer in demos:
                baseline = put(297, baseline, 715, f'{question} → {answer}', 'small', 18) + 3
    put(64, 846, 972, 'Expected category: Delivery.', 'small', 18)

    parts += [rect(40, 904, 1020, 462),
              '<circle cx="79" cy="948" r="19" fill="#14A800"/>']
    put(72, 955, 22, 'B', 'badge', 20, True)
    put(112, 957, 895, 'Compare a neutral prompt with a persona', 'section', 28, True)
    put(64, 999, 972, ARCHITECTURE_QUESTION)
    put(64, 1032, 972, f'Choices: {ARCHITECTURE_LABELS}', 'small', 18)
    put(64, 1065, 972, 'Both prompts ask for one operational trade-off in two short sentences.', 'small', 18)

    for x, title, body in (
        (64, 'Neutral · no role', 'No persona instruction is added.'),
        (562, 'Persona · one role', PERSONA),
    ):
        parts.append(rect(x, 1090, 474, 156, 'row', 12))
        put(x + 20, 1125, 434, title, 'label', 20, True)
        put(x + 20, 1163, 434, body)
    put(64, 1284, 972, '0 demonstrations in either prompt. Only the role instruction changes.', 'label', 20, True)
    put(64, 1323, 972, 'A persona can change emphasis; it does not guarantee expertise or correctness.', 'small', 18)

    parts.append('<rect x="40" y="1392" width="6" height="27" rx="3" fill="#14A800"/>')
    put(60, 1413, 1000, 'Zero-shot still has instructions. Shots count worked input → output demonstrations, not requests.', 'small', 18)
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(), encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

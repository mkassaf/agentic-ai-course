#!/usr/bin/env python3
"""Build Lab 00's independent comparisons of demonstrations and persona prompts."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'images' / 'prompt-techniques.svg'

ROUTING_QUESTION = "My package hasn't arrived."
ROUTING_INSTRUCTION = 'Choose one category: Billing, Delivery, or Login. Reply with the category only.'
ARCHITECTURE_QUESTION = "ShopEasy's mobile app needs smaller responses. The team can fund one change this sprint."
ARCHITECTURE_OPTIONS = 'Build a mobile-only API (a BFF) or add smaller responses to the shared API.'
ARCHITECTURE_INSTRUCTION = 'Choose one option and give one trade-off in two short sentences.'
DEMOS = (
    ('My package arrived at the wrong address.', 'Delivery'),
    ('I was charged twice.', 'Billing'),
    ("I can't sign in.", 'Login'),
)
PERSONAS = (
    ('Mobile team lead', 'You lead the mobile team. Your team is measured on how quickly it can ship mobile changes.'),
    ('Platform team lead', 'You lead the platform team. Your team is measured on keeping the number of services it runs low.'),
)


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
        'The expected category is Delivery. Panel B asks two team leads to choose a single '
        'change for smaller mobile API responses and give a trade-off. The mobile team lead '
        'is measured on how quickly the team ships mobile changes and may favor a mobile-only API. '
        'The platform team lead is measured on keeping the number of services low and may favor '
        'updating the shared API. Both receive the same task.'
    )
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1100 1500" role="img" aria-labelledby="title desc">
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
<rect width="1100" height="1500" rx="24" fill="#F3F5F7"/>''']

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

    parts += [rect(40, 904, 1020, 522),
              '<circle cx="79" cy="948" r="19" fill="#14A800"/>']
    put(72, 955, 22, 'B', 'badge', 20, True)
    put(112, 957, 895, 'Give two team leads the same decision', 'section', 28, True)
    next_line = put(64, 999, 972, ARCHITECTURE_QUESTION)
    next_line = put(64, next_line + 6, 972, ARCHITECTURE_OPTIONS, 'small', 18)
    next_line = put(64, next_line + 8, 972, ARCHITECTURE_INSTRUCTION, 'small', 18)

    card_y = next_line + 10
    choices = ('May favor a mobile-only API.', 'May favor updating the shared API.')
    for x, (title, body), choice in zip((64, 562), PERSONAS, choices):
        parts.append(rect(x, card_y, 474, 176, 'row', 12))
        put(x + 20, card_y + 35, 434, title, 'label', 20, True)
        put(x + 20, card_y + 70, 434, body)
        put(x + 20, card_y + 150, 434, choice, 'small', 18)
    put(64, card_y + 215, 972, 'Both leads get the same task. Their incentives pull in different directions.', 'label', 20, True)
    put(64, card_y + 250, 972, 'Compare the options they choose and the trade-offs they point out.', 'small', 18)

    parts.append('<rect x="40" y="1442" width="6" height="27" rx="3" fill="#14A800"/>')
    put(60, 1463, 1000, 'Zero-shot still has instructions. Shots count worked input → output demonstrations, not requests.', 'small', 18)
    parts.append('</svg>')
    return '\n'.join(parts) + '\n'


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render(), encoding='utf-8')
    print(f'Built {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

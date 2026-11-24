#!/usr/bin/env python3
"""Generate the small, numerically checked sampling illustration for Lab 01."""
from html import escape
from math import exp
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'assets' / 'images' / 'sampling-settings.svg'


def normalize(values):
    total = sum(values)
    return [value / total for value in values]


def example():
    """Temperature, top-k, then top-p on four illustrative next-token scores."""
    logits = [2.0, 1.0, 0.0, -1.0]
    temperature, top_k, top_p = 2.0, 3, 0.80
    scaled = [score / temperature for score in logits]
    after_temperature = normalize([exp(score) for score in scaled])
    ordered = sorted(range(len(logits)), key=lambda index: after_temperature[index], reverse=True)
    kept_k = set(ordered[:top_k])
    after_k = normalize([value if i in kept_k else 0.0 for i, value in enumerate(after_temperature)])
    kept_p, accumulated = [], 0.0
    for i in ordered:
        if after_k[i] == 0.0:
            continue
        kept_p.append(i)
        accumulated += after_k[i]
        if accumulated >= top_p:
            break
    after_p = normalize([value if i in kept_p else 0.0 for i, value in enumerate(after_k)])
    return dict(logits=logits, after_temperature=after_temperature, after_k=after_k,
                after_p=after_p, kept_p=kept_p, accumulated=accumulated)


def percent(value):
    return f'{100 * value:.2f}%'


def text(x, y, value, cls='body', anchor='start'):
    return f'<text x="{x}" y="{y}" class="{cls}" text-anchor="{anchor}">{escape(str(value))}</text>'


def card(x, y, width, number, title, subtitle):
    parts = [f'<rect x="{x}" y="{y}" width="{width}" height="300" rx="18" class="card"/>',
             f'<circle cx="{x+37}" cy="{y+43}" r="19" fill="#14a800"/>',
             text(x+37, y+50, number, 'number', 'middle'),
             text(x+70, y+52, title, 'card-title'),
             text(x+25, y+100, subtitle, 'subtitle')]
    return parts


def token_row(x, y, width, values):
    parts = []
    for i, (label, value) in enumerate(zip(('A', 'B', 'C', 'D'), values)):
        center = x + width * (i + .5) / 4
        parts += [text(center, y, label, 'token', 'middle'),
                  text(center, y+49, value, 'value' if value != 'removed' else 'removed', 'middle')]
    return parts


def render():
    values = example()
    p, k, final = values['after_temperature'], values['after_k'], values['after_p']
    desc = ('A four-token illustrative example: scores 2, 1, 0, and minus 1. Temperature 2 '
            'produces probabilities 45.51%, 27.60%, 16.74%, and 10.15%. Top-k 3 removes D '
            'and renormalizes the rest to 50.65%, 30.72%, and 18.63%. Top-p 0.80 keeps A '
            'and B, whose cumulative probability is 81.37%. The final probabilities are '
            '62.25% for A and 37.75% for B; one is sampled. This is one possible processing order.')
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1020" role="img" aria-labelledby="title desc">
<title id="title">How temperature, top-k, and top-p choose a next token</title>
<desc id="desc">{escape(desc)}</desc>
<style>
  text {{ font-family: "Helvetica Neue", Arial, sans-serif; fill: #1a1a1a; }}
  .title {{ font-size: 43px; font-weight: 700; }}
  .intro {{ font-size: 23px; fill: #5c5c5c; }}
  .pill {{ font-size: 20px; font-weight: 700; }}
  .card {{ fill: white; stroke: #d4dbe2; stroke-width: 2; }}
  .number {{ font-size: 22px; font-weight: 700; }}
  .card-title {{ font-size: 27px; font-weight: 700; }}
  .subtitle {{ font-size: 20px; fill: #5c5c5c; }}
  .token {{ font-size: 22px; font-weight: 700; }}
  .value {{ font-size: 27px; font-weight: 600; }}
  .removed {{ font-size: 20px; fill: #798086; }}
  .body {{ font-size: 22px; }}
  .note {{ font-size: 20px; fill: #5c5c5c; }}
  .large {{ font-size: 37px; font-weight: 700; }}
</style>
<defs><marker id="arrow" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#798086"/></marker></defs>
<rect width="1600" height="1020" rx="26" fill="#f3f5f7"/>''',
             text(50, 66, 'How sampling chooses the next token', 'title'),
             text(50, 106, 'A worked example: temperature → top-k → top-p → sample', 'intro'),
             '<rect x="50" y="131" width="455" height="48" rx="24" fill="#e0e6eb"/>',
             text(70, 162, 'T = 2.0  ·  top-k = 3  ·  top-p = 0.80', 'pill'),
             text(535, 162, 'Four illustrative candidates, not actual model scores', 'intro'),
             '<path d="M520 355 H548" stroke="#798086" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
             '<path d="M1040 355 H1068" stroke="#798086" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
             '<path d="M1320 505 V545 H390 V558" stroke="#798086" stroke-width="3" fill="none" marker-end="url(#arrow)"/>',
             '<path d="M770 720 H810" stroke="#798086" stroke-width="3" fill="none" marker-end="url(#arrow)"/>']
    parts += card(40, 205, 480, 1, 'Model scores', 'Four candidate next tokens')
    parts += token_row(65, 360, 430, [f'{x:.1f}' for x in values['logits']])
    parts += [text(65, 465, 'Scores are not probabilities yet.', 'note')]
    parts += card(560, 205, 480, 2, 'Temperature = 2', 'Divide scores by 2; compute probabilities')
    parts += token_row(585, 360, 430, [percent(x) for x in p])
    parts += [text(585, 465, 'Higher temperature flattens this example.', 'note')]
    parts += card(1080, 205, 480, 3, 'Top-k = 3', 'Keep the three highest candidates')
    parts += token_row(1105, 360, 430, [percent(k[0]), percent(k[1]), percent(k[2]), 'removed'])
    parts += [text(1105, 465, 'D is removed; remaining values are rescaled.', 'note')]
    parts += card(40, 570, 730, 4, 'Top-p = 0.80', 'Keep the smallest most-likely set reaching 80%')
    parts += [text(65, 743, f'A {percent(k[0])}  +  B {percent(k[1])}  =  {percent(values["accumulated"])}', 'large'),
              text(65, 805, 'Keep A and B; remove C. D was already removed.', 'body')]
    parts += card(830, 570, 730, 5, 'Sample one token', 'Renormalize the surviving candidates')
    parts += [text(855, 743, f'A  {percent(final[0])}       B  {percent(final[1])}', 'large'),
              text(855, 805, 'Sample A or B, then repeat for the next token.', 'body')]
    parts += [text(50, 931, 'This shows Transformers sampling with these settings and no other filters. Providers may use a different order or ignore settings.', 'note'),
              text(50, 968, 'The probabilities are illustrative. Temperature zero and greedy decoding are handled separately.', 'note'), '</svg>']
    return '\n'.join(parts) + '\n'


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(render())
    print(f'Built {OUTPUT.relative_to(ROOT)}')


if __name__ == '__main__':
    main()

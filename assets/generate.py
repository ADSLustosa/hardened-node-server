#!/usr/bin/env python3
"""Generate the README visuals (banner + request pipeline) in EN and PT-BR.

Usage:  python3 assets/generate.py

Only the Python standard library is used, so the SVGs are reproducible on
any machine. To mark a roadmap step as shipped, add its number to
SHIPPED_STEPS and run the script again: the pipeline box turns from dashed
(planned) to solid (shipped).
"""

from html import escape
from pathlib import Path

# Roadmap steps already merged into main. Update together with the README.
SHIPPED_STEPS: set[int] = set()

OUT = Path(__file__).resolve().parent

FONT = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', 'Ubuntu Mono', Consolas, monospace"

BG_TOP = "#0b1220"
BG_BOTTOM = "#121c33"
TEXT = "#e6edf3"
MUTED = "#9fb3c8"
GREEN = "#3fb950"
BLUE = "#58a6ff"
CARD = "#0f1a2e"

TEXTS = {
    "en": {
        "tagline": "Production-minded HTTP server in pure Node.js",
        "sub": "no frameworks · zero runtime dependencies · secure by default",
        "pills": ["node:http only", "0 runtime deps", "defense in depth", "built step by step"],
        "core": "your code",
        "pipeline_title": "Target request pipeline (v1.0.0)",
        "shipped": "shipped",
        "planned": "planned",
        "client": "Client",
        "response": "Response",
        "step": "STEP",
        "stages": [
            (8, "Socket timeouts", "anti-Slowloris"),
            (7, "Rate limiter", "429 + Retry-After"),
            (3, "Router", "404 / 405 + Allow"),
            (4, "Body limits", "413 / 415 / 400"),
            (2, "Handler", "notes API"),
            ("5·6", "Headers & cookies", "CSP · HSTS · __Host-"),
        ],
    },
    "pt-BR": {
        "tagline": "Servidor HTTP pronto para produção em Node.js puro",
        "sub": "sem frameworks · zero dependências em produção · seguro por padrão",
        "pills": ["só node:http", "0 dependências", "defesa em camadas", "etapa por etapa"],
        "core": "seu código",
        "pipeline_title": "Caminho da requisição planejado (v1.0.0)",
        "shipped": "entregue",
        "planned": "planejado",
        "client": "Cliente",
        "response": "Resposta",
        "step": "ETAPA",
        "stages": [
            (8, "Timeouts do socket", "anti-Slowloris"),
            (7, "Rate limiter", "429 + Retry-After"),
            (3, "Roteador", "404 / 405 + Allow"),
            (4, "Limites do corpo", "413 / 415 / 400"),
            (2, "Handler", "API de notas"),
            ("5·6", "Headers e cookies", "CSP · HSTS · __Host-"),
        ],
    },
}

RINGS = ["timeouts", "rate limit", "router", "body limits", "headers", "cookies"]


def text_width(text: str, size: float, mono: bool = False) -> float:
    """Rough width estimate; SVG cannot measure text before rendering."""
    return len(text) * size * (0.62 if mono else 0.56)


def banner(lang: str) -> str:
    t = TEXTS[lang]
    w, h = 1280, 360
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="hardened-node-server: {escape(t["tagline"])}">',
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>',
        f'<linearGradient id="shield" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>',
        '<pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity="0.04"/></pattern>',
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="20" fill="url(#bg)"/>',
        f'<rect width="{w}" height="{h}" rx="20" fill="url(#grid)"/>',
    ]

    # Shield icon with a check mark.
    parts += [
        '<g transform="translate(70 92)">',
        '<path d="M60 0 L120 22 V70 C120 112 94 140 60 156 C26 140 0 112 0 70 V22 Z" fill="url(#shield)"/>',
        '<path d="M60 14 L106 31 V70 C106 103 86 126 60 140 C34 126 14 103 14 70 V31 Z" fill="#0b1220" fill-opacity="0.35"/>',
        '<path d="M36 78 L54 96 L88 58" fill="none" stroke="#ffffff" stroke-width="11" stroke-linecap="round" stroke-linejoin="round"/>',
        "</g>",
    ]

    x = 230
    parts += [
        f'<text x="{x}" y="138" font-family="{MONO}" font-size="50" font-weight="700" fill="{TEXT}">hardened-node-server</text>',
        f'<text x="{x}" y="184" font-family="{FONT}" font-size="25" font-weight="600" fill="{TEXT}">{escape(t["tagline"])}</text>',
        f'<text x="{x}" y="218" font-family="{FONT}" font-size="18" fill="{MUTED}">{escape(t["sub"])}</text>',
    ]

    px = x
    for pill in t["pills"]:
        pw = text_width(pill, 15) + 30
        parts += [
            f'<rect x="{px}" y="250" width="{pw:.0f}" height="34" rx="17" fill="{CARD}" stroke="{GREEN}" stroke-opacity="0.55"/>',
            f'<text x="{px + pw / 2:.0f}" y="272" font-family="{FONT}" font-size="15" fill="{TEXT}" text-anchor="middle">{escape(pill)}</text>',
        ]
        px += pw + 12

    # Defense-in-depth rings around the application core.
    cx, cy = 1105, 180
    for i, label in enumerate(RINGS):
        r = 160 - i * 20
        opacity = 0.25 + i * 0.1
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{BLUE if i % 2 else GREEN}" stroke-opacity="{opacity:.2f}" stroke-width="2" stroke-dasharray="{"6 6" if i % 2 else "none"}"/>'
        )
        parts.append(
            f'<text x="{cx}" y="{cy - r + 14}" font-family="{MONO}" font-size="11" fill="{MUTED}" text-anchor="middle">{label}</text>'
        )
    parts += [
        f'<circle cx="{cx}" cy="{cy}" r="44" fill="url(#shield)"/>',
        f'<text x="{cx}" y="{cy + 5}" font-family="{FONT}" font-size="12" font-weight="700" fill="#0b1220" text-anchor="middle">{escape(t["core"])}</text>',
        "</svg>",
    ]
    return "\n".join(parts) + "\n"


def stage_box(x: float, y: float, w: float, h: float, step, title: str, sub: str, lang: str) -> list[str]:
    t = TEXTS[lang]
    numbers = [int(n) for n in str(step).split("·")]
    shipped = all(n in SHIPPED_STEPS for n in numbers)
    color = GREEN if shipped else BLUE
    dash = "" if shipped else ' stroke-dasharray="7 5"'
    badge = f'{t["step"]} {step}'
    bw = text_width(badge, 11, mono=True) + 16
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{CARD}" stroke="{color}" stroke-width="2"{dash}/>',
        f'<rect x="{x + 14}" y="{y + 14}" width="{bw:.0f}" height="20" rx="10" fill="{color}" fill-opacity="0.18"/>',
        f'<text x="{x + 14 + bw / 2:.0f}" y="{y + 28}" font-family="{MONO}" font-size="11" font-weight="700" fill="{color}" text-anchor="middle">{escape(badge)}</text>',
        f'<text x="{x + 14}" y="{y + 60}" font-family="{FONT}" font-size="18" font-weight="600" fill="{TEXT}">{escape(title)}</text>',
        f'<text x="{x + 14}" y="{y + 84}" font-family="{MONO}" font-size="13" fill="{MUTED}">{escape(sub)}</text>',
    ]


def endpoint(x: float, y: float, w: float, h: float, label: str) -> list[str]:
    return [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="#1b2a44" stroke="{MUTED}" stroke-opacity="0.6"/>',
        f'<text x="{x + w / 2}" y="{y + h / 2 + 6}" font-family="{FONT}" font-size="16" font-weight="600" fill="{TEXT}" text-anchor="middle">{escape(label)}</text>',
    ]


def arrow(x1: float, y1: float, x2: float, y2: float) -> str:
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>'


def pipeline(lang: str) -> str:
    t = TEXTS[lang]
    w, h = 960, 380
    bw, bh, gap, ew = 230, 100, 40, 110
    row1, row2 = 90, 250
    s = t["stages"]

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(t["pipeline_title"])}">',
        "<defs>",
        f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG_TOP}"/><stop offset="1" stop-color="{BG_BOTTOM}"/></linearGradient>',
        f'<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{MUTED}"/></marker>',
        "</defs>",
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#bg)"/>',
        f'<text x="20" y="44" font-family="{FONT}" font-size="22" font-weight="700" fill="{TEXT}">{escape(t["pipeline_title"])}</text>',
    ]

    # Legend.
    lx = w - 270
    parts += [
        f'<line x1="{lx}" y1="38" x2="{lx + 34}" y2="38" stroke="{GREEN}" stroke-width="3"/>',
        f'<text x="{lx + 42}" y="43" font-family="{FONT}" font-size="14" fill="{MUTED}">{escape(t["shipped"])}</text>',
        f'<line x1="{lx + 130}" y1="38" x2="{lx + 164}" y2="38" stroke="{BLUE}" stroke-width="3" stroke-dasharray="7 5"/>',
        f'<text x="{lx + 172}" y="43" font-family="{FONT}" font-size="14" fill="{MUTED}">{escape(t["planned"])}</text>',
    ]

    # Row 1: client -> 3 stages.
    x = 20
    ey1 = row1 + (bh - 44) / 2
    parts += endpoint(x, ey1, ew, 44, t["client"])
    x += ew
    for stage in s[:3]:
        parts.append(arrow(x + 4, row1 + bh / 2, x + gap - 4, row1 + bh / 2))
        x += gap
        parts += stage_box(x, row1, bw, bh, *stage, lang)
        x += bw
    last_cx = x - bw / 2

    # Connector from row 1 down to row 2.
    first2_cx = 20 + bw / 2
    mid = row1 + bh + (row2 - row1 - bh) / 2
    parts.append(
        f'<path d="M{last_cx} {row1 + bh + 4} V{mid} H{first2_cx} V{row2 - 4}" fill="none" stroke="{MUTED}" stroke-width="2" marker-end="url(#arrow)"/>'
    )

    # Row 2: 3 stages -> response.
    x = 20
    for i, stage in enumerate(s[3:]):
        if i:
            parts.append(arrow(x + 4, row2 + bh / 2, x + gap - 4, row2 + bh / 2))
            x += gap
        parts += stage_box(x, row2, bw, bh, *stage, lang)
        x += bw
    parts.append(arrow(x + 4, row2 + bh / 2, x + gap - 4, row2 + bh / 2))
    x += gap
    parts += endpoint(x, row2 + (bh - 44) / 2, ew, 44, t["response"])

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    for lang in TEXTS:
        suffix = "" if lang == "en" else f".{lang}"
        (OUT / f"banner{suffix}.svg").write_text(banner(lang), encoding="utf-8")
        (OUT / f"pipeline{suffix}.svg").write_text(pipeline(lang), encoding="utf-8")
        print(f"generated banner{suffix}.svg and pipeline{suffix}.svg")


if __name__ == "__main__":
    main()

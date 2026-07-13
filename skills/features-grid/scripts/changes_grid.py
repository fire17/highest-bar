#!/usr/bin/env python3
"""features-grid renderer — colorful, pixel-perfect ASCII card grid of a
project's features. Reads a JSON spec (file arg or stdin) with DONE and
IN-PROGRESS sections; every card carries a colored progress bar.

Alignment rule: all padding/centering is done on PLAIN text FIRST, then ANSI
color (zero display width) is wrapped around fixed-width segments — so colors
never shift the grid. Block-char bars stay aligned with or without color.

JSON spec:
{
  "title": "HERDR++ — FEATURES GRID",
  "subtitle": "fire17's patched fork of herdr",
  "sections": [
    {"name": "DONE",        "accent": "green",  "cards": [
       {"id":"0046","title":"FEEDBACK COMPOSER","desc":"...","tag":"live","progress":100}]},
    {"name": "IN PROGRESS", "accent": "yellow", "cards": [
       {"id":"Ph3b","title":"SELF-EXTEND HARNESS","desc":"...","tag":"gated","progress":30}]}
  ],
  "stats": ["55 patches", "2621 tests green", "badge 0.1.32", "HEALTHY"]
}
"""
import sys, os, json, textwrap

NO_COLOR = ("--no-color" in sys.argv) or bool(os.environ.get("NO_COLOR"))

def c(s, code):
    return s if NO_COLOR else f"\033[{code}m{s}\033[0m"

DIM = "2"; BOLD = "1"
NAMED = {"red": "31", "green": "32", "yellow": "33", "blue": "34",
         "magenta": "35", "cyan": "36", "white": "37",
         "bgreen": "92", "byellow": "93", "bcyan": "96", "bmagenta": "95"}
def col(name):  # accepts a named color or a raw ANSI code
    return NAMED.get(name, name)

IW = 36              # inner text width of a card
CW = IW + 4          # full card width: "│ " + IW + " │"
COLS = 2
GAP = "  "
BW = CW * COLS + len(GAP)   # banner / full width

TAGCOL = {"live": "green", "gated": "yellow", "exp": "magenta", "inert": "blue",
          "safe": "blue", "dev": "cyan", "planned": "2", "wip": "yellow",
          "docs": "cyan", "next": "byellow"}
def tag_color(tag):
    return col(TAGCOL.get((tag.split() or [""])[0].lower(), "cyan"))

def bar_of(pct):
    w = 10
    pct = max(0, min(100, int(pct)))
    f = round(pct / 100 * w)
    if pct >= 100: bc = "bgreen"
    elif pct >= 67: bc = "green"
    elif pct >= 34: bc = "yellow"
    elif pct > 0: bc = "red"
    else: bc = "2"
    colored = c("█" * f, col(bc)) + c("░" * (w - f), DIM)
    return colored, w, col(bc)

def bd(l, r):                        # a full-width dim border line
    return c(l + "─" * (IW + 2) + r, DIM)

def trow(plain):                     # a default-color padded text row
    return c("│", DIM) + " " + plain.ljust(IW)[:IW] + " " + c("│", DIM)

def title_row(idn, title, accent):
    t = f"{idn}  {title}"[:IW].ljust(IW)
    return c("│", DIM) + " " + c(t, BOLD + ";" + col(accent)) + " " + c("│", DIM)

def prog_row(pct, tag):
    cbar, w, pcol = bar_of(pct)
    tag = (tag or "")[:14]
    tail_plain = "] " + f"{int(max(0,min(100,pct))):>3}% · {tag}"
    vis = 1 + w + len(tail_plain)
    pad = max(0, IW - vis)
    colored = (c("[", DIM) + cbar + c("] ", DIM)
               + c(f"{int(max(0,min(100,pct))):>3}%", pcol)
               + c(" · ", DIM) + c(tag, tag_color(tag)))
    return c("│", DIM) + " " + colored + " " * pad + " " + c("│", DIM)

def card(cd, accent):
    lines = [bd("╭", "╮"),
             title_row(cd.get("id", ""), cd.get("title", "").upper(), accent),
             bd("├", "┤")]
    body = textwrap.wrap(cd.get("desc", ""), IW)[:3]
    while len(body) < 3:
        body.append("")
    lines += [trow(b) for b in body]
    lines.append(prog_row(cd.get("progress", 0), cd.get("tag", "")))
    lines.append(bd("╰", "╯"))
    return lines

def grid(cards, accent):
    out, cs = [], [card(cd, accent) for cd in cards]
    for i in range(0, len(cs), COLS):
        chunk = cs[i:i + COLS]
        h = max(len(x) for x in chunk)
        for x in chunk:
            x += [" " * CW] * (h - len(x))
        for r in range(h):
            out.append(GAP.join(x[r] for x in chunk))
        out.append("")
    return "\n".join(out)

def banner(title, subtitle):
    BC = col("bcyan")
    line = lambda l, r: c(l + "═" * (BW - 2) + r, BC)
    band = lambda s, code=BC: c("║", BC) + c(s.center(BW - 2), code) + c("║", BC)
    return "\n".join([line("╔", "╗"), band(""),
                      band(title, BOLD + ";" + BC), band(subtitle, DIM),
                      band(""), line("╚", "╝")])

def section(name, accent, count):
    text = f"{name}  ({count})"
    rest = max(0, BW - 3 - len(text) - 1)
    return ("\n" + c("──", col(accent)) + " " + c(text, BOLD + ";" + col(accent))
            + " " + c("─" * rest, DIM) + "\n")

def footer(stats):
    line = lambda l, r: c(l + "─" * (BW - 2) + r, DIM)
    fl = lambda s: c("│", DIM) + s.center(BW - 2)[:BW - 2] + c("│", DIM)
    rows = [line("┌", "┐")]
    for s in stats:
        rows.append(fl(s))
    rows.append(line("└", "┘"))
    return "\n".join(rows)

def main():
    args = [a for a in sys.argv[1:] if a != "--no-color"]
    spec = json.load(open(args[0])) if args else json.load(sys.stdin)
    print(banner(spec.get("title", "FEATURES GRID"), spec.get("subtitle", "")))
    for sec in spec.get("sections", []):
        cards = sec.get("cards", [])
        accent = sec.get("accent", "cyan")
        print(section(sec.get("name", ""), accent, len(cards)))
        print(grid(cards, accent))
    if spec.get("stats"):
        print(footer(spec["stats"]))

if __name__ == "__main__":
    main()

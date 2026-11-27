#!/usr/bin/env python3
"""Generates the SVG panels used by README.md.

Edit the content below and run:  python3 scripts/build_assets.py
Design system follows apple.com: SF Pro, #f5f5f7 canvases, white tiles,
#1d1d1f type, #6e6e73 secondary type, #d2d2d7 hairlines. Compact scale.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W = 1000
PAD = 40
GAP = 14
INNER = W - 2 * PAD

# ---------- apple.com palette ----------
CANVAS = "#f5f5f7"
TILE = "#ffffff"
INK = "#1d1d1f"
GRAY = "#6e6e73"
GRAY2 = "#86868b"
HAIR = "#d2d2d7"
NEW = "#b64400"          # Apple's "New" orange
BLACK = "#000000"
INK_DARK = "#f5f5f7"
HAIR_DARK = "#424245"

FONT = ('-apple-system, BlinkMacSystemFont, &quot;SF Pro Display&quot;, &quot;SF Pro Text&quot;, '
        '&quot;Helvetica Neue&quot;, Helvetica, Inter, &quot;Segoe UI&quot;, Arial, sans-serif')

BASE_CSS = """
text{font-family:FONT_STACK;}
.up{animation:up 1s cubic-bezier(.25,.1,.25,1) both;}
.d1{animation-delay:.05s}.d2{animation-delay:.12s}.d3{animation-delay:.19s}
.d4{animation-delay:.26s}.d5{animation-delay:.33s}.d6{animation-delay:.4s}
@keyframes up{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
""".replace("FONT_STACK", FONT)


def t(x, y, s, size, weight=400, fill=INK, anchor="start", ls=0, cls=""):
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls_attr}{cls_attr}>{escape(s)}</text>')


def frame(h, body, bg=CANVAS, css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h:.0f}" viewBox="0 0 {W} {h:.0f}" role="img">
<defs><style>{BASE_CSS}{css}</style></defs>
<rect width="{W}" height="{h:.0f}" rx="22" fill="{bg}"/>
{body}
</svg>'''


def tile(x, y, w, h, fill=TILE, rx=14):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"/>'


def hair(x1, y1, x2, y2, col=HAIR):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="1"/>'


def pill(x, y, w, label, h=24):
    return (f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.1f}" height="{h - 1}" rx="{(h - 1) / 2}" '
            f'fill="none" stroke="{HAIR}"/>' + t(x + w / 2, y + h / 2 + 4, label, 12, 400, INK, "middle"))


def heading(title, sub):
    return (t(PAD, 62, title, 30, 600, INK, ls=-.7, cls="up d1") +
            t(PAD, 88, sub, 15, 400, GRAY, cls="up d2"))


HEAD_H = 110  # where tiles start below a heading


# =====================================================================
# 1. INTRO: name, numbers, experience
# =====================================================================
def intro():
    parts = [
        t(PAD, 84, "Lal Aman Singh", 50, 600, INK, ls=-1.4, cls="up d1"),
        t(PAD, 116, "AI Product Intern at IndusLabs.", 18, 400, INK, ls=-.2, cls="up d2"),
        t(PAD, 140, "Noida, India", 14, 400, GRAY, cls="up d2"),
    ]
    stats = [("8", "National", "hackathon wins"), ("250+", "Teams at", "Spark Tank"),
             ("1st", "Intellect", "Design Arena"), ("2", "Product", "internships")]
    sx, sw = 520, (W - PAD - 520) / 4
    for i, (n, l1, l2) in enumerate(stats):
        cx = sx + i * sw + sw / 2
        parts.append(t(cx, 90, n, 32, 600, INK, "middle", -.8, f"up d{i + 2}"))
        parts.append(t(cx, 114, l1, 12, 400, GRAY, "middle", 0, f"up d{i + 2}"))
        parts.append(t(cx, 130, l2, 12, 400, GRAY, "middle", 0, f"up d{i + 2}"))
        if i:
            parts.append(hair(sx + i * sw, 60, sx + i * sw, 132))

    y, th = 176, 128
    tw = (INNER - GAP) / 2
    jobs = [("Current", NEW, "Aug 2026 – Present · On-site, Noida", "AI Product Intern", "IndusLabs",
             "Shaping voice AI agents that speak India’s languages."),
            ("Previous", GRAY, "Feb – Jul 2026 · 6 mos", "Product Manager Intern", "RYM Grenergy",
             "Six months in product management.")]
    for i, (eb, ebc, date, role, co, desc) in enumerate(jobs):
        x = PAD + i * (tw + GAP)
        ix = x + 24
        parts.append(f'''<g class="up d{i + 4}">
{tile(x, y, tw, th)}
{t(ix, y + 32, eb, 12, 600, ebc)}
{t(x + tw - 24, y + 32, date, 12, 400, GRAY, "end")}
{t(ix, y + 66, role, 21, 600, INK, ls=-.4)}
{t(ix, y + 88, co, 14, 400, INK)}
{hair(ix, y + 100, x + tw - 24, y + 100)}
{t(ix, y + 118, desc, 12, 400, GRAY)}
</g>''')
    return frame(y + th + PAD, "\n".join(parts))


# =====================================================================
# 2. RECOGNITION
# =====================================================================
def recognition():
    parts = [heading("Recognition.", "Eight national wins. Each one built in hours, not months.")]
    y = HEAD_H
    bw, bh = 440, 222
    parts.append(f'''<g class="up d3">
{tile(PAD, y, bw, bh)}
{t(PAD + 26, y + 34, "1st Prize", 12, 600, NEW)}
{t(PAD + 22, y + 108, "1st", 72, 600, INK, ls=-2.4)}
{t(PAD + 26, y + 146, "Design Spark Challenge", 21, 600, INK, ls=-.4)}
{t(PAD + 26, y + 168, "Intellect Design Arena, Chennai", 13, 400, GRAY)}
{hair(PAD + 26, y + 182, PAD + bw - 26, y + 182)}
{t(PAD + 26, y + 202, "A national banking-product challenge. Cash award and internship offer.", 12, 400, GRAY2)}
</g>''')

    def small(x, ty, w, h, eb, title, sub, big, d):
        return f'''<g class="up d{d}">
{tile(x, ty, w, h)}
{t(x + 22, ty + 30, eb, 11, 600, GRAY)}
{t(x + 22, ty + 58, title, 16, 600, INK, ls=-.2)}
{t(x + 22, ty + 78, sub, 12, 400, GRAY)}
{t(x + w - 22, ty + 66, big, 30, 600, INK, "end", -.8)}
</g>'''

    rx_, rw, rh = PAD + bw + GAP, INNER - bw - GAP, (bh - GAP) / 2
    parts.append(small(rx_, y, rw, rh, "Winner · Oct 2025", "National Level Tech Hackathon", "Kanpur", "1st", 4))
    parts.append(small(rx_, y + rh + GAP, rw, rh, "Winner · Jul 2025", "AI Product Builder", "Jivika Future Work", "1st", 5))

    y2, h2 = y + bh + GAP, 104
    tw = (INNER - 2 * GAP) / 3
    row = [("1st Runner-Up · Oct 2025", "Spark Tank", "IIFM Bhopal. 250+ teams.", "2nd"),
           ("2nd Runner-Up · Nov 2025", "Chakravyuh B-Plan", "CVS, Delhi University.", "3rd"),
           ("24-hour build", "AI HackMatrix", "Chandigarh University.", "24h")]
    for i, (eb, title, sub, big) in enumerate(row):
        parts.append(small(PAD + i * (tw + GAP), y2, tw, h2, eb, title, sub, big, 4 + i))

    y3, h3 = y2 + h2 + GAP, 84
    parts.append(f'<g class="up d6">{tile(PAD, y3, INNER, h3)}')
    parts.append(t(PAD + 22, y3 + 30, "Also pitched at", 11, 600, GRAY))
    stages = [("IIT Bombay", "National Entrepreneurship Challenge"),
              ("IIM Bangalore", "Pitch Perfect, Season 8"),
              ("BHU, Varanasi", "Bharat Innovation Conclave")]
    cw = (INNER - 44) / 3
    for i, (name, det) in enumerate(stages):
        cx = PAD + 22 + i * cw
        parts.append(t(cx, y3 + 54, name, 15, 600, INK, ls=-.2))
        parts.append(t(cx, y3 + 72, det, 12, 400, GRAY))
        if i:
            parts.append(hair(cx - 18, y3 + 42, cx - 18, y3 + 74))
    parts.append("</g>")
    return frame(y3 + h3 + PAD, "\n".join(parts))


# =====================================================================
# 3. HARDINI (black product panel)
# =====================================================================
def hardini():
    h = 300
    cx, cy = 770, 150
    heights = [8, 13, 21, 30, 24, 40, 51, 34, 58, 44, 66, 55, 66, 44, 58, 34, 51, 40, 24, 30, 21, 13, 8]
    n, sp = len(heights), 7
    bars = "".join(
        f'<line class="bar" style="animation-delay:-{abs(i - n // 2) * .09:.2f}s" x1="{cx + (i - n // 2) * sp}" '
        f'y1="{cy - bh / 2:.1f}" x2="{cx + (i - n // 2) * sp}" y2="{cy + bh / 2:.1f}" stroke="{INK_DARK}" '
        f'stroke-width="3" stroke-linecap="round"/>' for i, bh in enumerate(heights))
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{o}"/>'
                    for r, o in [(70, .14), (104, .08), (138, .045)])
    greet = [("नमस्ते", cx - 92, cy - 82, 0), ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", cx + 78, cy - 72, 1.5),
             ("வணக்கம்", cx - 96, cy + 98, 3), ("నమస్కారం", cx + 82, cy + 92, 4.5),
             ("নমস্কার", cx + 104, cy + 5, 6), ("Hello", cx - 118, cy + 5, 7.5)]
    gtxt = "".join(f'<text class="greet" style="animation-delay:{d}s" x="{x}" y="{y}" font-size="12" '
                   f'fill="{GRAY2}" text-anchor="middle">{escape(s)}</text>' for s, x, y, d in greet)
    lx = PAD + 4
    body = f'''
{rings}{bars}{gtxt}
{t(lx, 62, "Featured project", 12, 600, GRAY2, cls="up d1")}
{t(lx - 2, 114, "Hardini", 50, 600, INK_DARK, ls=-1.4, cls="up d2")}
{t(lx, 146, "Ask anything. In your own language.", 19, 400, INK_DARK, ls=-.3, cls="up d3")}
{t(lx, 176, "A voice AI platform for India’s farmers. Crop diseases, mandi", 13, 400, GRAY2, cls="up d4")}
{t(lx, 195, "prices, weather and government schemes, in their native tongue.", 13, 400, GRAY2, cls="up d4")}
<g class="up d5">
{hair(lx, 218, lx + 400, 218, HAIR_DARK)}
{t(lx, 242, "Built in 24 hours at AI HackMatrix, Chandigarh University.", 12, 400, GRAY2)}
{t(lx, 260, "1st Runner-Up at Spark Tank, IIFM Bhopal. 250+ teams.", 12, 400, GRAY2)}
</g>
'''
    css = """
.bar{animation:wave 1.8s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center;}
@keyframes wave{0%{transform:scaleY(.3)}100%{transform:scaleY(1)}}
.greet{opacity:0;animation:greet 9s ease-in-out infinite;}
@keyframes greet{0%,100%{opacity:0}12%,40%{opacity:1}55%{opacity:0}}
"""
    return frame(h, body, BLACK, css)


# =====================================================================
# 4. THE PROCESS + footer
# =====================================================================
def process():
    parts = [heading("The process.", "Every detail considered. From the first interview to launch day.")]
    y, th = HEAD_H, 232
    tw = (INNER - 2 * GAP) / 3
    cols = [
        ("Discover.", ["User research", "Requirements and PRDs", "User stories", "RICE and P0/P1 priorities",
                       "Roadmaps", "Market research", "Competitive analysis"]),
        ("Deliver.", ["Product launch", "Agile, Scrum and Kanban", "Testing, QA and edge cases",
                      "Iterative development", "Cross-functional teams", "Stakeholder communication",
                      "Technical presentations"]),
        ("Build with AI.", ["Voice AI and speech-to-text", "LLM prototyping", "AI/ML product design",
                            "Python for automation", "SQL", "Figma flows and wireframes", "Jira and Notion"]),
    ]
    for i, (title, items) in enumerate(cols):
        x = PAD + i * (tw + GAP)
        ix = x + 22
        parts.append(f'<g class="up d{3 + i}">{tile(x, y, tw, th)}')
        parts.append(t(ix, y + 36, title, 17, 600, INK, ls=-.3))
        for k, it in enumerate(items):
            iy = y + 70 + k * 25
            parts.append(t(ix, iy, it, 13, 400, INK))
            if k < len(items) - 1:
                parts.append(hair(ix, iy + 9, x + tw - 22, iy + 9))
        parts.append("</g>")

    by, bh = y + th + GAP, 82
    bw = (INNER - GAP) / 2
    blocks = [("Certified", "Agile Project Management", "Professional Certificate, Atlassian. Aug 2026.", ["Agile", "Jira"]),
              ("Community", "Event Coordinator", "Lloyd Institute of Engineering and Technology. Dec 2025.", [])]
    for i, (eb, title, sub, chips) in enumerate(blocks):
        x = PAD + i * (bw + GAP)
        ix = x + 22
        parts.append(f'<g class="up d{5 + i}">{tile(x, by, bw, bh)}')
        parts.append(t(ix, by + 28, eb, 11, 600, GRAY))
        parts.append(t(ix, by + 51, title, 16, 600, INK, ls=-.2))
        parts.append(t(ix, by + 69, sub, 12, 400, GRAY))
        cx = x + bw - 22
        for c in reversed(chips):
            w = 16 + len(c) * 7
            cx -= w
            parts.append(pill(cx, by + 14, w, c))
            cx -= 6
        parts.append("</g>")

    # footer
    fy = by + bh + 56
    parts.append(t(W / 2, fy, "Let’s make something great.", 28, 600, INK, "middle", -.6, "up d6"))
    parts.append(t(W / 2, fy + 26, "Open to conversations about AI products, voice and building for India.",
                   14, 400, GRAY, "middle", 0, "up d6"))
    parts.append(hair(PAD, fy + 52, W - PAD, fy + 52))
    parts.append(t(PAD, fy + 74, "Designed by Lal Aman Singh in Noida.", 11, 400, GRAY2))
    parts.append(t(W - PAD, fy + 74, "github.com/lalamansingh", 11, 400, GRAY2, "end"))
    return frame(fy + 96, "\n".join(parts))


PANELS = {"intro": intro, "recognition": recognition, "hardini": hardini, "process": process}

if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        if old.stem not in PANELS:
            old.unlink()
    for name, fn in PANELS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")

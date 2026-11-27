#!/usr/bin/env python3
"""Generates the SVG panels used by README.md.

Edit the content below and run:  python3 scripts/build_assets.py
Design system follows apple.com: SF Pro, #f5f5f7 canvases, white tiles,
#1d1d1f type, #6e6e73 secondary type, #d2d2d7 hairlines.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W = 1000
PAD = 56

# ---------- apple.com palette ----------
CANVAS = "#f5f5f7"
TILE = "#ffffff"
INK = "#1d1d1f"
GRAY = "#6e6e73"
GRAY2 = "#86868b"
HAIR = "#d2d2d7"
NEW = "#b64400"          # Apple's "New" orange
BLACK = "#000000"
INK_DARK = "#f5f5f7"     # text on black
HAIR_DARK = "#424245"

FONT = ('-apple-system, BlinkMacSystemFont, &quot;SF Pro Display&quot;, &quot;SF Pro Text&quot;, '
        '&quot;Helvetica Neue&quot;, Helvetica, Inter, &quot;Segoe UI&quot;, Arial, sans-serif')

BASE_CSS = """
text{font-family:FONT_STACK;}
.up{animation:up 1.2s cubic-bezier(.25,.1,.25,1) both;}
.d1{animation-delay:.05s}.d2{animation-delay:.15s}.d3{animation-delay:.25s}
.d4{animation-delay:.35s}.d5{animation-delay:.45s}.d6{animation-delay:.55s}
@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
""".replace("FONT_STACK", FONT)


def t(x, y, s, size, weight=400, fill=INK, anchor="start", ls=0, cls=""):
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls_attr}{cls_attr}>{escape(s)}</text>')


def frame(h, body, bg=CANVAS, css="", defs=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
<defs><style>{BASE_CSS}{css}</style>{defs}</defs>
<rect width="{W}" height="{h}" rx="28" fill="{bg}"/>
{body}
</svg>'''


def tile(x, y, w, h, fill=TILE, rx=18):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'


def hair(x1, y1, x2, y2, col=HAIR):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col}" stroke-width="1"/>'


def pill(x, y, w, label, h=30, dark=False):
    stroke = HAIR_DARK if dark else HAIR
    col = INK_DARK if dark else INK
    return (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" '
            f'fill="none" stroke="{stroke}"/>' + t(x + w / 2, y + h / 2 + 4.5, label, 13, 400, col, "middle"))


def heading(title, sub, dark=False):
    return (t(PAD, 106, title, 48, 600, INK_DARK if dark else INK, ls=-1.2, cls="up d1") +
            t(PAD, 144, sub, 21, 400, GRAY2 if dark else GRAY, ls=-.2, cls="up d2"))


# =====================================================================
# 1. HERO
# =====================================================================
def hero():
    h = 480
    body = f'''
{t(500, 222, "Lal Aman Singh", 92, 600, INK, "middle", -2.6, "up d1")}
{t(500, 282, "AI Product Intern at IndusLabs.", 28, 400, INK, "middle", -.4, "up d2")}
{t(500, 326, "Noida, India", 19, 400, GRAY, "middle", -.1, "up d3")}
'''
    return frame(h, body)


# =====================================================================
# 2. BY THE NUMBERS
# =====================================================================
def stats():
    h = 250
    items = [
        ("8", "National hackathon", "wins."),
        ("250+", "Teams at Spark Tank.", "We placed second."),
        ("1st", "National challenge,", "Intellect Design Arena."),
        ("2", "Product", "internships."),
    ]
    col = W / 4
    parts = []
    for i, (num, l1, l2) in enumerate(items):
        cx = col * i + col / 2
        d = f"up d{i + 1}"
        parts.append(t(cx, 122, num, 64, 600, INK, "middle", -1.8, d))
        parts.append(t(cx, 164, l1, 15, 400, GRAY, "middle", 0, d))
        parts.append(t(cx, 186, l2, 15, 400, GRAY, "middle", 0, d))
        if i:
            parts.append(hair(col * i, 72, col * i, 186))
    return frame(h, "\n".join(parts))


# =====================================================================
# 3. EXPERIENCE
# =====================================================================
def experience():
    y, th = 184, 290
    tw = (W - 2 * PAD - 20) / 2
    jobs = [
        ("Current", NEW, "Aug 2026 – Present", "AI Product Intern", "IndusLabs",
         ["Shaping voice AI agents that speak", "India’s languages."], "On-site, Noida"),
        ("Feb – Jul 2026", GRAY, "", "Product Manager Intern", "RYM Grenergy",
         ["Six months in product management.", ""], "Internship"),
    ]
    parts = [heading("Experience.", "Two internships. One focus: the people who use the product.")]
    for i, (eb, ebc, date, role, co, desc, foot) in enumerate(jobs):
        x = PAD + i * (tw + 20)
        ix = x + 36
        parts.append(f'''<g class="up d{i + 3}">
{tile(x, y, tw, th)}
{t(ix, y + 50, eb, 14, 600, ebc)}
{t(x + tw - 36, y + 50, date, 14, 400, GRAY, "end")}
{t(ix, y + 116, role, 30, 600, INK, ls=-.7)}
{t(ix, y + 150, co, 21, 400, INK, ls=-.2)}
{t(ix, y + 198, desc[0], 17, 400, GRAY)}
{t(ix, y + 222, desc[1], 17, 400, GRAY)}
{hair(ix, y + 246, x + tw - 36, y + 246)}
{t(ix, y + 272, foot, 13, 400, GRAY2)}
</g>''')
    return frame(y + th + PAD, "\n".join(parts))


# =====================================================================
# 4. RECOGNITION
# =====================================================================
def recognition():
    g = 20
    inner = W - 2 * PAD
    parts = [heading("Recognition.", "Eight national wins. Each one built in hours, not months.")]

    bx, by, bw, bh = PAD, 184, 520, 320
    parts.append(f'''<g class="up d3">
{tile(bx, by, bw, bh)}
{t(bx + 40, by + 52, "1st Prize", 14, 600, NEW)}
{t(bx + 34, by + 172, "1st", 120, 600, INK, ls=-4)}
{t(bx + 40, by + 220, "Design Spark Challenge", 28, 600, INK, ls=-.6)}
{t(bx + 40, by + 248, "Intellect Design Arena, Chennai", 17, 400, GRAY)}
{hair(bx + 40, by + 270, bx + bw - 40, by + 270)}
{t(bx + 40, by + 296, "A national banking-product challenge. Cash award and internship offer.", 13, 400, GRAY2)}
</g>''')

    rx_, rw, rh = bx + bw + g, inner - bw - g, (bh - g) / 2
    right = [("Winner · Oct 2025", "National Level", "Tech Hackathon", "Kanpur"),
             ("Winner · Jul 2025", "AI Product", "Builder", "Jivika Future Work")]
    for i, (eb, l1, l2, sub) in enumerate(right):
        ty = by + i * (rh + g)
        parts.append(f'''<g class="up d{4 + i}">
{tile(rx_, ty, rw, rh)}
{t(rx_ + 30, ty + 42, eb, 13, 600, GRAY)}
{t(rx_ + 30, ty + 80, l1, 21, 600, INK, ls=-.3)}
{t(rx_ + 30, ty + 106, l2, 21, 600, INK, ls=-.3)}
{t(rx_ + 30, ty + 132, sub, 14, 400, GRAY)}
{t(rx_ + rw - 30, ty + 108, "1st", 50, 600, INK, "end", -1.5)}
</g>''')

    r2y, r2h = by + bh + g, 220
    tw = (inner - 2 * g) / 3
    row2 = [("1st Runner-Up · Oct 2025", "2nd", "Spark Tank", "IIFM Bhopal. 250+ teams."),
            ("2nd Runner-Up · Nov 2025", "3rd", "Chakravyuh B-Plan", "CVS, Delhi University."),
            ("24-hour build", "24h", "AI HackMatrix", "Chandigarh University.")]
    for i, (eb, big, title, sub) in enumerate(row2):
        tx = PAD + i * (tw + g)
        parts.append(f'''<g class="up d{3 + i}">
{tile(tx, r2y, tw, r2h)}
{t(tx + 30, r2y + 44, eb, 13, 600, GRAY)}
{t(tx + 28, r2y + 120, big, 56, 600, INK, ls=-1.8)}
{t(tx + 30, r2y + 164, title, 20, 600, INK, ls=-.3)}
{t(tx + 30, r2y + 190, sub, 14, 400, GRAY)}
</g>''')

    r3y, r3h = r2y + r2h + g, 124
    parts.append(f'<g class="up d6">{tile(PAD, r3y, inner, r3h)}')
    parts.append(t(PAD + 40, r3y + 42, "Also pitched at", 13, 600, GRAY))
    stages = [("IIT Bombay", "National Entrepreneurship Challenge"),
              ("IIM Bangalore", "Pitch Perfect, Season 8"),
              ("BHU, Varanasi", "Bharat Innovation Conclave")]
    cw = (inner - 80) / 3
    for i, (name, det) in enumerate(stages):
        cx = PAD + 40 + i * cw
        parts.append(t(cx, r3y + 80, name, 19, 600, INK, ls=-.3))
        parts.append(t(cx, r3y + 103, det, 14, 400, GRAY))
        if i:
            parts.append(hair(cx - 24, r3y + 62, cx - 24, r3y + 106))
    parts.append("</g>")
    return frame(r3y + r3h + PAD, "\n".join(parts))


# =====================================================================
# 5. HARDINI (black product panel)
# =====================================================================
def hardini():
    h = 560
    cx, cy = 760, 280
    heights = [14, 24, 38, 54, 44, 72, 92, 62, 106, 80, 120, 100, 120, 80, 106, 62, 92, 72, 44, 54, 38, 24, 14]
    n, sp = len(heights), 11
    bars = []
    for i, bh in enumerate(heights):
        x = cx + (i - n // 2) * sp
        delay = abs(i - n // 2) * .09
        bars.append(f'<line class="bar" style="animation-delay:-{delay:.2f}s" x1="{x}" y1="{cy - bh / 2:.1f}" '
                    f'x2="{x}" y2="{cy + bh / 2:.1f}" stroke="{INK_DARK}" stroke-width="4.5" stroke-linecap="round"/>')
    greet = [("नमस्ते", cx - 150, cy - 138, 0), ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", cx + 120, cy - 116, 1.5),
             ("வணக்கம்", cx - 158, cy + 158, 3), ("నమస్కారం", cx + 128, cy + 148, 4.5),
             ("নমস্কার", cx + 166, cy + 12, 6), ("Hello", cx - 196, cy + 10, 7.5)]
    gtxt = "".join(f'<text class="greet" style="animation-delay:{d}s" x="{x}" y="{y}" font-size="16" '
                   f'font-weight="400" fill="{GRAY2}" text-anchor="middle">{escape(s)}</text>'
                   for s, x, y, d in greet)
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{o}"/>'
                    for r, o in [(116, .14), (176, .08), (236, .045)])
    lx = PAD + 8
    body = f'''
{rings}
{"".join(bars)}
{gtxt}
{t(lx, 124, "Featured project", 14, 600, GRAY2, cls="up d1")}
{t(lx - 3, 200, "Hardini", 80, 600, INK_DARK, ls=-2.4, cls="up d2")}
{t(lx, 250, "Ask anything. In your own language.", 26, 400, INK_DARK, ls=-.5, cls="up d3")}
{t(lx, 298, "A voice AI platform for India’s farmers. Crop", 17, 400, GRAY2, cls="up d4")}
{t(lx, 322, "diseases, mandi prices, weather and government", 17, 400, GRAY2, cls="up d4")}
{t(lx, 346, "schemes. Answered instantly, in their native tongue.", 17, 400, GRAY2, cls="up d4")}
<g class="up d5">
{hair(lx, 400, lx + 400, 400, HAIR_DARK)}
{t(lx, 436, "Built in 24 hours at AI HackMatrix, Chandigarh University.", 14, 400, GRAY2)}
{t(lx, 460, "1st Runner-Up at Spark Tank, IIFM Bhopal. 250+ teams.", 14, 400, GRAY2)}
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
# 6. THE PROCESS
# =====================================================================
def process():
    y, th = 184, 400
    inner = W - 2 * PAD
    g = 20
    tw = (inner - 2 * g) / 3
    parts = [heading("The process.", "Every detail considered. From the first interview to launch day.")]
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
        x = PAD + i * (tw + g)
        ix = x + 30
        parts.append(f'<g class="up d{3 + i}">{tile(x, y, tw, th)}')
        parts.append(t(ix, y + 58, title, 24, 600, INK, ls=-.5))
        for k, it in enumerate(items):
            iy = y + 116 + k * 40
            parts.append(t(ix, iy, it, 16, 400, INK, ls=-.1))
            if k < len(items) - 1:
                parts.append(hair(ix, iy + 16, x + tw - 30, iy + 16))
        parts.append("</g>")

    by, bh = y + th + g, 156
    bw = (inner - g) / 2
    blocks = [
        ("Certified", "Agile Project Management", "Professional Certificate, Atlassian. Aug 2026.", ["Agile", "Jira"]),
        ("Community", "Event Coordinator", "Lloyd Institute of Engineering and Technology. Dec 2025.", []),
    ]
    for i, (eb, title, sub, chips) in enumerate(blocks):
        x = PAD + i * (bw + g)
        ix = x + 32
        parts.append(f'<g class="up d{5 + i}">{tile(x, by, bw, bh)}')
        parts.append(t(ix, by + 46, eb, 13, 600, GRAY))
        parts.append(t(ix, by + 86, title, 23, 600, INK, ls=-.5))
        parts.append(t(ix, by + 116, sub, 14, 400, GRAY))
        cx = x + bw - 32
        for c in reversed(chips):
            w = 18 + len(c) * 8
            cx -= w
            parts.append(pill(cx, by + 28, w, c))
            cx -= 8
        parts.append("</g>")
    return frame(by + bh + PAD, "\n".join(parts))


# =====================================================================
# 7. FOOTER
# =====================================================================
def footer():
    h = 360
    body = f'''
{t(500, 160, "Let’s make something great.", 52, 600, INK, "middle", -1.4, "up d1")}
{t(500, 206, "Open to conversations about AI products, voice and building for India.", 19, 400, GRAY, "middle", -.1, "up d2")}
{hair(PAD, 276, W - PAD, 276)}
{t(PAD, 310, "Designed by Lal Aman Singh in Noida.", 12, 400, GRAY2, cls="up d3")}
{t(W - PAD, 310, "github.com/lalamansingh", 12, 400, GRAY2, "end", cls="up d3")}
'''
    return frame(h, body)


PANELS = {"hero": hero, "stats": stats, "experience": experience, "recognition": recognition,
          "hardini": hardini, "process": process, "footer": footer}

if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        if old.stem not in PANELS:
            old.unlink()
    for name, fn in PANELS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")

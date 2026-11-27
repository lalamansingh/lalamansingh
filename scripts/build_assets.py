#!/usr/bin/env python3
"""Generates the SVG panels used by README.md.

Edit the content below and run:  python3 scripts/build_assets.py
Every panel is 1000px wide and shares one set of design tokens, so spacing,
type and colour stay consistent across the whole profile.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

W = 1000
PAD = 56  # outer margin inside every panel

# ---------- design tokens ----------
BG = "#000000"
TILE = "#161617"
TEXT = "#f5f5f7"
TEXT2 = "#a1a1a6"
TEXT3 = "#86868b"
TEXT4 = "#6e6e73"
GREEN = "#30d158"
AI = ["#ff9f0a", "#ff375f", "#bf5af2", "#5e5ce6", "#0a84ff"]

FONT = ('-apple-system, BlinkMacSystemFont, &quot;SF Pro Display&quot;, &quot;SF Pro Text&quot;, '
        'Inter, &quot;Segoe UI&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif')

BASE_CSS = """
text{font-family:FONT_STACK;}
.up{animation:up 1.1s cubic-bezier(.16,1,.3,1) both;}
.d1{animation-delay:.08s}.d2{animation-delay:.18s}.d3{animation-delay:.28s}
.d4{animation-delay:.38s}.d5{animation-delay:.48s}.d6{animation-delay:.58s}
@keyframes up{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:none}}
.drift1{animation:drift1 14s ease-in-out infinite alternate;}
.drift2{animation:drift2 17s ease-in-out infinite alternate;}
.drift3{animation:drift3 12s ease-in-out infinite alternate;}
@keyframes drift1{to{transform:translate(70px,-18px)}}
@keyframes drift2{to{transform:translate(-80px,10px)}}
@keyframes drift3{to{transform:translate(40px,14px)}}
.pulse{animation:pulse 2.4s ease-out infinite;transform-box:fill-box;transform-origin:center;}
@keyframes pulse{0%{opacity:.6;transform:scale(1)}100%{opacity:0;transform:scale(3.2)}}
""".replace("FONT_STACK", FONT)


def t(x, y, s, size, weight=400, fill=TEXT, anchor="start", ls=0, cls="", extra=""):
    ls_attr = f' letter-spacing="{ls}"' if ls else ""
    cls_attr = f' class="{cls}"' if cls else ""
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}"{ls_attr}{cls_attr}{extra}>{escape(s)}</text>')


def ai_gradient(gid="ai", x1=180, x2=820, shimmer=True):
    stops = "".join(f'<stop offset="{i / (len(AI) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(AI))
    anim = ""
    if shimmer:
        anim = (f'<animateTransform attributeName="gradientTransform" type="translate" '
                f'values="0 0;{x2 - x1} 0;0 0" dur="14s" repeatCount="indefinite"/>')
    return (f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="{x1}" y1="0" x2="{x2}" y2="0" '
            f'spreadMethod="reflect">{stops}{anim}</linearGradient>')


def frame(h, body, defs="", css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img">
<defs>
<style>{BASE_CSS}{css}</style>
<clipPath id="card"><rect x="0" y="0" width="{W}" height="{h}" rx="30"/></clipPath>
<filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="56"/></filter>
<filter id="blurS" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="34"/></filter>
{ai_gradient()}
{defs}
</defs>
<rect x="0" y="0" width="{W}" height="{h}" rx="30" fill="{BG}"/>
<g clip-path="url(#card)">
{body}
</g>
<rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="29.5" fill="none" stroke="#fff" stroke-opacity=".09"/>
</svg>'''


def glow(cy, spread=1.0, opacity=1.0):
    """Apple Intelligence style multicolour glow, centred horizontally at height cy."""
    blobs = [
        (300, AI[2], 270, .62, "drift1"),
        (520, AI[1], 280, .50, "drift2"),
        (730, AI[4], 250, .58, "drift3"),
        (470, AI[0], 170, .38, "drift1"),
    ]
    out = []
    for cx, col, rx, op, cls in blobs:
        out.append(f'<ellipse class="{cls}" cx="{cx}" cy="{cy}" rx="{rx * spread:.0f}" ry="{110 * spread:.0f}" '
                   f'fill="{col}" opacity="{op * opacity:.2f}" filter="url(#blur)"/>')
    return "\n".join(out)


def tile(x, y, w, h, fill=TILE, rx=22):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"/>'
            f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{rx - .5}" fill="none" '
            f'stroke="#fff" stroke-opacity=".06"/>')


def pill(x, y, w, label, h=36, filled=False, size=14):
    if filled:
        r = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="{TEXT}"/>'
        col = "#1d1d1f"
    else:
        r = (f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="{(h - 1) / 2}" '
             f'fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".22"/>')
        col = TEXT
    return r + t(x + w / 2, y + h / 2 + size * .36, label, size, 600, col, "middle")


def section_title(title, sub):
    return (t(PAD, 104, title, 52, 700, TEXT, ls=-1.6, cls="up d1") +
            t(PAD, 142, sub, 21, 400, TEXT3, cls="up d2"))


# =====================================================================
# 1. HERO
# =====================================================================
def hero():
    h = 600
    pills_w = (300, 268)
    gap = 14
    x0 = (W - sum(pills_w) - gap) / 2
    body = f'''
{glow(650)}
{t(500, 156, "AI PRODUCT MANAGER", 14, 700, "url(#ai)", "middle", 3.2, "up d1")}
{t(500, 258, "Lal Aman Singh.", 90, 700, TEXT, "middle", -3, "up d2")}
{t(500, 322, "Conversations in. Value out.", 34, 600, "url(#ai)", "middle", -.6, "up d3")}
{t(500, 374, "I design and ship voice AI that speaks India’s languages.", 21, 400, TEXT2, "middle", 0, "up d4")}
<g class="up d5">
{pill(x0, 418, pills_w[0], "AI Product Intern at IndusLabs", 46, True, 16)}
{pill(x0 + pills_w[0] + gap, 418, pills_w[1], "8× National Hackathon Winner", 46, False, 16)}
</g>
{t(500, 548, "Noida, India   ·   He/Him", 14, 500, TEXT, "middle", .4, "up d6", ' fill-opacity=".72"')}
'''
    return frame(h, body)


# =====================================================================
# 2. STATS STRIP
# =====================================================================
def stats():
    h = 236
    items = [
        ("8×", "National hackathon", "wins"),
        ("250+", "Teams in the field at", "Spark Tank, IIFM"),
        ("2", "Product", "internships"),
        ("#1", "Rank at Design Spark,", "Intellect Design Arena"),
    ]
    col = W / 4
    parts = []
    for i, (num, l1, l2) in enumerate(items):
        cx = col * i + col / 2
        d = f"d{i + 1}"
        parts.append(t(cx, 116, num, 64, 700, "url(#ai)", "middle", -2, f"up {d}"))
        parts.append(t(cx, 156, l1, 15, 400, TEXT3, "middle", 0, f"up {d}"))
        parts.append(t(cx, 178, l2, 15, 400, TEXT3, "middle", 0, f"up {d}"))
        if i:
            parts.append(f'<line x1="{col * i}" y1="62" x2="{col * i}" y2="178" stroke="#fff" stroke-opacity=".1"/>')
    return frame(h, "\n".join(parts))


# =====================================================================
# 3. EXPERIENCE
# =====================================================================
def experience():
    h = 540
    y = 180
    th = 304
    tw = (W - 2 * PAD - 16) / 2
    jobs = [
        dict(x=PAD, now=True, status="Now", date="Aug 2026 – Present", role="AI Product Intern",
             company="IndusLabs", desc=["Building voice AI agents that speak", "India’s languages."],
             foot="On-site  ·  Noida  ·  4 mos"),
        dict(x=PAD + tw + 16, now=False, status="Completed", date="Feb – Jul 2026", role="Product Manager Intern",
             company="RYM Grenergy", desc=["A six-month product management", "internship."],
             foot="Internship  ·  6 mos"),
    ]
    parts = [section_title("Experience.", "Where products meet people.")]
    for i, j in enumerate(jobs):
        x = j["x"]
        ix = x + 36
        d = f"up d{i + 3}"
        dot = GREEN if j["now"] else TEXT4
        pulse = (f'<circle class="pulse" cx="{ix + 6}" cy="{y + 44}" r="5" fill="{GREEN}"/>' if j["now"] else "")
        parts.append(f'''<g class="{d}">
{tile(x, y, tw, th)}
{pulse}<circle cx="{ix + 6}" cy="{y + 44}" r="5" fill="{dot}"/>
{t(ix + 20, y + 49, j["status"], 14, 600, dot if j["now"] else TEXT3, ls=.3)}
{t(x + tw - 36, y + 49, j["date"], 14, 500, TEXT3, "end")}
{t(ix, y + 120, j["role"], 29, 700, TEXT, ls=-.6)}
{t(ix, y + 156, j["company"], 22, 600, "url(#ai)")}
{t(ix, y + 206, j["desc"][0], 17, 400, TEXT2)}
{t(ix, y + 230, j["desc"][1], 17, 400, TEXT2)}
<line x1="{ix}" y1="{y + 258}" x2="{x + tw - 36}" y2="{y + 258}" stroke="#fff" stroke-opacity=".07"/>
{t(ix, y + 284, j["foot"], 13, 500, TEXT4, ls=.2)}
</g>''')
    return frame(h, "\n".join(parts))


# =====================================================================
# 4. RECOGNITION (bento grid)
# =====================================================================
def recognition():
    h = 926
    g = 16
    inner = W - 2 * PAD
    parts = [section_title("Recognition.", "8 national hackathon wins, leading product in 24–48 hour sprints.")]

    # --- big tile: Design Spark
    bx, by, bw, bh = PAD, 180, 528, 300
    parts.append(f'''<g class="up d3">
{tile(bx, by, bw, bh)}
<g clip-path="url(#bigclip)"><circle cx="{bx + 150}" cy="{by + 175}" r="120" fill="url(#ai)" opacity=".2" filter="url(#blurS)"/></g>
{t(bx + 40, by + 50, "NATIONAL CHALLENGE", 13, 600, TEXT3, ls=1.6)}
{pill(bx + bw - 40 - 200, by + 28, 200, "Cash award + internship", 32, False, 13)}
{t(bx + 34, by + 166, "1st", 128, 800, "url(#ai)", ls=-5)}
{t(bx + 40, by + 212, "Design Spark Challenge", 28, 700, TEXT, ls=-.5)}
{t(bx + 40, by + 242, "Intellect Design Arena, Chennai", 15, 500, TEXT3)}
{t(bx + 40, by + 270, "Banking-product challenge  ·  Multi-agent AI system", 15, 400, TEXT2)}
</g>''')

    # --- two stacked tiles on the right
    rx_, rw, rh = bx + bw + g, inner - bw - g, (bh - g) / 2
    right = [
        ("WINNER  ·  OCT 2025", "National Level", "Tech Hackathon", "Kanpur  ·  Team Aspirofy", "1st"),
        ("WINNER  ·  JUL 2025", "AI Product", "Builder", "Jivika Future Work", "1st"),
    ]
    for i, (eb, l1, l2, sub, big) in enumerate(right):
        ty = by + i * (rh + g)
        parts.append(f'''<g class="up d{4 + i}">
{tile(rx_, ty, rw, rh)}
{t(rx_ + 28, ty + 40, eb, 12, 600, TEXT3, ls=1.5)}
{t(rx_ + 28, ty + 74, l1, 20, 700, TEXT, ls=-.3)}
{t(rx_ + 28, ty + 98, l2, 20, 700, TEXT, ls=-.3)}
{t(rx_ + 28, ty + 124, sub, 14, 400, TEXT3)}
{t(rx_ + rw - 28, ty + 104, big, 54, 800, "url(#ai)", "end", -2)}
</g>''')

    # --- row 2: three tiles
    r2y, r2h = by + bh + g, 230
    tw = (inner - 2 * g) / 3
    row2 = [
        ("1ST RUNNER-UP  ·  OCT 2025", "#2", "Spark Tank", "of 250+ teams  ·  IIFM Bhopal"),
        ("2ND RUNNER-UP  ·  NOV 2025", "#3", "Chakravyuh B-Plan", "CVS, Delhi University"),
        ("24-HOUR BUILD", "24h", "AI HackMatrix", "Chandigarh University"),
    ]
    for i, (eb, big, title, sub) in enumerate(row2):
        tx = PAD + i * (tw + g)
        parts.append(f'''<g class="up d{3 + i}">
{tile(tx, r2y, tw, r2h)}
{t(tx + 28, r2y + 44, eb, 12, 600, TEXT3, ls=1.5)}
{t(tx + 26, r2y + 128, big, 64, 800, "url(#ai)", ls=-2.5)}
{t(tx + 28, r2y + 172, title, 21, 700, TEXT, ls=-.4)}
{t(tx + 28, r2y + 198, sub, 14, 400, TEXT3)}
</g>''')

    # --- row 3: also pitched at
    r3y, r3h = r2y + r2h + g, 128
    parts.append(f'<g class="up d6">{tile(PAD, r3y, inner, r3h)}')
    parts.append(t(PAD + 40, r3y + 42, "ALSO PITCHED AT", 12, 600, "url(#ai)", ls=1.8))
    stages = [("IIT Bombay", "National Entrepreneurship Challenge"),
              ("IIM Bangalore", "Pitch Perfect, Season 8"),
              ("BHU, Varanasi", "Bharat Innovation Conclave")]
    cw = (inner - 80) / 3
    for i, (name, det) in enumerate(stages):
        cx = PAD + 40 + i * cw
        parts.append(t(cx, r3y + 82, name, 20, 700, TEXT, ls=-.3))
        parts.append(t(cx, r3y + 106, det, 14, 400, TEXT3))
        if i:
            parts.append(f'<line x1="{cx - 24}" y1="{r3y + 64}" x2="{cx - 24}" y2="{r3y + 110}" stroke="#fff" stroke-opacity=".08"/>')
    parts.append("</g>")

    defs = f'<clipPath id="bigclip"><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="22"/></clipPath>'
    return frame(h, "\n".join(parts), defs)


# =====================================================================
# 5. FEATURED PROJECT: HARDINI
# =====================================================================
def hardini():
    h = 560
    cx, cy = 760, 280
    bars = []
    n = 23
    spacing = 11
    heights = [18, 30, 46, 64, 52, 84, 104, 72, 118, 92, 130, 112, 130, 92, 118, 72, 104, 84, 52, 64, 46, 30, 18]
    for i in range(n):
        x = cx + (i - n // 2) * spacing
        bh = heights[i]
        delay = (abs(i - n // 2) * 0.09)
        bars.append(f'<line class="bar" style="animation-delay:-{delay:.2f}s" x1="{x}" y1="{cy - bh / 2:.1f}" '
                    f'x2="{x}" y2="{cy + bh / 2:.1f}" stroke="url(#aiV)" stroke-width="5" stroke-linecap="round"/>')
    greet = [
        ("नमस्ते", cx - 150, cy - 140, 0),
        ("ਸਤ ਸ੍ਰੀ ਅਕਾਲ", cx + 120, cy - 118, 1.5),
        ("வணக்கம்", cx - 160, cy + 160, 3),
        ("నమస్కారం", cx + 130, cy + 150, 4.5),
        ("নমস্কার", cx + 168, cy + 12, 6),
        ("Hello", cx - 200, cy + 10, 7.5),
    ]
    g_parts = "".join(
        f'<text class="greet" style="animation-delay:{d}s" x="{x}" y="{y}" font-size="17" font-weight="500" '
        f'fill="{TEXT}" text-anchor="middle">{escape(s)}</text>' for s, x, y, d in greet)

    chips = [("Real-time voice", 148), ("Multilingual", 124), ("Built in 24h", 118)]
    chip_svg, x = [], PAD + 8
    for label, w in chips:
        chip_svg.append(pill(x, 352, w, label, 36, False, 14))
        x += w + 10

    body = f'''
<circle class="breathe" cx="{cx}" cy="{cy}" r="150" fill="url(#ai)" opacity=".34" filter="url(#blur)"/>
<circle cx="{cx}" cy="{cy}" r="118" fill="none" stroke="#fff" stroke-opacity=".10"/>
<circle cx="{cx}" cy="{cy}" r="178" fill="none" stroke="#fff" stroke-opacity=".06"/>
<circle cx="{cx}" cy="{cy}" r="238" fill="none" stroke="#fff" stroke-opacity=".035"/>
{"".join(bars)}
{g_parts}
{t(PAD + 8, 120, "FEATURED PROJECT", 13, 700, "url(#ai)", ls=2.4, cls="up d1")}
{t(PAD + 4, 198, "Hardini.", 76, 800, TEXT, ls=-3, cls="up d2")}
{t(PAD + 8, 246, "Voice AI for every farmer in Bharat.", 24, 600, "#d2d2d7", ls=-.4, cls="up d3")}
{t(PAD + 8, 294, "Crop diseases, mandi prices, weather and", 17, 400, TEXT3, cls="up d4")}
{t(PAD + 8, 318, "government schemes, in the farmer’s own language.", 17, 400, TEXT3, cls="up d4")}
<g class="up d5">{"".join(chip_svg)}</g>
<g class="up d6">
<line x1="{PAD + 8}" y1="430" x2="{PAD + 420}" y2="430" stroke="#fff" stroke-opacity=".08"/>
<circle cx="{PAD + 12}" cy="463" r="4" fill="url(#ai)"/>
{t(PAD + 26, 468, "1st Runner-Up, Spark Tank, IIFM Bhopal (250+ teams)", 14, 500, TEXT2)}
<circle cx="{PAD + 12}" cy="491" r="4" fill="url(#ai)"/>
{t(PAD + 26, 496, "Built in 24 hours at AI HackMatrix, Chandigarh University", 14, 500, TEXT2)}
</g>
'''
    stops = "".join(f'<stop offset="{i / (len(AI) - 1):.2f}" stop-color="{c}"/>' for i, c in enumerate(AI))
    defs = (f'<linearGradient id="aiV" gradientUnits="userSpaceOnUse" x1="{cx - 130}" y1="0" x2="{cx + 130}" y2="0">'
            f'{stops}</linearGradient>')
    css = """
.bar{animation:wave 1.6s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center;}
@keyframes wave{0%{transform:scaleY(.25)}100%{transform:scaleY(1)}}
.breathe{animation:breathe 5s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center;}
@keyframes breathe{0%{transform:scale(.85);opacity:.22}100%{transform:scale(1.1);opacity:.42}}
.greet{opacity:0;animation:greet 9s ease-in-out infinite;}
@keyframes greet{0%,100%{opacity:0}12%,40%{opacity:.85}55%{opacity:0}}
"""
    return frame(h, body, defs, css)


# =====================================================================
# 6. HOW I WORK
# =====================================================================
def toolkit():
    y, th = 180, 352
    inner = W - 2 * PAD
    g = 16
    tw = (inner - 2 * g) / 3
    parts = [section_title("How I work.", "From user research to launch, with AI in the loop.")]
    lists = [
        ("PRODUCT", ["User research", "Requirements & PRDs", "User stories", "RICE · P0/P1 priorities",
                     "Roadmaps", "Market research", "Competitive analysis"]),
        ("DELIVERY", ["Product launch", "Agile · Scrum & Kanban", "Testing, QA & edge cases",
                      "Iterative development", "Cross-functional work", "Stakeholder updates",
                      "Technical presentations"]),
        ("AI & TOOLS", ["Voice AI & speech-to-text", "LLM prototyping", "AI/ML product design",
                        "Python for automation", "SQL (basic)", "Figma flows & wireframes", "Jira · Notion"]),
    ]
    for i, (eb, items) in enumerate(lists):
        x = PAD + i * (tw + g)
        parts.append(f'<g class="up d{3 + i}">{tile(x, y, tw, th)}')
        parts.append(t(x + 30, y + 50, eb, 13, 700, "url(#ai)", ls=2.2))
        for k, it in enumerate(items):
            iy = y + 100 + k * 36
            parts.append(f'<circle cx="{x + 34}" cy="{iy - 5.5}" r="2.5" fill="url(#ai)"/>')
            parts.append(t(x + 48, iy, it, 16.5, 500, TEXT, ls=-.2))
        parts.append("</g>")

    # bottom row: certification + beyond work
    by, bh = y + th + g, 172
    bw = (inner - g) / 2
    cx = PAD
    parts.append(f'''<g class="up d5">
{tile(cx, by, bw, bh)}
{t(cx + 32, by + 46, "CERTIFIED", 13, 700, "url(#ai)", ls=2.2)}
{t(cx + 32, by + 86, "Agile Project Management", 23, 700, TEXT, ls=-.5)}
{t(cx + 32, by + 114, "Professional Certificate  ·  Atlassian", 15, 400, TEXT2)}
{t(cx + 32, by + 146, "Issued Aug 2026", 13, 500, TEXT4)}
{pill(cx + bw - 32 - 64 - 8 - 76, by + 124, 76, "Agile", 30, False, 13)}
{pill(cx + bw - 32 - 64, by + 124, 64, "Jira", 30, False, 13)}
</g>''')
    vx = PAD + bw + g
    parts.append(f'''<g class="up d6">
{tile(vx, by, bw, bh)}
{t(vx + 32, by + 46, "BEYOND WORK", 13, 700, "url(#ai)", ls=2.2)}
{t(vx + 32, by + 86, "Event Coordinator", 23, 700, TEXT, ls=-.5)}
{t(vx + 32, by + 114, "Lloyd Institute of Engineering and Technology", 15, 400, TEXT2)}
{t(vx + 32, by + 146, "Dec 2025", 13, 500, TEXT4)}
</g>''')
    return frame(by + bh + PAD, "\n".join(parts))


# =====================================================================
# 7. FOOTER
# =====================================================================
def footer():
    h = 420
    body = f'''
{glow(-70, .9, .8)}
{t(500, 178, "Let’s build what’s next.", 58, 700, TEXT, "middle", -2, "up d1")}
{t(500, 226, "Open to conversations on AI products, voice and Bharat-first tech.", 20, 400, TEXT2, "middle", 0, "up d2")}
<line class="up d3" x1="420" y1="296" x2="580" y2="296" stroke="url(#ai)" stroke-width="1.5"/>
{t(500, 344, "Conversations in. Value out.", 16, 600, "url(#ai)", "middle", .2, "up d4")}
{t(500, 372, "Designed and built by Lal Aman Singh in Noida, India.", 13, 400, TEXT4, "middle", .2, "up d5")}
'''
    return frame(h, body)


PANELS = {
    "hero": hero, "stats": stats, "experience": experience, "recognition": recognition,
    "hardini": hardini, "toolkit": toolkit, "footer": footer,
}

if __name__ == "__main__":
    for name, fn in PANELS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")

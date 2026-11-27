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
        t(PAD, 118, "Product Thinking & User-Centric Design.", 20, 400, INK, ls=-.3, cls="up d2"),
        t(PAD, 145, "Bridging users ⇄ tech ⇄ business.", 15, 400, GRAY, cls="up d2"),
        t(PAD, 170, "AI Product Intern at IndusLabs  ·  Noida, India", 13, 400, GRAY2, cls="up d3"),
    ]
    # highlighted "at a glance" box
    stats = [("8", "National", "hackathon wins"), ("2", "Product", "internships")]
    sw, bh = 150, 128
    bw = sw * len(stats) + 20
    bx, by = W - PAD - bw, 44
    parts.append(f'''<g class="up d3">
<defs><filter id="liftI" x="-15%" y="-20%" width="130%" height="150%">
<feDropShadow dx="0" dy="4" stdDeviation="9" flood-color="#000" flood-opacity=".08"/></filter></defs>
<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="16" fill="{TILE}" filter="url(#liftI)"/>
{t(bx + 22, by + 28, "At a glance", 11, 600, NEW)}''')
    for i, (n, l1, l2) in enumerate(stats):
        cx = bx + 10 + i * sw + sw / 2
        parts.append(t(cx, by + 72, n, 38, 600, INK, "middle", -1))
        parts.append(t(cx, by + 95, l1, 12, 400, GRAY, "middle"))
        parts.append(t(cx, by + 111, l2, 12, 400, GRAY, "middle"))
        if i:
            parts.append(hair(bx + 10 + i * sw, by + 46, bx + 10 + i * sw, by + 112))
    parts.append("</g>")

    y, th = 196, 128
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
# 2. RECOGNITION (3x3, soft glow)
# =====================================================================
# (big label, top-right note, title, subtitle, is_first_place)
WINS = [
    ("1st", "Cash award + internship", "Design Spark Challenge", "Intellect Design Arena, Chennai.", True),
    ("1st", "Oct 2025", "National Level Tech Hackathon", "Dr. Virendra Swarup Institute, Kanpur.", True),
    ("1st", "Jul 2025", "AI Product Builder", "Jivika Future Work Pvt. Ltd.", True),
    ("2nd", "Oct 2025", "Spark Tank", "IIFM Bhopal. Runner-up of 250+ teams.", False),
    ("3rd", "Nov 2025", "Chakravyuh B-Plan", "CVS, Delhi University. 2nd Runner-Up.", False),
    ("24h", "24-hour build", "AI HackMatrix", "Chandigarh University. Built Hardini.", False),
]

# (name, detail, x, measured SF Pro Semibold width of name at 13.5px)
PITCHED = [
    ("IIT Bombay", ", National Entrepreneurship Challenge", 156, 66.6),
    ("IIM Bangalore", ", Pitch Perfect, Season 8", 480, 81.5),
    ("BHU", ", Bharat Innovation Conclave", 744, 27.4),
]

def recognition():
    parts = [heading("Recognition.", "Eight national wins. Each one built in hours, not months.")]
    parts.append(f'''<defs>
<filter id="lift" x="-10%" y="-20%" width="120%" height="150%">
  <feDropShadow dx="0" dy="4" stdDeviation="9" flood-color="#000" flood-opacity=".07"/>
</filter>
<linearGradient id="sheenInk" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{INK}"/><stop offset=".42" stop-color="{INK}"/>
  <stop offset=".5" stop-color="#8e8e93"/><stop offset=".58" stop-color="{INK}"/><stop offset="1" stop-color="{INK}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="sheenNew" x1="0" y1="0" x2="1" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{NEW}"/><stop offset=".42" stop-color="{NEW}"/>
  <stop offset=".5" stop-color="#e3893f"/><stop offset=".58" stop-color="{NEW}"/><stop offset="1" stop-color="{NEW}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/>
</linearGradient>
</defs>''')
    cols, th = 3, 108
    tw = (INNER - (cols - 1) * GAP) / cols
    for i, (big, note, title, sub, first) in enumerate(WINS):
        x = PAD + (i % cols) * (tw + GAP)
        y = HEAD_H + (i // cols) * (th + GAP)
        ix = x + 22
        d = 3 + i % cols + i // cols
        parts.append(f'<g class="up d{min(d, 6)}">')
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" rx="14" fill="{TILE}" filter="url(#lift)"/>')
        parts.append(t(ix, y + 44, big, 30, 600, "url(#sheenNew)" if first else "url(#sheenInk)", ls=-.8))
        parts.append(t(x + tw - 20, y + 28, note, 11, 500, NEW if first else GRAY2, "end"))
        parts.append(t(ix, y + 74, title, 16, 600, INK, ls=-.25))
        parts.append(t(ix, y + 93, sub, 12.5, 400, GRAY))
        parts.append("</g>")
    rows = (len(WINS) + cols - 1) // cols
    ly = HEAD_H + rows * th + (rows - 1) * GAP + 40
    parts.append(t(PAD, ly, "Also pitched at", 13.5, 400, GRAY, cls="up d6"))
    for k, (name, det, x, w) in enumerate(PITCHED):
        hw = w * 1.03 + 6
        parts.append(f'<rect class="mark" style="animation-delay:{.7 + k * .45:.2f}s" x="{x - 3}" y="{ly - 12.5}" '
                     f'width="{hw:.1f}" height="17" rx="3" fill="#ffcc00" fill-opacity=".42"/>')
        parts.append(f'<text x="{x}" y="{ly}" font-size="13.5" class="up d6">'
                     f'<tspan font-weight="600" fill="{INK}">{escape(name)}</tspan>'
                     f'<tspan font-weight="400" fill="{GRAY}">{escape(det)}</tspan></text>')
    css = """
.mark{transform:scaleX(0);transform-box:fill-box;transform-origin:left center;
  animation:mark .7s cubic-bezier(.3,.6,.3,1) forwards;}
@keyframes mark{to{transform:scaleX(1)}}
"""
    return frame(ly + 34, "\n".join(parts), CANVAS, css)


# =====================================================================
# 3. PROJECTS (public repositories)
# =====================================================================
# (name, tagline, category, live, description, stack tags)
PROJECTS = [
    ("FirstRecord", "Policing, in every language.", "Voice AI", True,
     "Police case and statement records, driven by a Hindi and English voice assistant.",
     ["Claude Sonnet 5.5", "Whisper", "Next.js"]),
    ("PhishGuard", "Know before you click.", "Security ML", False,
     "Four ML classifiers and 50+ live checks score any URL for phishing. ROC-AUC 0.945.",
     ["Random Forest", "scikit-learn", "FastAPI"]),
    ("TruthLens", "See what’s real.", "Computer vision", False,
     "Deepfake and AI-image detection with face forensics and inpainting restoration.",
     ["SigLIP", "OpenCV YuNet", "PyTorch"]),
    ("ORCA", "Oceans, reasoned.", "Multi-agent AI", True,
     "Marine risk intelligence. Planned by AI agents, backed by evidence.",
     ["LangGraph", "FastAPI", "PostGIS"]),
    ("ATS Resume Scorer", "Get past the filter.", "NLP", True,
     "Semantic ATS scoring against a job description, with SQL and prompt-injection detection.",
     ["Sentence-Transformers", "PyTorch"]),
    ("X-Green Tracker", "Bugs, simplified.", "Dev tools", False,
     "A self-hosted Jira alternative with a speech-to-speech AI assistant built in.",
     ["Gemini Live", "Supabase", "Next.js"]),
    ("Real or Rendered?", "Train your eyes.", "AI literacy", True,
     "A five-minute daily game. Spot AI-made images, voices and videos, then learn the clues.",
     ["Next.js 15", "Drizzle", "Postgres"]),
    ("Aspirofy Roadmaps", "Learning, mapped.", "EdTech", True,
     "Interactive learning roadmaps with built-in progress tracking and analytics.",
     ["React 19", "Zustand", "Recharts"]),
]


def tag_w(label):
    return 14 + len(label) * 5.9


def wrap(s, n):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def projects():
    parts = [heading("Projects.", "Eight ideas, taken all the way to working code.")]
    cols = 4
    tw = (INNER - (cols - 1) * GAP) / cols

    def tag_rows(tags):
        n, cx = 1, 0
        for tg in tags:
            w = tag_w(tg)
            if cx and cx + w > tw - 40:
                n, cx = n + 1, 0
            cx += w + 6
        return n

    th = 164 + max(tag_rows(p[5]) for p in PROJECTS) * 26 + 6
    for i, (name, tag, cat, live, desc, stack) in enumerate(PROJECTS):
        x = PAD + (i % cols) * (tw + GAP)
        y = HEAD_H + (i // cols) * (th + GAP)
        ix = x + 20
        lines = wrap(desc, 31)
        assert len(lines) <= 3, name
        parts.append(f'<g class="up d{3 + i % cols}">{tile(x, y, tw, th)}')
        parts.append(t(ix, y + 30, cat, 11, 600, GRAY))
        if live:
            parts.append(t(x + tw - 20, y + 30, "Live", 11, 600, NEW, "end"))
        parts.append(t(ix, y + 58, name, 17, 600, INK, ls=-.3))
        parts.append(t(ix, y + 78, tag, 13, 400, INK))
        parts.append(hair(ix, y + 92, x + tw - 20, y + 92))
        for k, ln in enumerate(lines):
            parts.append(t(ix, y + 113 + k * 17, ln, 12, 400, GRAY))
        cx, cy = ix, y + 164
        for tg in stack:
            w = tag_w(tg)
            if cx > ix and cx + w > x + tw - 20:
                cx, cy = ix, cy + 26
            parts.append(f'<rect x="{cx:.1f}" y="{cy}" width="{w:.1f}" height="20" rx="10" fill="{CANVAS}"/>')
            parts.append(t(cx + w / 2, cy + 14, tg, 11, 500, INK, "middle"))
            cx += w + 6
        parts.append("</g>")
    end = HEAD_H + 2 * th + GAP
    parts.append(t(W / 2, end + 36, "Every project is open source. Explore them in the repositories below.",
                   12, 400, GRAY2, "middle", 0, "up d6"))
    return frame(end + 60, "\n".join(parts))


# =====================================================================
# 4. THE PROCESS
# =====================================================================

STEPS = [
    ("Discover.", "Understand people first.",
     ["User research", "Requirements", "PRDs", "User stories", "RICE", "P0/P1 priorities", "Roadmaps",
      "Market research", "Competitive analysis"]),
    ("Deliver.", "Ship it. Then make it better.",
     ["Product launch", "Scrum", "Kanban", "QA", "Edge cases", "Iteration", "Cross-functional teams",
      "Stakeholders", "Tech presentations"]),
    ("Build with AI.", "Prototype at the speed of thought.",
     ["Voice AI", "Speech-to-text", "LLM prototyping", "AI/ML products", "Python", "SQL", "Figma", "Jira",
      "Notion"]),
]


def chip(x, y, label, h=24):
    w = 20 + len(label) * 6.4
    return w, (f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.1f}" height="{h - 1}" rx="{(h - 1) / 2}" '
               f'fill="{CANVAS}" stroke="{HAIR}"/>' +
               t(x + w / 2, y + h / 2 + 4, label, 12, 400, INK, "middle"))


def process():
    parts = [t(PAD, 62, "The process.", 30, 600, INK, ls=-.7, cls="up d1"),
             t(PAD, 88, "Every detail considered. From the first interview to launch day.", 15, 400, GRAY2,
               cls="up d2")]
    tw = (INNER - 2 * GAP) / 3
    parts.append('<defs><filter id="lift2" x="-10%" y="-20%" width="120%" height="150%">'
                 '<feDropShadow dx="0" dy="4" stdDeviation="9" flood-color="#000" flood-opacity=".07"/></filter></defs>')
    ly = 128
    # timeline that draws itself, with numbered nodes
    parts.append(f'<line class="draw" x1="{PAD + 34}" y1="{ly}" x2="{PAD + 2 * (tw + GAP) + 34}" y2="{ly}" '
                 f'stroke="{HAIR}" stroke-width="1"/>')
    y = 158

    def rows(chips):
        n, cx = 1, 0
        for c in chips:
            w = 20 + len(c) * 6.4
            if cx and cx + w > tw - 44:
                n, cx = n + 1, 0
            cx += w + 8
        return n

    th = 116 + max(rows(c) for _, _, c in STEPS) * 32 + 14
    for i, (title, line, chips) in enumerate(STEPS):
        x = PAD + i * (tw + GAP)
        ix = x + 22
        parts.append(f'<g class="up d{3 + i}">')
        parts.append(f'<circle cx="{x + 34}" cy="{ly}" r="12" fill="{TILE}" stroke="{GRAY2}"/>')
        parts.append(t(x + 34, ly + 4, str(i + 1), 11, 600, INK, "middle"))
        parts.append(f'<rect x="{x:.1f}" y="{y}" width="{tw:.1f}" height="{th}" rx="14" fill="{TILE}" filter="url(#lift2)"/>')
        parts.append(t(ix, y + 30, f"Step {i + 1:02d}", 11, 600, GRAY))
        parts.append(t(ix, y + 62, title, 22, 600, INK, ls=-.4))
        parts.append(t(ix, y + 84, line, 13, 400, GRAY))
        parts.append(hair(ix, y + 100, x + tw - 22, y + 100, HAIR))
        cx, cy = ix, y + 116
        for c in chips:
            w = 20 + len(c) * 6.4
            if cx + w > x + tw - 22:
                cx, cy = ix, cy + 32
            _, svg = chip(cx, cy, c)
            parts.append(svg)
            cx += w + 8
        parts.append("</g>")

    by, bh = y + th + GAP, 82
    bw = (INNER - GAP) / 2
    blocks = [("Certified", "Agile Project Management", "Professional Certificate, Atlassian. Aug 2026."),
              ("Community", "Event Coordinator", "Lloyd Institute of Engineering and Technology. Dec 2025.")]
    for i, (eb, title, sub) in enumerate(blocks):
        x = PAD + i * (bw + GAP)
        ix = x + 22
        parts.append(f'<g class="up d{5 + i}">{f'<rect x="{x:.1f}" y="{by}" width="{bw:.1f}" height="{bh}" rx="14" fill="{TILE}" filter="url(#lift2)"/>'}')
        parts.append(t(ix, by + 28, eb, 11, 600, GRAY))
        parts.append(t(ix, by + 51, title, 16, 600, INK, ls=-.2))
        parts.append(t(ix, by + 69, sub, 12, 400, GRAY))
        parts.append("</g>")
    css = """
.draw{stroke-dasharray:700;stroke-dashoffset:700;animation:draw 1.6s cubic-bezier(.25,.1,.25,1) .2s forwards;}
@keyframes draw{to{stroke-dashoffset:0}}
"""
    return frame(by + bh + PAD, "\n".join(parts), CANVAS, css)


# =====================================================================
# 5. FOOTER
# =====================================================================
def footer():
    h = 168
    body = f'''
{t(W / 2, 64, "Let’s make something great.", 28, 600, INK, "middle", -.6, "up d1")}
{t(W / 2, 90, "Open to conversations about AI products, voice and building for India.", 14, 400, GRAY, "middle", 0, "up d2")}
{hair(PAD, 118, W - PAD, 118)}
{t(PAD, 142, "Designed by Lal Aman Singh in Noida.", 11, 400, GRAY2)}
{t(W - PAD, 142, "github.com/lalamansingh", 11, 400, GRAY2, "end")}
'''
    return frame(h, body)


PANELS = {"intro": intro, "recognition": recognition, "projects": projects, "process": process,
          "footer": footer}

if __name__ == "__main__":
    for old in OUT.glob("*.svg"):
        if old.stem not in PANELS:
            old.unlink()
    for name, fn in PANELS.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
        print("wrote", OUT / f"{name}.svg")

    # Cache-bust: give every README image a content hash so browsers and GitHub's
    # image proxy fetch the new file whenever a panel changes.
    import hashlib
    import re
    readme = OUT.parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    for name in PANELS:
        digest = hashlib.sha1((OUT / f"{name}.svg").read_bytes()).hexdigest()[:8]
        text = re.sub(rf'assets/{name}\.svg(\?v=[0-9a-f]+)?"', f'assets/{name}.svg?v={digest}"', text)
    readme.write_text(text, encoding="utf-8")

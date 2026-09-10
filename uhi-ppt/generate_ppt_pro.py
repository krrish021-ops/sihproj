"""HeatSight UHI hackathon PPT — PRO edition.
Light editorial theme, hairline tables, ghost numerals, realistic UI mockup, zero emoji.
Output: uhi-ppt/HeatSight_UHI_PPT_Pro.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_TICK_MARK
from pptx.oxml.ns import qn

# ---------------- Palette ----------------
PAPER  = RGBColor(0xF6, 0xF4, 0xEF)   # warm off-white
INK    = RGBColor(0x19, 0x1C, 0x20)   # near-black
MUTED  = RGBColor(0x6E, 0x6E, 0x6A)   # warm gray
FAINT  = RGBColor(0xE7, 0xE3, 0xD9)   # hairlines / ghost numerals
CARD_B = RGBColor(0xDE, 0xD9, 0xCE)   # card borders
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
TERRA  = RGBColor(0xC2, 0x41, 0x0C)   # primary accent (burnt orange)
AMBER  = RGBColor(0xD9, 0x77, 0x06)
TEAL   = RGBColor(0x0E, 0x7C, 0x6B)
RISK   = RGBColor(0xB9, 0x1C, 0x1C)
SLATE  = RGBColor(0x33, 0x41, 0x55)
COAL   = RGBColor(0x14, 0x14, 0x16)   # dark slides
CREAM  = RGBColor(0xF5, 0xF2, 0xEA)
DIM    = RGBColor(0xA8, 0xA2, 0x9A)
GOLD   = RGBColor(0xF5, 0x9E, 0x0B)   # amber for dark backgrounds
TINT_R = RGBColor(0xF7, 0xE3, 0xDC)   # light red tint
TINT_A = RGBColor(0xF8, 0xEC, 0xD5)   # light amber tint
TINT_T = RGBColor(0xDC, 0xEF, 0xE9)   # light teal tint
TINT_G = RGBColor(0xEF, 0xED, 0xE6)   # light neutral tint

FONT  = "Segoe UI"
MONO  = "Consolas"
N_MAIN = 10  # appendix unnumbered

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]
W = 13.33

# ---------------- helpers ----------------
def letterspace(run, spc="140"):
    try:
        run._r.get_or_add_rPr().set("spc", spc)
    except Exception:
        pass

def transparent(shape, pct):
    """pct 0-100 transparency on an autoshape solid fill."""
    try:
        spPr = shape._element.find(qn("p:spPr"))
        solid = spPr.find(qn("a:solidFill"))
        srgb = solid.find(qn("a:srgbClr"))
        if srgb is None:
            return
        srgb.append(srgb.makeelement(qn("a:alpha"), {"val": str(int(pct * 1000))}))
    except Exception:
        pass

def no_line(shape):
    shape.line.fill.background()

def rect(s, l, t, w, h, fill=None, line=None, lw=1.0, shape=MSO_SHAPE.RECTANGLE):
    sh = s.shapes.add_shape(shape, Inches(l), Inches(t), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None:
        no_line(sh)
    else:
        sh.line.color.rgb = line; sh.line.width = Pt(lw)
    return sh

def circle(s, l, t, d, fill, line=None):
    return rect(s, l, t, d, d, fill, line, shape=MSO_SHAPE.OVAL)

def txt(s, l, t, w, h, runs, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, wrap=True):
    """runs: list of (text, size, color, bold, font, space_after, space_before, ls) or plain str."""
    tx = s.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = tx.text_frame; tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0.02); tf.margin_right = Inches(0.02)
    first = True
    for item in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        if isinstance(item, str):
            item = [(item, 12, INK, False, FONT, 2, 0, None)]
        if isinstance(item, tuple):
            item = [item]
        for piece in item:
            text, size, color, bold, font, sa, sb, ls = (list(piece) + [None]*8)[:8]
            p.space_after = Pt(sa or 2); p.space_before = Pt(sb or 0)
            r = p.add_run(); r.text = text
            r.font.size = Pt(size); r.font.color.rgb = color
            r.font.bold = bool(bold); r.font.name = font or FONT
            if ls:
                letterspace(r, ls)
    return tx

def hairline(s, l, t, w, color=FAINT):
    return rect(s, l, t, w, 0.014, fill=color)

def interior(num, kicker, title, subtitle=None):
    """Light interior slide w/ ghost numeral, header, footer."""
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = PAPER
    # ghost numeral (added first => sits at back)
    txt(s, 10.55, -0.15, 2.6, 1.9, [[(num, 110, FAINT, True, FONT, 0, 0, None)]], align=PP_ALIGN.RIGHT)
    # header
    txt(s, 0.7, 0.42, 9.5, 0.32, [[(f"{num}  —  {kicker}", 11, TERRA, True, FONT, 0, 0, "150")]])
    txt(s, 0.7, 0.70, 9.5, 0.62, [[(title, 29, INK, True, FONT, 0, 0, None)]])
    if subtitle:
        txt(s, 0.7, 1.32, 9.5, 0.42, [[(subtitle, 13.5, MUTED, False, FONT, 0, 0, None)]])
    # footer
    hairline(s, 0.7, 6.98, W - 1.4)
    txt(s, 0.7, 7.06, 6.0, 0.3, [[("HEATSIGHT  ·  URBAN HEAT ISLAND FORECASTING", 8.5, MUTED, True, FONT, 0, 0, "120")]])
    txt(s, 11.2, 7.06, 1.43, 0.3, [[(f"{num} / {N_MAIN:02d}", 8.5, MUTED, True, FONT, 0, 0, "120")]], align=PP_ALIGN.RIGHT)
    return s

def dark_slide():
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid(); s.background.fill.fore_color.rgb = COAL
    return s

def notes(s, text):
    s.notes_slide.notes_text_frame.text = text

def pro_table(s, l, t, w, data, widths, row_h=0.52, size=11.5):
    """Banded hairline table on white card. data[0] = header."""
    # card behind
    total_h = row_h * len(data) + 0.1
    rect(s, l - 0.12, t - 0.08, w + 0.24, total_h + 0.1, fill=WHITE, line=CARD_B, lw=1.0,
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    gt = s.shapes.add_table(len(data), len(data[0]), Inches(l), Inches(t), Inches(w), Inches(row_h * len(data))).table
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            c = gt.cell(i, j)
            c.fill.solid()
            c.fill.fore_color.rgb = WHITE if (i == 0 or i % 2 == 1) else TINT_G
            c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.margin_left = Inches(0.12); c.margin_right = Inches(0.08)
            tf = c.text_frame; tf.word_wrap = True
            p = tf.paragraphs[0]
            r = p.add_run(); r.text = val
            r.font.name = FONT
            if i == 0:
                r.font.size = Pt(9.5); r.font.bold = True; r.font.color.rgb = MUTED
                letterspace(r, "120")
            else:
                r.font.size = Pt(size); r.font.color.rgb = INK
                if j == 0:
                    r.font.bold = True
    for j, wd in enumerate(widths):
        gt.columns[j].width = Inches(wd)
    return gt

# ================= 01 · COVER (dark) =================
s = dark_slide()
# abstract thermal glow — layered translucent circles, right side
glow = [
    (9.7, 0.4, 5.4, RGBColor(0x7C, 0x2D, 0x12), 55),
    (10.5, 1.3, 4.1, RGBColor(0xC2, 0x41, 0x0C), 45),
    (11.2, 2.0, 2.8, RGBColor(0xF5, 0x9E, 0x0B), 35),
    (11.85, 2.6, 1.5, RGBColor(0xFD, 0xD6, 0x8A), 15),
]
for l, t, d, col, tr in glow:
    c = circle(s, l, t, d, col); transparent(c, tr)
# thin orbit rings
for l, t, d in [(10.15, 0.9, 4.6), (10.75, 1.5, 3.4)]:
    r_ = circle(s, l, t, d, None, line=DIM); transparent(r_, 70)
# left content
txt(s, 0.9, 1.05, 7.6, 0.35, [[("SMART INDIA HACKATHON  ·  2026", 12, GOLD, True, FONT, 0, 0, "180")]])
txt(s, 0.9, 1.45, 7.6, 1.2, [[("HeatSight", 66, CREAM, True, FONT, 0, 0, None)]])
rect(s, 0.9, 2.62, 0.9, 0.05, fill=GOLD)
txt(s, 0.9, 2.85, 7.0, 0.9, [[("Forecasting urban heat islands for climate-smart Indian cities.", 19, CREAM, False, FONT, 0, 0, None)]])
txt(s, 0.9, 3.75, 6.6, 0.8, [[("Satellite LST time-series  +  land-use intelligence  →  ward-level heat forecasts urban planners can act on.", 12.5, DIM, False, FONT, 0, 0, None)]])
# LST legend bar (thematic touch)
lx = 0.9
for i, col in enumerate([RGBColor(0x7C,0x2D,0x12), RGBColor(0xC2,0x41,0x0C), RGBColor(0xEA,0x7A,0x28),
                         RGBColor(0xF5,0x9E,0x0B), RGBColor(0xFD,0xD6,0x8A)]):
    rect(s, lx + i * 0.55, 4.85, 0.55, 0.16, fill=col)
txt(s, 0.9, 5.05, 3.0, 0.3, [[("LAND SURFACE TEMPERATURE  ·  38°C  →  46°C", 8.5, DIM, True, FONT, 0, 0, "120")]])
# meta row
for i, (k, v) in enumerate([("TEAM", "[ Your Team Name ]"), ("INSTITUTE", "[ College Name ]"), ("PROBLEM STATEMENT", "[ PS-ID ]")]):
    x = 0.9 + i * 2.5
    txt(s, x, 5.85, 2.4, 0.28, [[(k, 9, GOLD, True, FONT, 0, 0, "150")]])
    txt(s, x, 6.10, 2.4, 0.35, [[(v, 12, CREAM, False, FONT, 0, 0, None)]])
hairline(s, 0.9, 6.85, W - 1.8, RGBColor(0x33,0x33,0x36))
txt(s, 0.9, 6.95, 6.0, 0.3, [[("HEATSIGHT  ·  IDEA DECK  ·  SEPTEMBER 2026", 8.5, DIM, True, FONT, 0, 0, "120")]])
notes(s, "20 seconds. Land the one-liner: Indian cities run 3–7°C hotter than their villages, and planners have no forecast. HeatSight is that forecast. Then move on.")

# ================= 02 · PROBLEM =================
s = interior("02", "THE PROBLEM", "Indian cities are becoming heat traps",
             "An urban heat island (UHI) keeps built-up zones 3–7 °C hotter than surrounding rural land — day and night.")
# stat band
stats = [("50 °C +", "recorded summer peaks\nin Delhi, 2024–25"), ("3–7 °C", "city-vs-village\ntemperature gap"), ("50 +", "Indian cities facing\nsevere UHI stress")]
for i, (val, lab) in enumerate(stats):
    x = 0.7 + i * 3.98
    rect(s, x, 2.05, 3.75, 1.45, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x + 0.3, 2.18, 3.15, 0.6, [[(val, 34, TERRA, True, FONT, 0, 0, None)]])
    txt(s, x + 0.3, 2.78, 3.15, 0.6, [[(lab, 11.5, MUTED, False, FONT, 0, 0, None)]])
# concise impact rows
rows = [
    ("Concrete is replacing green cover.", "Rapid construction and shrinking lakes and parks trap daytime heat deep into the night."),
    ("Health and energy bills are exploding.", "Heat-stroke cases, peak power demand and water stress spike every summer in dense wards."),
    ("Planners are flying blind.", "No ward-level forecast exists of where heat will intensify next as the city grows."),
]
y = 3.85
for title, desc in rows:
    txt(s, 0.7, y, 0.35, 0.35, [[("▪", 14, TERRA, True, FONT, 0, 0, None)]])
    txt(s, 1.05, y - 0.02, 11.55, 0.75, [[(title + "  ", 13.5, INK, True, FONT, 0, 0, None), (desc, 13.5, MUTED, False, FONT, 0, 0, None)]])
    y += 0.78
hairline(s, 0.7, 6.35, W - 1.4)
txt(s, 0.7, 6.45, 11.9, 0.35, [[("The question no tool answers today:  which wards will overheat next?", 12, TERRA, True, FONT, 0, 0, None)]])
notes(s, "40 seconds. Read the three stats, then the three rows fast. End on the question at the bottom — it tees up the next slide.")

# ================= 03 · GAP =================
s = interior("03", "THE GAP", "Temperature is reported. Heat islands are not.",
             "What exists today — and why none of it helps a planner decide where to act.")
# two cards
rect(s, 0.7, 2.0, 5.85, 3.6, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 1.0, 2.2, 5.25, 0.3, [[("WHAT EXISTS TODAY", 10, MUTED, True, FONT, 0, 0, "150")]])
exists = [("IMD & weather apps", "City-average air temperature. No land-surface detail, no ward split."),
          ("Research papers", "One-time LST maps as static PDFs. No forecast, no dashboard."),
          ("Smart-city dashboards", "Track AQI and traffic. Heat intelligence: zero.")]
y = 2.65
for t, d in exists:
    txt(s, 1.0, y, 5.25, 0.7, [[(t, 12.5, INK, True, FONT, 2, 0, None)], [(d, 11.5, MUTED, False, FONT, 0, 0, None)]])
    y += 0.85
rect(s, 6.78, 2.0, 5.85, 3.6, fill=COAL, line=COAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 7.08, 2.2, 5.25, 0.3, [[("WHAT'S MISSING", 10, GOLD, True, FONT, 0, 0, "150")]])
missing = [("Ward-level heat forecasts", "Which zones warm fastest as land use changes."),
           ("A living, updating system", "New satellite passes in, fresh risk maps out."),
           ("Planning-ready outputs", "Rankings and actions — not raw rasters and jargon.")]
y = 2.65
for t, d in missing:
    txt(s, 7.08, y, 5.25, 0.7, [[(t, 12.5, CREAM, True, FONT, 2, 0, None)], [(d, 11.5, DIM, False, FONT, 0, 0, None)]])
    y += 0.85
# insight bar
rect(s, 0.7, 5.85, 11.93, 0.85, fill=TINT_R, line=TERRA, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 1.0, 5.97, 11.33, 0.6, [[("No open tool links satellite LST  +  land-use change  →  future hotspot forecasts.   That gap is HeatSight.", 12.5, RISK, True, FONT, 0, 0, None)]], anchor=MSO_ANCHOR.MIDDLE)
notes(s, "30 seconds. Left card: three things that exist. Right card: three things missing. Read the red bar verbatim — it's the pitch.")

# ================= 04 · IDEA =================
s = interior("04", "THE IDEA", "HeatSight — a heat-forecast copilot for urban planners",
             "Three capabilities, one pipeline, one dashboard.")
cards = [
    ("01", "Map the past", "A 10-year satellite record (2015–2025) of land-surface temperature and land-use change for every ward.", TERRA),
    ("02", "Forecast hotspots", "Machine learning projects 2030 heat-intensification zones as construction and concrete grow.", AMBER),
    ("03", "Guide action", "Ward risk rankings plus concrete moves: plantations, cool roofs, lake revival, building norms.", TEAL),
]
for i, (num, title, desc, accent) in enumerate(cards):
    x = 0.7 + i * 4.05
    rect(s, x, 2.0, 3.83, 3.3, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, x, 2.0, 3.83, 0.09, fill=accent)
    txt(s, x + 0.35, 2.3, 3.1, 0.5, [[(num, 30, accent, True, FONT, 0, 0, None)]])
    txt(s, x + 0.35, 2.95, 3.1, 0.45, [[(title, 15, INK, True, FONT, 0, 0, None)]])
    txt(s, x + 0.35, 3.45, 3.13, 1.5, [[(desc, 11.5, MUTED, False, FONT, 0, 0, None)]])
rect(s, 0.7, 5.6, 11.93, 0.8, fill=COAL, line=COAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 0.7, 5.68, 11.93, 0.6, [[("Past heat  +  land-use change   →   future hotspots   →   planning decisions.", 13, CREAM, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "40 seconds. Point at 01, 02, 03. End by reading the dark strip — judges remember one-liners.")

# ================= 05 · ARCHITECTURE =================
s = interior("05", "HOW IT WORKS", "From satellite pixels to planner decisions",
             "Five stages. Fully open data, fully reproducible.")
steps = [
    ("1", "SATELLITE DATA", "Landsat 8/9 LST\nSentinel-2 land use\nMODIS · IMD"),
    ("2", "PREPROCESS", "Cloud masking\nLST retrieval\nWard clipping"),
    ("3", "FEATURES", "LST trend\nNDVI · NDBI\nBuilt-up %"),
    ("4", "ML MODEL", "Random Forest\nXGBoost / LSTM\nTrain 2015 → 25"),
    ("5", "FORECAST UI", "2030 hotspot map\nWard ranking\nAction tips"),
]
# connector line
rect(s, 1.55, 2.72, 10.23, 0.035, fill=CARD_B)
n = len(steps)
slot = 11.93 / n
for i, (num, title, desc) in enumerate(steps):
    cx = 0.7 + slot * i + slot / 2
    # node
    c = circle(s, cx - 0.21, 2.51, 0.42, TERRA if i in (0, 4) else WHITE, TERRA)
    if i not in (0, 4):
        c.line.width = Pt(2.25)
    txt(s, cx - 0.21, 2.52, 0.42, 0.4, [[(num, 14, WHITE if i in (0, 4) else TERRA, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # card
    rect(s, 0.7 + slot * i + 0.1, 3.15, slot - 0.2, 1.85, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, 0.7 + slot * i + 0.2, 3.32, slot - 0.4, 0.35, [[(title, 10, TERRA, True, FONT, 0, 0, "80")]], align=PP_ALIGN.CENTER)
    txt(s, 0.7 + slot * i + 0.2, 3.72, slot - 0.4, 1.1, [[(desc, 11, MUTED, False, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER)
# science strip
rect(s, 0.7, 5.3, 11.93, 1.35, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 1.0, 5.45, 11.33, 0.35, [[("CORE SCIENCE  ·  FULL DERIVATION IN APPENDIX A", 9.5, MUTED, True, FONT, 0, 0, "150")]])
txt(s, 1.0, 5.8, 11.33, 0.7, [[("NDVI = (NIR − Red) / (NIR + Red)      NDBI = (SWIR − NIR) / (SWIR + NIR)      UHI = LST(urban) − LST(rural)", 12, INK, False, MONO, 0, 0, None)]])
notes(s, "60 seconds — the most important slide. Walk the five nodes left to right. One line on science: LST corrected with NDVI emissivity, NDBI tracks concrete, UHI is urban minus rural. Point to the appendix for derivation.")

# ================= 06 · STACK =================
s = interior("06", "STACK & DATA", "An entirely open stack — built to scale",
             "Every dataset is free. Every tool is open-source. Any Indian city can be onboarded.")
data = [
    ("LAYER", "TOOLS", "WHY THIS CHOICE"),
    ("Satellite processing", "Google Earth Engine · Landsat 8/9 · Sentinel-2 · MODIS", "Petabyte-scale compute, zero downloads"),
    ("Geo + ML pipeline", "Python · rasterio / GDAL · scikit-learn · XGBoost", "LST trends, drivers, ward forecasts"),
    ("Dashboard", "Streamlit / React + Leaflet · FastAPI", "Hotspot maps + rankings for planners"),
    ("Validation", "IMD observations · Bhuvan · ground sensors", "Independent cross-check of hotspots"),
]
pro_table(s, 0.82, 2.15, 11.69, data, [2.7, 5.6, 3.39], row_h=0.62)
rect(s, 0.7, 5.75, 11.93, 0.85, fill=TINT_T, line=TEAL, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 0.7, 5.86, 11.93, 0.6, [[("Zero data cost   ·   No proprietary software   ·   Tier-1, Tier-2 and Tier-3 ready", 12.5, TEAL, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "30 seconds. Stress FREE and SCALABLE — this answers the cost question before judges ask it.")

# ================= 07 · DASHBOARD MOCKUP =================
s = interior("07", "EXPECTED OUTPUT", "What the planner sees",
             "Concept UI for the pilot city dashboard — proposed layout, sample values for illustration.")
# window
win_l, win_t, win_w, win_h = 0.7, 1.95, 11.93, 4.85
rect(s, win_l, win_t, win_w, win_h, fill=WHITE, line=CARD_B, lw=1.25, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
# chrome
rect(s, win_l + 0.02, win_t + 0.02, win_w - 0.04, 0.4, fill=TINT_G)
for i, col in enumerate([RGBColor(0xD4,0x6B,0x5E), RGBColor(0xE0,0xA8,0x3E), RGBColor(0x6F,0xA2,0x87)]):
    circle(s, win_l + 0.22 + i * 0.24, win_t + 0.15, 0.13, col)
rect(s, 5.4, win_t + 0.11, 3.6, 0.24, fill=WHITE, line=CARD_B, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 5.4, win_t + 0.12, 3.6, 0.24, [[("heatsight · dashboard — Nagpur pilot", 8.5, MUTED, False, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# sidebar
sb_w = 2.0
rect(s, win_l + 0.02, win_t + 0.44, sb_w - 0.02, win_h - 0.46, fill=COAL)
txt(s, win_l + 0.22, win_t + 0.62, 1.6, 0.25, [[("◉  HEATSIGHT", 9.5, CREAM, True, FONT, 0, 0, "100")]])
nav = [("Overview", True), ("Hotspot map", False), ("Trends", False), ("Ward ranking", False), ("Reports", False)]
ny = win_t + 1.1
for label, active in nav:
    if active:
        rect(s, win_l + 0.12, ny - 0.05, sb_w - 0.24, 0.32, fill=RGBColor(0x2A,0x2A,0x2E), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        circle(s, win_l + 0.22, ny + 0.035, 0.09, GOLD)
        txt(s, win_l + 0.42, ny - 0.03, 1.35, 0.28, [[(label, 9.5, CREAM, True, FONT, 0, 0, None)]])
    else:
        txt(s, win_l + 0.42, ny - 0.03, 1.35, 0.28, [[(label, 9.5, DIM, False, FONT, 0, 0, None)]])
    ny += 0.42
rect(s, win_l + 0.22, win_t + win_h - 0.55, sb_w - 0.44, 0.32, fill=None, line=DIM, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, win_l + 0.22, win_t + win_h - 0.54, sb_w - 0.44, 0.3, [[("PLANNER LOGIN", 8, DIM, True, FONT, 0, 0, "80")]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# main area
mx, mw = win_l + sb_w + 0.18, win_w - sb_w - 0.36
# KPI chips
kpis = [("MEAN SUMMER LST · 2025", "41.6 °C", "+2.4° since 2015", TERRA),
        ("HOTSPOT WARDS", "14 / 38", "5 new since 2020", RISK),
        ("GREEN COVER", "11.2 %", "−3.1 pts since 2015", TEAL)]
kw = (mw - 0.24) / 3
for i, (k, v, d, col) in enumerate(kpis):
    x = mx + i * (kw + 0.12)
    rect(s, x, win_t + 0.6, kw, 0.72, fill=PAPER, line=CARD_B, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x + 0.14, win_t + 0.66, kw - 0.28, 0.2, [[(k, 7.5, MUTED, True, FONT, 0, 0, "80")]])
    txt(s, x + 0.14, win_t + 0.84, 1.3, 0.35, [[(v, 15, INK, True, FONT, 0, 0, None)]])
    txt(s, x + 1.45, win_t + 0.92, kw - 1.6, 0.25, [[(d, 8.5, col, True, FONT, 0, 0, None)]])
# map panel
map_y, map_h = win_t + 1.48, 2.05
map_w = mw * 0.58
rect(s, mx, map_y, map_w, map_h, fill=PAPER, line=CARD_B, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, mx + 0.16, map_y + 0.1, 3.2, 0.25, [[("NAGPUR  ·  2030 FORECAST", 8.5, INK, True, FONT, 0, 0, "100")]])
rect(s, mx + map_w - 1.35, map_y + 0.08, 1.19, 0.26, fill=TERRA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, mx + map_w - 1.35, map_y + 0.09, 1.19, 0.26, [[("HIGH RISK · 8", 8, WHITE, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
zones = [
    (0.16, 0.45, 2.35, 0.72, TINT_R, RISK, "Industrial belt", "W-12 · 44.6°"),
    (2.65, 0.45, 1.95, 0.72, TINT_A, AMBER, "Old city", "W-07 · 43.1°"),
    (0.16, 1.27, 1.65, 0.62, TINT_A, AMBER, "Market dist.", "W-03 · 41.8°"),
    (1.95, 1.27, 2.65, 0.62, TINT_T, TEAL, "Lake side", "W-21 · 38.4°"),
]
for ox, oy, zw, zh, fillc, linec, zname, zval in zones:
    rect(s, mx + ox, map_y + oy, min(zw, map_w - ox - 0.16), zh, fill=fillc, line=linec, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, mx + ox + 0.1, map_y + oy + 0.06, zw - 0.2, 0.5, [[(zname, 8.5, INK, True, FONT, 1, 0, None)], [(zval, 8, MUTED, False, FONT, 0, 0, None)]])
# ranking panel
rk_x, rk_w = mx + map_w + 0.16, mw - map_w - 0.16
rect(s, rk_x, map_y, rk_w, map_h, fill=WHITE, line=CARD_B, lw=0.75, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, rk_x + 0.16, map_y + 0.1, rk_w - 0.32, 0.25, [[("WARD RISK RANKING", 8.5, INK, True, FONT, 0, 0, "100")]])
rank_rows = [("W-12 · Industrial", "43.8°", "HIGH", RISK, TINT_R),
             ("W-07 · Old city", "42.4°", "HIGH", RISK, TINT_R),
             ("W-03 · Market", "40.9°", "MED", AMBER, TINT_A),
             ("W-21 · Lake side", "38.1°", "LOW", TEAL, TINT_T)]
ry = map_y + 0.42
for wname, wval, tag, tcol, tfill in rank_rows:
    if ry > map_y + 0.45:
        hairline(s, rk_x + 0.16, ry - 0.04, rk_w - 0.32)
    txt(s, rk_x + 0.16, ry, rk_w - 1.55, 0.3, [[(wname, 9, INK, False, FONT, 0, 0, None)]])
    txt(s, rk_x + rk_w - 1.42, ry, 0.62, 0.3, [[(wval, 9, MUTED, True, FONT, 0, 0, None)]], align=PP_ALIGN.RIGHT)
    rect(s, rk_x + rk_w - 0.72, ry + 0.02, 0.56, 0.22, fill=tfill, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, rk_x + rk_w - 0.72, ry + 0.02, 0.56, 0.22, [[(tag, 7, tcol, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    ry += 0.36
# trend strip (real chart)
ch_y, ch_h = map_y + map_h + 0.14, 1.0
txt(s, mx, ch_y - 0.02, 4.5, 0.25, [[("MEAN SUMMER LST  vs  BUILT-UP %  ·  2015 → 2030", 8.5, INK, True, FONT, 0, 0, "100")]])
rect(s, mx + 6.35, ch_y + 0.03, 0.18, 0.12, fill=TERRA)
txt(s, mx + 6.58, ch_y - 0.01, 1.1, 0.2, [[("LST (°C)", 8, MUTED, False, FONT, 0, 0, None)]])
rect(s, mx + 7.55, ch_y + 0.03, 0.18, 0.12, fill=SLATE)
txt(s, mx + 7.78, ch_y - 0.01, 1.3, 0.2, [[("Built-up %", 8, MUTED, False, FONT, 0, 0, None)]])
cd = ChartData()
cd.categories = ["2015", "17", "19", "21", "23", "25", "30*"]
cd.add_series("LST", (38.2, 39.1, 40.0, 40.8, 42.1, 43.0, 44.6))
cd.add_series("Built-up", (31, 34, 37, 40, 43, 46, 52))
cf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(mx), Inches(ch_y + 0.22), Inches(mw), Inches(ch_h - 0.2), cd)
ch = cf.chart
ch.has_title = False; ch.has_legend = False
ch.value_axis.has_major_gridlines = True
ch.value_axis.visible = True
try:
    ch.value_axis.minimum_scale = 25; ch.value_axis.maximum_scale = 55
except Exception:
    pass
for idx, col in enumerate([TERRA, SLATE]):
    ser = ch.series[idx]
    ser.format.line.color.rgb = col
    ser.format.line.width = Pt(2.5)
    ser.smooth = True
    try:
        ser.marker.style = 2
        ser.marker.format.fill.solid(); ser.marker.format.fill.fore_color.rgb = col
        ser.marker.format.line.color.rgb = WHITE
        ser.marker.size = 6
    except Exception:
        pass
txt(s, 0.7, 6.86, 11.93, 0.25, [[("Concept UI mockup · sample values for illustration  ·  *2030 = model forecast", 9.5, MUTED, False, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER)
notes(s, "60 seconds. Tour the product: KPIs on top, forecast map left, ward ranking right, trend strip below. Say honestly: concept UI, real values land once the satellite pipeline is built.")

# ================= 08 · ROADMAP =================
s = interior("08", "EXECUTION PLAN", "From idea to working pilot",
             "One city first, validated properly — then a repeatable template for every city.")
phases = [
    ("PHASE 1 · WK 1–2", "Data pipeline", "GEE: Landsat LST 2015–25, Sentinel-2 land use, ward boundaries.", "Clean time-series for pilot city"),
    ("PHASE 2 · WK 3–4", "Model & validate", "Engineer NDVI / NDBI / built-up features; train RF + XGBoost.", "2030 ward forecast, IMD-checked"),
    ("PHASE 3 · WK 5–6", "Dashboard MVP", "Hotspot map, trends, rankings and action tips in one UI.", "Working planner dashboard"),
    ("PHASE 4 · WK 7+", "Pilot & scale", "Ground-truth validation, second city, Heat Action Plan report.", "Pilot report + city template"),
]
rect(s, 1.5, 2.15, 10.33, 0.035, fill=CARD_B)
for i, (tag, title, tasks, out) in enumerate(phases):
    x = 0.7 + i * 3.06
    cx = x + 1.45
    c = circle(s, cx - 0.11, 2.04, 0.22, TERRA if i == 0 else WHITE, TERRA)
    if i != 0:
        c.line.width = Pt(2.0)
    rect(s, x, 2.45, 2.9, 3.55, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    rect(s, x + 0.25, 2.7, 2.4, 0.34, fill=COAL if i == 0 else TINT_G, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, x + 0.25, 2.71, 2.4, 0.32, [[(tag, 8.5, CREAM if i == 0 else MUTED, True, FONT, 0, 0, "60")]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + 0.25, 3.15, 2.4, 0.4, [[(title, 14, INK, True, FONT, 0, 0, None)]])
    txt(s, x + 0.25, 3.6, 2.4, 1.0, [[(tasks, 10.5, MUTED, False, FONT, 0, 0, None)]])
    hairline(s, x + 0.25, 4.85, 2.4)
    txt(s, x + 0.25, 5.0, 2.4, 0.8, [[("→  ", 10.5, TEAL, True, FONT, 0, 0, None), (out, 10.5, INK, True, FONT, 0, 0, None)]])
notes(s, "30 seconds. Emphasize discipline: one pilot city, validated, then scale. Judges fear over-scoped projects — this calms them.")

# ================= 09 · IMPACT =================
s = interior("09", "IMPACT & USERS", "Built for the people who shape Indian cities",
             "A forecast is only useful if the right hands hold it.")
users = [
    ("MUNICIPAL CORPORATIONS", "Decide where to plant, where to pause concrete, and where to mandate cool roofs — ward by ward.", TERRA),
    ("HEAT ACTION PLANS", "Give NDMA and IMD ward-level evidence to extend Ahmedabad-style plans to every heat-prone city.", TERRA),
    ("PLANNERS & BUILDERS", "Check the heat impact of new layouts before approval — a future “heat NOC” layer.", AMBER),
    ("CITIZENS", "Cooler wards, lower power bills, safer summers for outdoor workers and the elderly.", TEAL),
]
y = 2.05
for uname, benefit, col in users:
    txt(s, 0.7, y, 3.3, 0.35, [[(uname, 10.5, col, True, FONT, 0, 0, "100")]])
    txt(s, 4.15, y - 0.04, 8.45, 0.6, [[(benefit, 12.5, INK, False, FONT, 0, 0, None)]])
    y += 0.72
    hairline(s, 0.7, y, W - 1.4)
    y += 0.18
rect(s, 0.7, 5.85, 11.93, 0.85, fill=COAL, line=COAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 0.7, 5.93, 11.93, 0.65, [[("50+ cities face severe UHI  ·  one pipeline, replicated everywhere  ·  zero data cost", 13, CREAM, True, FONT, 0, 0, None)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "40 seconds — the winner slide. Name real users: municipality, Smart City mission, NDMA. Close with the scale line.")

# ================= 10 · TEAM + THANK YOU (dark) =================
s = dark_slide()
rect(s, 0.9, 5.9, 0.9, 0.05, fill=GOLD)
txt(s, 0.9, 1.1, 6.4, 1.1, [[("Thank you.", 56, CREAM, True, FONT, 0, 0, None)]])
txt(s, 0.9, 2.25, 6.4, 0.5, [[("Questions and discussion are welcome.", 15, DIM, False, FONT, 0, 0, None)]])
txt(s, 0.9, 3.1, 6.4, 1.4, [[("HeatSight turns a decade of satellite heat data into the one thing planners lack — a forecast of where their city will overheat next.", 12.5, DIM, False, FONT, 0, 0, None)]])
# contact pills
for i, label in enumerate(["GITHUB  ·  [ link ]", "CONTACT  ·  [ email ]"]):
    rect(s, 0.9 + i * 2.9, 4.7, 2.7, 0.44, fill=None, line=DIM, lw=0.9, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    txt(s, 0.9 + i * 2.9, 4.72, 2.7, 0.4, [[(label, 9, DIM, True, FONT, 0, 0, "60")]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
# team panel
rect(s, 7.6, 0.9, 4.85, 5.65, fill=RGBColor(0x1D,0x1D,0x20), line=RGBColor(0x33,0x33,0x36), lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 8.0, 1.2, 4.05, 0.3, [[("THE TEAM", 10, GOLD, True, FONT, 0, 0, "160")]])
members = [
    ("[ Member 1 ]", "Team Lead · ML & Pipeline"),
    ("[ Member 2 ]", "Remote Sensing · GEE & LST"),
    ("[ Member 3 ]", "Backend · API & Data"),
    ("[ Member 4 ]", "Frontend · Dashboard & Maps"),
    ("[ Member 5 ]", "Research · Planning & Validation"),
    ("[ Member 6 ]", "Design · Demo & Deck"),
]
my = 1.7
for name, role in members:
    txt(s, 8.0, my, 4.05, 0.55, [[(name, 12, CREAM, True, FONT, 1, 0, None)], [(role, 10.5, DIM, False, FONT, 0, 0, None)]])
    my += 0.68
hairline(s, 0.9, 6.85, W - 1.8, RGBColor(0x33,0x33,0x36))
txt(s, 0.9, 6.95, 6.0, 0.3, [[("HEATSIGHT  ·  IDEA DECK  ·  SEPTEMBER 2026", 8.5, DIM, True, FONT, 0, 0, "120")]])
notes(s, "20 seconds. Read roles quickly, thank the judges, invite questions. Keep Appendix A ready for the maths question.")

# ================= APPENDIX A · MATHS =================
s = prs.slides.add_slide(BLANK)
s.background.fill.solid(); s.background.fill.fore_color.rgb = PAPER
txt(s, 10.55, -0.15, 2.6, 1.9, [[("A", 110, FAINT, True, FONT, 0, 0, None)]], align=PP_ALIGN.RIGHT)
txt(s, 0.7, 0.42, 9.5, 0.32, [[("APPENDIX A  —  SHOW ONLY IF ASKED", 11, TERRA, True, FONT, 0, 0, "150")]])
txt(s, 0.7, 0.70, 9.5, 0.62, [[("The maths: LST retrieval and forecast model", 29, INK, True, FONT, 0, 0, None)]])
rect(s, 0.7, 2.0, 7.5, 4.6, fill=WHITE, line=CARD_B, lw=1.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 1.0, 2.2, 6.9, 0.3, [[("LANDSAT LST RETRIEVAL  ·  COLLECTION 2, BAND 10", 9.5, MUTED, True, FONT, 0, 0, "120")]])
formula = [
    "1   Radiance ...........  Lλ = ML × DN + AL",
    "2   Brightness temp  BT = K2 / ln(K1/Lλ + 1) − 273.15",
    "3   Veg. fraction .....  Pv = [(NDVI − NDVImin)/(NDVImax − NDVImin)]²",
    "4   Emissivity ..........  ε = 0.004 × Pv + 0.986",
    "5   Final LST ............  LST = BT / [ 1 + (λ·BT/ρ) · ln(ε) ]",
    "",
    "UHI intensity = mean LST(urban) − mean LST(rural buffer)",
    "Trend = slope of LST vs year, 2015–2025 (°C / yr)",
    "Forecast: LST2030 = f(history, NDVI, NDBI, built-up %) · RMSE + R²",
]
txt(s, 1.0, 2.65, 6.9, 3.7, [[(ln, 11.5, INK, False, MONO, 4, 0, None)] for ln in formula])
rect(s, 8.45, 2.0, 3.88, 4.6, fill=COAL, line=COAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
txt(s, 8.8, 2.2, 3.2, 0.3, [[("METHOD NOTES", 9.5, GOLD, True, FONT, 0, 0, "150")]])
hnotes = [
    "Emissivity via the NDVI-threshold method (Sobrino et al.).",
    "Rural baseline: 10 km buffer outside municipal boundary.",
    "Summer composites only (Mar–Jun), <20% cloud cover.",
    "Validation against IMD station data + held-out years.",
]
ny = 2.7
for h in hnotes:
    txt(s, 8.8, ny, 3.2, 0.7, [[("—  ", 11, GOLD, True, FONT, 0, 0, None), (h, 11, DIM, False, FONT, 0, 0, None)]])
    ny += 0.85
hairline(s, 0.7, 6.98, W - 1.4)
txt(s, 0.7, 7.06, 6.0, 0.3, [[("HEATSIGHT  ·  APPENDIX", 8.5, MUTED, True, FONT, 0, 0, "120")]])
notes(s, "Backup only. If asked how LST is computed, walk steps 1–5, then the UHI and forecast lines. Under 60 seconds.")

from pathlib import Path as _P
_OUT = _P(__file__).resolve().parent / "HeatSight_UHI_PPT_Pro.pptx"
prs.save(str(_OUT))
print(f"Saved {_OUT}")

# Also drop a copy straight into the user's Downloads folder (if it exists)
try:
    _dl = _P.home() / "Downloads"
    if _dl.is_dir():
        import shutil as _sh
        _sh.copy(str(_OUT), str(_dl / _OUT.name))
        print(f"Also copied to {_dl / _OUT.name}")
except Exception as _e:
    print(f"(Downloads copy skipped: {_e})")


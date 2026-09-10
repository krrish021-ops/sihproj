"""Generate HeatSight UHI hackathon PPT (10 slides + 1 backup)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import ChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

# ---------- Theme ----------
BG      = RGBColor(0x0F, 0x1B, 0x2D)  # dark navy
CARD    = RGBColor(0x1A, 0x2B, 0x45)  # card navy
ACCENT  = RGBColor(0xFF, 0x6B, 0x35)  # heat orange
YELLOW  = RGBColor(0xFF, 0xC3, 0x00)
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
GRAY    = RGBColor(0xA0, 0xAE, 0xC0)
GREEN   = RGBColor(0x2E, 0xC4, 0xB6)
RED     = RGBColor(0xE7, 0x1D, 0x36)
FONT    = "Calibri"
TOTAL   = 11

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]

def base_slide():
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = BG
    # top accent bar
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, Inches(0.08))
    bar.fill.solid(); bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()
    return s

def footer(s, n):
    tx = s.shapes.add_textbox(Inches(0.5), Inches(7.0), Inches(12.33), Inches(0.3))
    tf = tx.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = f"HeatSight  •  Smart India Hackathon 2026  •  {n}/{TOTAL}"
    r.font.size = Pt(10); r.font.color.rgb = GRAY; r.font.name = FONT

def title_block(s, kicker, title, subtitle=None):
    tx = s.shapes.add_textbox(Inches(0.6), Inches(0.35), Inches(12.1), Inches(1.5))
    tf = tx.text_frame; tf.word_wrap = True
    if kicker:
        p = tf.paragraphs[0]
        r = p.add_run(); r.text = kicker.upper()
        r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
        p.space_after = Pt(2)
        p2 = tf.add_paragraph()
    else:
        p2 = tf.paragraphs[0]
    r = p2.add_run(); r.text = title
    r.font.size = Pt(32); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
    if subtitle:
        p3 = tf.add_paragraph()
        r = p3.add_run(); r.text = subtitle
        r.font.size = Pt(15); r.font.color.rgb = GRAY; r.font.name = FONT
    # orange underline
    u = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.75), Inches(1.2), Inches(0.06))
    u.fill.solid(); u.fill.fore_color.rgb = ACCENT; u.line.fill.background()

def bullets(s, items, left=0.7, top=2.1, width=11.9, height=4.6, size=17):
    tx = s.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame; tf.word_wrap = True
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(10); p.space_before = Pt(2)
        p.level = 0
        if isinstance(item, tuple):
            head, rest = item
            r = p.add_run(); r.text = "▸  " + head
            r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = YELLOW; r.font.name = FONT
            r2 = p.add_run(); r2.text = rest
            r2.font.size = Pt(size); r2.font.color.rgb = WHITE; r2.font.name = FONT
        else:
            r = p.add_run(); r.text = "▸  " + item
            r.font.size = Pt(size); r.font.color.rgb = WHITE; r.font.name = FONT

def card(s, left, top, width, height, title, desc, border=ACCENT, tsize=14):
    box = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    box.fill.solid(); box.fill.fore_color.rgb = CARD
    box.line.color.rgb = border; box.line.width = Pt(2)
    tf = box.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.15); tf.margin_right = Inches(0.15); tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = title
    r.font.size = Pt(tsize); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
    p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(6)
    r = p2.add_run(); r.text = desc
    r.font.size = Pt(11); r.font.color.rgb = GRAY; r.font.name = FONT
    return box

def style_table(table, col_widths=None):
    for j, cell in enumerate(table.rows[0].cells):
        cell.fill.solid(); cell.fill.fore_color.rgb = ACCENT
        for p in cell.text_frame.paragraphs:
            p.alignment = PP_ALIGN.CENTER
            for r in p.runs:
                r.font.bold = True; r.font.color.rgb = WHITE; r.font.size = Pt(13); r.font.name = FONT
    for i, row in enumerate(table.rows):
        if i == 0: continue
        for cell in row.cells:
            cell.fill.solid(); cell.fill.fore_color.rgb = CARD
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for r in p.runs:
                    r.font.color.rgb = WHITE; r.font.size = Pt(12); r.font.name = FONT
    if col_widths:
        for j, w in enumerate(col_widths):
            table.columns[j].width = Inches(w)

def notes(s, text):
    s.notes_slide.notes_text_frame.text = text

# ================= SLIDE 1 — Title =================
s = base_slide()
# big glow circle effect via two rounded shapes
tx = s.shapes.add_textbox(Inches(0.8), Inches(1.3), Inches(11.7), Inches(4.5))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "SMART INDIA HACKATHON 2026  •  PROBLEM STATEMENT [PS-ID]"
r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(18)
r = p2.add_run(); r.text = "HeatSight"
r.font.size = Pt(72); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
p3 = tf.add_paragraph(); p3.alignment = PP_ALIGN.CENTER
r = p3.add_run(); r.text = "Forecasting Urban Heat Islands for Climate-Smart Indian Cities"
r.font.size = Pt(22); r.font.color.rgb = YELLOW; r.font.name = FONT
p4 = tf.add_paragraph(); p4.alignment = PP_ALIGN.CENTER; p4.space_before = Pt(16)
r = p4.add_run(); r.text = "Satellite LST time-series  +  land-use data  →  ward-level heat intensification forecast for urban planners"
r.font.size = Pt(14); r.font.color.rgb = GRAY; r.font.name = FONT
p5 = tf.add_paragraph(); p5.alignment = PP_ALIGN.CENTER; p5.space_before = Pt(22)
r = p5.add_run(); r.text = "Team [Your Team Name]   •   [College Name]   •   [City]"
r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
footer(s, 1)
notes(s, "Open with the heatmap visual in mind. Say: Indian cities are heating 3-7°C more than villages around them, and planners today have no forecasting tool. HeatSight fixes that. 20 seconds.")

# ================= SLIDE 2 — Problem =================
s = base_slide()
title_block(s, "The Problem", "Indian cities are becoming heat traps",
            "Urban Heat Island (UHI): built-up city zones stay 3–7 °C hotter than surrounding rural areas")
bullets(s, [
    ("Heatwaves are deadlier every year: ", "Delhi crossed 50 °C; thousands of heat-stroke cases each summer across North & Central India."),
    ("Concrete replaces green cover: ", "rapid construction + shrinking lakes/parks trap daytime heat deep into the night."),
    ("Energy & health bills explode: ", "peak power demand, water stress, outdoor worker illness, higher mortality in dense wards."),
    ("Planners fly blind today: ", "no ward-level forecast exists of WHERE heat will intensify next as the city grows."),
])
footer(s, 2)
notes(s, "40 sec. Define UHI in one line, then hit 3 pains: deaths/health, energy cost, and planners having no tool. End with: nobody predicts WHERE heat grows next.")

# ================= SLIDE 3 — Gap =================
s = base_slide()
title_block(s, "Why existing solutions fail", "Weather apps tell temperature — nobody predicts heat islands")
bullets(s, [
    ("IMD / weather apps: ", "give city-average air temperature, not land-surface heat at ward/street level."),
    ("Research papers: ", "one-time LST maps of a city — static PDFs, no forecast, no planner dashboard."),
    ("Smart city dashboards: ", "track air quality & traffic, but have zero heat-intensification intelligence."),
    ("Our gap = our opportunity: ", "no open, scalable tool links satellite LST + land-use change → future hotspot forecast."),
])
footer(s, 3)
notes(s, "30 sec. Name 3 things that exist and why each is not enough. Land on the gap: prediction + planning in one tool.")

# ================= SLIDE 4 — Idea =================
s = base_slide()
title_block(s, "Proposed idea", "HeatSight: a heat-forecast copilot for urban planners",
            "Three things the system does")
card(s, 0.6, 2.3, 3.6, 2.5, "1  •  MAP THE PAST", "10-year satellite LST time-series (2015–2025) + land-use change per ward: built-up %, green cover, water bodies.")
card(s, 4.7, 2.3, 3.6, 2.5, "2  •  FORECAST HOTSPOTS", "ML model predicts 2030 heat-intensification zones: which wards will warm fastest as construction grows.", YELLOW)
card(s, 8.8, 2.3, 3.6, 2.5, "3  •  GUIDE ACTION", "Ward heat-risk ranking + planning suggestions: plantations, cool roofs, lake revival, building norms.", GREEN)
tx = s.shapes.add_textbox(Inches(0.6), Inches(5.2), Inches(12.1), Inches(0.6))
p = tx.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "One line: past heat  +  land-use change  →  future hotspots  →  planning decisions."
r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = YELLOW; r.font.name = FONT
footer(s, 4)
notes(s, "40 sec. Past, future, action. Point at each card. End with the one-line summary — judges remember one-liners.")

# ================= SLIDE 5 — Architecture =================
s = base_slide()
title_block(s, "How it will work", "System architecture: from satellite pixels to planner decisions")
steps = [
    ("SATELLITE DATA", "Landsat 8/9 LST\nSentinel-2 land-use\nMODIS, IMD"),
    ("PREPROCESS", "Cloud masking\nLST retrieval\nWard clipping"),
    ("FEATURES", "LST trend\nNDVI • NDBI\nBuilt-up %"),
    ("ML MODEL", "Random Forest\nXGBoost / LSTM\nTrain 2015→25"),
    ("FORECAST UI", "2030 hotspot map\nWard ranking\nAction tips"),
]
x = 0.45
for i, (t, d) in enumerate(steps):
    card(s, x, 2.4, 2.1, 2.2, t, d, tsize=12)
    if i < 4:
        ax = s.shapes.add_textbox(Inches(x + 2.12), Inches(3.2), Inches(0.4), Inches(0.5))
        p = ax.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = "▶"
        r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
    x += 2.5
tx = s.shapes.add_textbox(Inches(0.6), Inches(5.1), Inches(12.1), Inches(1.5))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Core science:  NDVI = (NIR−Red)/(NIR+Red)    •    NDBI = (SWIR−NIR)/(SWIR+NIR)    •    UHI intensity = LST(urban) − LST(rural)"
r.font.size = Pt(13); r.font.color.rgb = YELLOW; r.font.name = FONT
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER
r = p2.add_run(); r.text = "LST from Landsat Band 10 → emissivity-corrected → ward-level time-series → ML forecast (full derivation in Appendix B1)"
r.font.size = Pt(12); r.font.color.rgb = GRAY; r.font.name = FONT
footer(s, 5)
notes(s, "60 sec — most important slide. Walk left to right in 5 steps. Say one line on the science: LST corrected with NDVI emissivity, NDBI tracks concrete, UHI = urban minus rural. Point to appendix for derivation.")

# ================= SLIDE 6 — Tech stack =================
s = base_slide()
title_block(s, "Tech stack + data", "100% free & open stack — scalable to every Indian city")
rows, cols = 5, 3
gt = s.shapes.add_table(rows, cols, Inches(0.6), Inches(2.2), Inches(12.1), Inches(3.2)).table
data = [
    ("LAYER", "TOOLS", "WHY"),
    ("Satellite processing", "Google Earth Engine, Landsat 8/9, Sentinel-2, MODIS", "Free petabyte-scale data, no downloads"),
    ("Geo + ML pipeline", "Python, rasterio / GDAL, scikit-learn, XGBoost", "LST trends, drivers, ward forecasts"),
    ("Dashboard", "Streamlit / React + Leaflet maps, FastAPI", "Hotspot maps + rankings for planners"),
    ("Validation data", "IMD weather, Bhuvan, ground sensors (if available)", "Cross-check predicted hotspots"),
]
for i, row in enumerate(data):
    for j, val in enumerate(row):
        cell = gt.cell(i, j)
        cell.text_frame.word_wrap = True
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        cell.text_frame.paragraphs[0].add_run().text = val
style_table(gt, [2.6, 5.3, 4.2])
tx = s.shapes.add_textbox(Inches(0.6), Inches(5.7), Inches(12.1), Inches(0.5))
p = tx.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Zero data cost  •  No proprietary software  •  Works for Tier-1, Tier-2 and Tier-3 cities"
r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = GREEN; r.font.name = FONT
footer(s, 6)
notes(s, "30 sec. Stress FREE and SCALABLE — every dataset is open. That answers the judge's cost question before they ask.")

# ================= SLIDE 7 — Mockup + chart =================
s = base_slide()
title_block(s, "Expected output (proposed prototype)", "What the planner sees: hotspot map + trend + ward ranking")
# Left: zone legend cards
card(s, 0.6, 2.2, 3.4, 1.3, "🔴  HIGH-RISK WARDS", "LST ≥ 44 °C predicted by 2030\nAction: cool roofs, plantations", RED)
card(s, 0.6, 3.7, 3.4, 1.3, "🟡  WATCHLIST WARDS", "Fastest-warming trend 2015→25\nAction: protect green cover", YELLOW)
card(s, 0.6, 5.2, 3.4, 1.3, "🟢  COOL / SAFE WARDS", "Near lakes, parks, low built-up\nAction: preserve, replicate model", GREEN)
# Right: LST trend chart (sample data)
chart_data = ChartData()
chart_data.categories = ["2015", "2017", "2019", "2021", "2023", "2025", "2030*"]
chart_data.add_series("Mean summer LST (°C)", (38.2, 39.1, 40.0, 40.8, 42.1, 43.0, 44.6))
chart_data.add_series("Built-up %", (31, 34, 37, 40, 43, 46, 52))
cf = s.shapes.add_chart(XL_CHART_TYPE.LINE_MARKERS, Inches(4.4), Inches(2.2), Inches(4.2), Inches(3.0), chart_data)
ch = cf.chart
ch.has_title = True; ch.chart_title.text_frame.text = "Sample: LST vs built-up (illustrative)"
ch.chart_title.text_frame.paragraphs[0].runs[0].font.size = Pt(11)
ch.has_legend = True; ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
ch.value_axis.has_title = True; ch.value_axis.axis_title.text_frame.text = "°C / %"
# Ward ranking mini-table
rt = s.shapes.add_table(4, 3, Inches(8.9), Inches(2.2), Inches(3.5), Inches(3.0)).table
rdata = [("WARD", "LST 2025", "2030 RISK"),
         ("Ward 12 — Industrial", "43.8 °C", "🔴 High"),
         ("Ward 07 — Old City", "42.4 °C", "🔴 High"),
         ("Ward 21 — Lake Side", "38.1 °C", "🟢 Low")]
for i, row in enumerate(rdata):
    for j, val in enumerate(row):
        c = rt.cell(i, j)
        c.text_frame.word_wrap = True; c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.text_frame.paragraphs[0].add_run().text = val
style_table(rt)
tx = s.shapes.add_textbox(Inches(4.4), Inches(5.45), Inches(8.5), Inches(1.0))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]
r = p.add_run(); r.text = "ⓘ  Illustrative mockup with sample values — real values come from satellite pipeline after build.  *2030 = model forecast."
r.font.size = Pt(11); r.font.color.rgb = GRAY; r.font.name = FONT
footer(s, 7)
notes(s, "60 sec. Walk through: red/yellow/green zones, rising LST curve tracking built-up growth, ward ranking. Say honestly: illustrative mockup, real numbers after pipeline build.")

# ================= SLIDE 8 — Roadmap =================
s = base_slide()
title_block(s, "Implementation plan", "From idea to working MVP in 4 phases")
rows, cols = 5, 3
pt = s.shapes.add_table(rows, cols, Inches(0.6), Inches(2.2), Inches(12.1), Inches(3.4)).table
pdata = [
    ("PHASE", "TASKS", "OUTPUT"),
    ("1 • Data (weeks 1–2)", "GEE pipeline: Landsat LST 2015–25, Sentinel-2 land-use, ward boundaries", "Clean LST time-series for 1 pilot city"),
    ("2 • Model (weeks 3–4)", "Features (NDVI, NDBI, built-up %), train RF/XGBoost, validate vs IMD", "2030 ward-level heat forecast"),
    ("3 • Dashboard (weeks 5–6)", "Hotspot map + trends + rankings + action tips UI", "Working planner dashboard (MVP)"),
    ("4 • Pilot & scale (week 7+)", "Validate with ground data, extend to 2nd city, Heat Action Plan report", "Pilot report + multi-city template"),
]
for i, row in enumerate(pdata):
    for j, val in enumerate(row):
        c = pt.cell(i, j)
        c.text_frame.word_wrap = True; c.vertical_anchor = MSO_ANCHOR.MIDDLE
        c.text_frame.paragraphs[0].add_run().text = val
style_table(pt, [2.6, 6.4, 3.1])
footer(s, 8)
notes(s, "30 sec. Show you can execute. Emphasize: pilot ONE city first, then scale. Judges fear over-scoped projects — this calms them.")

# ================= SLIDE 9 — Impact =================
s = base_slide()
title_block(s, "Impact + users", "Built for the people who shape Indian cities")
bullets(s, [
    ("Municipal corporations & Smart City SPVs: ", "decide where to plant, where to pause concrete, where to mandate cool roofs."),
    ("Heat Action Plans (NDMA / IMD): ", "ward-level evidence for Ahmedabad-style plans in every heat-prone city."),
    ("Urban planners & builders: ", "check heat impact of new layouts before approval — a 'heat NOC' layer."),
    ("Citizens: ", "cooler wards, lower power bills, safer summers for outdoor workers & the elderly."),
    ("Scale of impact: ", "50+ Indian cities face severe UHI — one pipeline, replicated everywhere, at zero data cost."),
])
footer(s, 9)
notes(s, "40 sec — winner slide. Name real users: municipality, Smart City mission, NDMA. End with scale: 50+ cities, zero data cost.")

# ================= SLIDE 10 — Team =================
s = base_slide()
tx = s.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(5.8))
tf = tx.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "MEET THE TEAM"
r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = ACCENT; r.font.name = FONT
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.CENTER; p2.space_before = Pt(6)
r = p2.add_run(); r.text = "Thank You!"
r.font.size = Pt(54); r.font.bold = True; r.font.color.rgb = WHITE; r.font.name = FONT
members = [
    ("[Member 1 — Name]", "Team Lead • ML + Pipeline"),
    ("[Member 2 — Name]", "Remote Sensing • GEE + LST"),
    ("[Member 3 — Name]", "Backend • API + Data"),
    ("[Member 4 — Name]", "Frontend • Dashboard + Maps"),
    ("[Member 5 — Name]", "Research • Planning + Validation"),
    ("[Member 6 — Name]", "Design • PPT + Demo"),
]
for name, role in members:
    pm = tf.add_paragraph(); pm.alignment = PP_ALIGN.CENTER; pm.space_before = Pt(4)
    r = pm.add_run(); r.text = f"{name}  —  "
    r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = YELLOW; r.font.name = FONT
    r2 = pm.add_run(); r2.text = role
    r2.font.size = Pt(14); r2.font.color.rgb = WHITE; r2.font.name = FONT
pq = tf.add_paragraph(); pq.alignment = PP_ALIGN.CENTER; pq.space_before = Pt(14)
r = pq.add_run(); r.text = "Questions welcome  •  GitHub: [link]  •  Contact: [email]"
r.font.size = Pt(12); r.font.color.rgb = GRAY; r.font.name = FONT
footer(s, 10)
notes(s, "20 sec. Read roles fast, thank judges, invite questions. Have appendix ready if they ask about maths.")

# ================= SLIDE 11 — Backup B1 maths =================
s = base_slide()
title_block(s, "Appendix B1 — show only if asked", "The maths: LST retrieval + UHI + forecast model")
tx = s.shapes.add_textbox(Inches(0.6), Inches(2.1), Inches(12.1), Inches(4.6))
tf = tx.text_frame; tf.word_wrap = True
lines = [
    ("Step 1 — Radiance:  ", "Lλ = ML × DN + AL   (ML, AL from Landsat metadata)"),
    ("Step 2 — Brightness temp:  ", "BT = K2 / ln(K1/Lλ + 1) − 273.15   (K1, K2 band constants, °C)"),
    ("Step 3 — Vegetation fraction:  ", "Pv = [(NDVI − NDVImin)/(NDVImax − NDVImin)]²"),
    ("Step 4 — Emissivity:  ", "ε = 0.004 × Pv + 0.986"),
    ("Step 5 — Final LST:  ", "LST = BT / [ 1 + (λ·BT/ρ)·ln(ε) ],  ρ = 1.4388×10⁻² m·K"),
    ("UHI intensity:  ", "UHI = mean LST(urban wards) − mean LST(rural buffer)"),
    ("Trend per pixel:  ", "slope of linear fit LST vs year, 2015–2025 (°C/year)"),
    ("Forecast model:  ", "LST2030 = f(LST history, NDVI, NDBI, built-up %)  •  validated with RMSE & R² vs IMD"),
]
first = True
for head, rest in lines:
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    first = False
    p.space_after = Pt(8)
    r = p.add_run(); r.text = "▸  " + head
    r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = YELLOW; r.font.name = "Consolas"
    r2 = p.add_run(); r2.text = rest
    r2.font.size = Pt(14); r2.font.color.rgb = WHITE; r2.font.name = "Consolas"
footer(s, 11)
notes(s, "Backup only. If asked 'how do you compute LST', walk through steps 1-5, then UHI and model line. Keep under 60 sec.")

from pathlib import Path as _P
_OUT = _P(__file__).resolve().parent / "HeatSight_UHI_PPT.pptx"
prs.save(str(_OUT))
print(f"Saved {_OUT}")

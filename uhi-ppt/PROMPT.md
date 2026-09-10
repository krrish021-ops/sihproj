# Full Prompt for AI PPT Makers (Gamma / Canva Magic / Copilot / Beautiful.ai)

Copy everything inside the box below and paste it into your AI presentation tool:

---

```
Create an 11-slide hackathon pitch deck titled "HeatSight: Forecasting Urban Heat Islands
for Climate-Smart Indian Cities" for Smart India Hackathon 2026.

TOPIC: Urban Heat Island forecasting using satellite LST (Land Surface Temperature)
time-series + land-use data to predict heat intensification in growing Indian cities,
feeding into urban planning. NOTE: No prototype is built yet — this is an idea-stage
pitch, so show a "proposed dashboard mockup with illustrative sample values".

DESIGN: Dark navy background (#0F1B2D), heat-orange accents (#FF6B35), yellow
highlights (#FFC300), white text, modern tech style, 16:9. One idea per slide,
max 5 bullets, big visuals, minimal text.

SLIDES:

1. TITLE — "HeatSight: Forecasting Urban Heat Islands for Climate-Smart Indian Cities",
tagline "Satellite LST time-series + land-use data → ward-level heat forecast for
urban planners", Team [Your Team Name], [College Name], Hackathon 2026. Visual:
satellite thermal heatmap of an Indian city.

2. THE PROBLEM: "Indian cities are becoming heat traps" — Define Urban Heat Island
(UHI): city zones 3–7 °C hotter than rural surroundings. Bullets: deadly heatwaves
(Delhi 50 °C+), concrete replacing green cover, energy/health bills exploding,
planners have no ward-level forecast tool.

3. WHY EXISTING SOLUTIONS FAIL: "Weather apps tell temperature — nobody predicts
heat islands" — IMD gives city-average air temp only; research papers are static
one-time maps; smart-city dashboards track AQI/traffic but not heat; gap = no open
tool linking satellite LST + land-use → future forecast.

4. PROPOSED IDEA: "HeatSight: a heat-forecast copilot for urban planners" — 3 cards:
(1) MAP THE PAST: 10-year satellite LST + land-use change per ward;
(2) FORECAST HOTSPOTS: ML predicts 2030 intensification zones;
(3) GUIDE ACTION: ward risk ranking + suggestions (plantations, cool roofs,
lake revival). One-liner: past heat + land-use change → future hotspots → decisions.

5. HOW IT WILL WORK (architecture diagram, 5 steps left→right): SATELLITE DATA
(Landsat 8/9 LST, Sentinel-2, MODIS, IMD) → PREPROCESS (cloud masking, LST
retrieval, ward clipping) → FEATURES (LST trend, NDVI, NDBI, built-up %) →
ML MODEL (Random Forest / XGBoost / LSTM) → FORECAST UI (2030 hotspot map, ward
ranking, action tips). Footer formulas: NDVI=(NIR−Red)/(NIR+Red),
NDBI=(SWIR−NIR)/(SWIR+NIR), UHI = LST(urban)−LST(rural).

6. TECH STACK + DATA (table: Layer | Tools | Why): Satellite processing = Google
Earth Engine, Landsat 8/9, Sentinel-2, MODIS (free, no downloads); Geo+ML = Python,
rasterio/GDAL, scikit-learn, XGBoost; Dashboard = Streamlit/React + Leaflet, FastAPI;
Validation = IMD, Bhuvan, ground sensors. Banner: "Zero data cost, works for Tier-1/2/3 cities".

7. EXPECTED OUTPUT — PROPOSED DASHBOARD MOCKUP (label: illustrative sample values):
red/yellow/green ward risk zones, a rising line chart of mean summer LST vs built-up %
2015→2030, and a ward ranking table (Ward 12 Industrial 43.8 °C High; Ward 07 Old City
42.4 °C High; Ward 21 Lake Side 38.1 °C Low).

8. IMPLEMENTATION PLAN (table: Phase | Tasks | Output): Phase 1 weeks 1–2 data pipeline
in GEE for 1 pilot city; Phase 2 weeks 3–4 model training + IMD validation; Phase 3
weeks 5–6 dashboard MVP; Phase 4 week 7+ ground validation + 2nd city + Heat Action
Plan report.

9. IMPACT + USERS: "Built for the people who shape Indian cities" — municipal
corporations & Smart City SPVs, Heat Action Plans (NDMA/IMD), planners/builders
("heat NOC" layer), citizens (cooler wards, lower bills), scale: 50+ Indian cities,
one pipeline, zero data cost.

10. TEAM + THANK YOU — 6 placeholders with roles (ML, Remote Sensing, Backend,
Frontend, Research, Design), "Questions welcome", GitHub + contact placeholders.

11. APPENDIX B1 (backup, maths): LST retrieval steps — Lλ=ML×DN+AL;
BT=K2/ln(K1/Lλ+1)−273.15; Pv=[(NDVI−NDVImin)/(NDVImax−NDVImin)]²; ε=0.004×Pv+0.986;
LST=BT/[1+(λBT/ρ)ln ε]; UHI=urban−rural LST; trend slope °C/year; forecast
LST2030=f(history, NDVI, NDBI, built-up%), RMSE & R² validation.

Add speaker notes (20–60 sec script) for every slide.
```

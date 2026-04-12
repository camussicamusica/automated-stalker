# 📜 Scripts

## `nuno_competition.py` — The Darwin Engine
The main script. Queries YouTube Data API across 8 niche search terms to discover competitor channels, then runs a **Darwinian evolutionary scoring algorithm** across 7 weighted dimensions (audience size, niche overlap, webinar strategy, offer structure, etc.). Runs 3 elimination generations — survival of the fittest. Outputs ranked CSV, top 3 report TXT, and Nuno vs competitors comparison CSV.

**Run it:**
```bash
cat > 01_Scripts/README.md << 'EOF'
# 📜 Scripts

## `nuno_competition.py` — The Darwin Engine
The main script. Queries YouTube Data API across 8 niche search terms to discover competitor channels, then runs a **Darwinian evolutionary scoring algorithm** across 7 weighted dimensions (audience size, niche overlap, webinar strategy, offer structure, etc.). Runs 3 elimination generations — survival of the fittest. Outputs ranked CSV, top 3 report TXT, and Nuno vs competitors comparison CSV.

**Run it:**
```bash
python3 nuno_competition.py
```
Requires: YouTube Data API v3 key

---

## `2. report.py` — The Visualizer
Takes the CSV output from `nuno_competition.py` and generates the first interactive HTML report (`competitor_report.html`). Dark theme, sortable candidate table, fitness score bars, algorithm explanation section, and Chart.js comparison chart.

**Run it:**
```bash
python3 "2. report.py"
```
Requires: `competitor_analysis.csv` in same folder

---

## `3. report2.py` — The Deep Enricher
Takes the 28 discovered candidates and runs a deep link discovery search on each one — finding their real website, YouTube, LinkedIn, Instagram, course pages, and webinar registration pages. Generates an enriched CSV and a second HTML report (`competitor_final_report.html`) with clickable links, webinar intelligence table, and digital footprint chart per candidate.

**Run it:**
```bash
python3 "3. report2.py"
```
Requires: `competitor_analysis.csv` in same folder

---

> Note: The final deep intelligence on the Top 3 (`top3_intelligence.txt` and `top3_final.html`) was produced using **Claude Code + RivalSearchMCP** — not a Python script. See root README for details.

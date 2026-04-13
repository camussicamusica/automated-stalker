# 🤖 automated-stalker

> "The steps everyone skips — a Darwinian algorithm that stalks Nuno's competitors so you don't have to. Pretty darn cool."

Built for **Nuno Tavares (Automated Marketer)** as part of a webinar launch competitive intelligence project.

## 🏆 Live Report
👉 **[View Interactive HTML Report](https://camussicamusica.github.io/automated-stalker/)**
👉 **[View Algorithm SOP — The Darwin Engine](https://camussicamusica.github.io/automated-stalker/algorithm_sop.html)**

## 🧬 What This Does
A Darwinian evolutionary scoring algorithm that:
1. Queries YouTube Data API across 8 niche search terms
2. Discovers 28 competitor candidates in the AI/no-code space
3. Scores each on 7 weighted dimensions (audience, niche, webinar strategy, etc.)
4. Runs 3 generations of elimination — survival of the fittest
5. Deep-stalks the top 3 finalists across all platforms
6. Generates a full interactive HTML intelligence report

## 🏅 Top 3 Competitors Found

### V1 — Algorithm Output (Organic YouTubers)
| Rank | Creator | Subscribers | Est. Revenue |
|------|---------|-------------|--------------|
| 🥇 | Nick Saraev | 377K | $160K–$300K+/mo |
| 🥈 | Riley Brown | 211K | VC-funded ($9.4M) |
| 🥉 | Nate Herk | 648K | $200K–$350K/mo |

### V2 — Manual Research Output (Paid-Funnel Operators)
| Rank | Creator | YouTube Subs | High-Ticket Price | GHL Connection |
|------|---------|-------------|-------------------|----------------|
| 🥇 | Liam Ottley | ~730K | $5,000–$7,150 (AAA Accelerator) | None |
| 🥈 | Jordan Platten | ~375K | $3,800–$4,500 (Agency Launch) | Confirmed Affiliate |
| 🥉 | Billy Gene | ~300K–400K | ~$5,000–$10,000+ (Accelerator) | Co-Marketing Partner |

> **Why V2?** The V1 algorithm found organic-only creators. Nuno runs Facebook/Instagram ads and has an active sales funnel. V2 applied the missing filter: **YouTube ✓ + Active Facebook ads ✓ + Confirmed sales funnel ✓ + GHL connection ✓**

## 💡 Key Strategic Finding
**None of the V1 top 3 competitors run public webinars.**
Nuno's webinar is completely uncontested in this space.

**V2 Finding:** The GHL + AI + Organic YouTube slot is unfilled. Liam Ottley has 730K subs but no GHL. Jordan Platten has GHL but is UK-centric. Billy Gene has GHL but relies on paid ads. Nuno sits in the gap.

## 🛠 Stack
- Python 3 + YouTube Data API v3
- BeautifulSoup + requests (web scraping)
- Pandas (scoring matrix)
- googlesearch-python
- **[RivalSearchMCP](https://github.com/damionrashford/RivalSearchMCP)** — used for deep competitor stalking via Claude Code (Cloudflare bypass, multi-engine search, website traversal)

## 📁 Structure
\`\`\`
automated-stalker/
├── 01_Scripts/    # Python scripts
├── 02_Data/       # CSVs + raw research TXTs
├── 03_Reports/    # HTML reports
└── 04_Archive/    # Older iterations
\`\`\`

## 🚀 How to Run
\`\`\`bash
pip install requests beautifulsoup4 pandas googlesearch-python google-api-python-client
python3 01_Scripts/nuno_competition.py
\`\`\`

## 🧠 Built with NunoBrain
This project was built as Phase 1 of a full webinar launch strategy for the Automated Marketer brand.

---
*Vibe-coded with Claude Code + RivalSearchMCP. Pretty darn cool. 🤖*

## 📎 AI Conversation Citations

### Phase 1 — April 11–12, 2026 (V1 Research)

#### 🤖 Claude Sonnet 4.6 (Anthropic, claude.ai)
- [Conversation 1](https://claude.ai/share/c7992f5f-f1ce-442d-988e-d29d8be77d86)
- [Conversation 2](https://claude.ai/share/8f0f8190-132d-4c63-a136-8bf2f8d02b91)
- [Conversation 3](https://claude.ai/share/fed341c9-ab17-454f-b1d5-a7fdf3230fc1)
- [Conversation 4](https://claude.ai/share/3bc08b45-ab22-433b-b734-deeb99aa9ae4)

#### 💎 Google Gemini 2.5 Pro (Google, gemini.google.com)
- [Conversation 1](https://gemini.google.com/share/7fae70229974)
- [Conversation 2](https://gemini.google.com/share/7d3034e042bf)
- [Conversation 3](https://gemini.google.com/share/9d253dea0799)
- [Conversation 4](https://gemini.google.com/share/d9c7a8d036b5)

#### ⚡ Claude Code + RivalSearchMCP
- [Terminal Session Log](https://github.com/camussicamusica/automated-stalker/blob/main/02_Data/session_transcript.txt)

*All Phase 1 conversations conducted by Sofia Renata Camussi, April 11–12, 2026*

---

## 🧠 AI Conversations — Research Log (April 12–13, 2026)

### Phase 2 — V2 Research: Process Brief + Competitor Intelligence

| Session | Model | What Happened |
|---------|-------|---------------|
| April 12 — V2 Research | Claude Sonnet 4.6 (Claude Code) | Ran `today.py` · Diagnosed V1 algorithm flaw (organic-only creators) · Wrote PROCESS_BRIEF.txt · Ran RivalSearchMCP competitor intelligence on Liam Ottley, Jordan Platten, Billy Gene · Produced `competitor_intelligence_report_2026.txt` |
| April 13 — GitHub Pages | Claude Sonnet 4.6 (Claude Code) | Created `process_brief.html` + `v2_intel.html` · Updated nav across all V1 pages · Added V1 banner to index.html · Updated README |

#### 🤖 Claude Sonnet 4.6 — V2 Research Sessions (claude.ai/code)
| Session | Date | Description |
|---------|------|-------------|
| [V2 Competitor Intelligence](https://claude.ai/share/c7992f5f-f1ce-442d-988e-d29d8be77d86) | April 12–13, 2026 | RivalSearchMCP deep research on Liam Ottley, Jordan Platten, Billy Gene · Process Brief writing · GitHub Pages restructure |

#### Key V2 Research Outputs
- **Algorithm Flaw Identified:** V1 assumed YouTubers + AI topics = paid funnel operators. Wrong. The missing filter: `YouTube ✓ + FB ads ✓ + sales funnel ✓ + GHL ✓`
- **GHL Pivot:** Used GoHighLevel award winners as the seed pool instead of generic YouTube search
- **Process Brief:** `PROCESS_BRIEF.txt` — full narrative of April 12 research day (416 files, 00:25–23:37)
- **Intelligence Report:** `competitor_intelligence_report_2026.txt` — 7 sections per competitor, pricing tables, funnel maps, social stats, GHL analysis

*All Phase 2 conversations conducted by Sofia Renata Camussi, April 12–13, 2026*

---

## 🖥️ Claude Code Session Logs

Full terminal session transcripts are stored in `02_Data/`:

- [`session_transcript.txt`](02_Data/session_transcript.txt) — Session 1: algorithm build, scraping, deep intel, report generation
- [`session_transcript_2.txt`](02_Data/session_transcript_2.txt) — Session 2: UI polish, animations, nav, repo restructure

### Session 2 Summary — April 12, 2026

| Task | What was done |
|------|---------------|
| CSS glitch animation | Added `@keyframes` RGB-split glitch to all 5 hero titles (hub, index, sop, iteration1, funnelipc) |
| Nav reorder | Moved "View Report" to first position across all 36 HTML files via Python bulk-replace |
| Nav cleanup | Removed "Evolution Matrix" from Intelligence dropdown (36 files) |
| Content removal | Removed Digital Footprint Discovery section from competitors28 |
| Hero layout fix | Fixed hub.html tag stacking (flex column) after inline-block glitch broke layout |
| Script execution | Ran `reorganize_repo.sh`, `fix_links.sh`, `fix_competitors28_responsive.sh` (with macOS compat fixes) |
| Repo restructure | `pages/` → `06_Presentation/` · `assets/` + `report_cards/` + `brain/` → `05_Assets/` · scripts → `01_Scripts/` |
| Link fixing | Two rounds of bulk link repair across 36+ files after each folder move |
| Glitch speed | Animation duration 4s → 2s on all titles |
| GitHub Pages | Root redirect stubs for all old URLs (hub, funnelipc, algorithm_sop, etc.) |

*Built with Claude Code (claude-sonnet-4-6) · All terminal work by Sofia Renata Camussi*

# 🤖 automated-stalker

> "The steps everyone skips — a Darwinian algorithm that stalks Nuno's competitors so you don't have to. Pretty darn cool."

Built for **Nuno Tavares (Automated Marketer)** as part of a webinar launch competitive intelligence project.

## 🏆 Live Report
👉 **[View Interactive HTML Report](https://camussicamusica.github.io/automated-stalker/)**

## 🧬 What This Does
A Darwinian evolutionary scoring algorithm that:
1. Queries YouTube Data API across 8 niche search terms
2. Discovers 28 competitor candidates in the AI/no-code space
3. Scores each on 7 weighted dimensions (audience, niche, webinar strategy, etc.)
4. Runs 3 generations of elimination — survival of the fittest
5. Deep-stalks the top 3 finalists across all platforms
6. Generates a full interactive HTML intelligence report

## 🏅 Top 3 Competitors Found
| Rank | Creator | Subscribers | Est. Revenue |
|------|---------|-------------|--------------|
| 🥇 | Nick Saraev | 377K | $160K–$300K+/mo |
| 🥈 | Riley Brown | 211K | VC-funded ($9.4M) |
| 🥉 | Nate Herk | 648K | $200K–$350K/mo |

## 💡 Key Strategic Finding
**None of the top 3 competitors run public webinars.**
Nuno's webinar is completely uncontested in this space.

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

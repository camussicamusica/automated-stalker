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

## 📎 AI Conversation Citations

### 🤖 Claude Sonnet 4.6 (Anthropic, claude.ai)
- [Conversation 1](https://claude.ai/share/c7992f5f-f1ce-442d-988e-d29d8be77d86)
- [Conversation 2](https://claude.ai/share/8f0f8190-132d-4c63-a136-8bf2f8d02b91)
- [Conversation 3](https://claude.ai/share/fed341c9-ab17-454f-b1d5-a7fdf3230fc1)
- [Conversation 4](https://claude.ai/share/3bc08b45-ab22-433b-b734-deeb99aa9ae4)

### 💎 Google Gemini 2.5 Pro (Google, gemini.google.com)
- [Conversation 1](https://gemini.google.com/share/7fae70229974)
- [Conversation 2](https://gemini.google.com/share/7d3034e042bf)
- [Conversation 3](https://gemini.google.com/share/9d253dea0799)
- [Conversation 4](https://gemini.google.com/share/d9c7a8d036b5)

### ⚡ Claude Code + RivalSearchMCP
- [Terminal Session Log](https://github.com/camussicamusica/automated-stalker/blob/main/02_Data/session_transcript.txt)

*All conversations conducted by Sofia Renata Camussi, April 11, 2026*

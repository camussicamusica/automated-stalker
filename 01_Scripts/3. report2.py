import os
import time
import re
import json
import webbrowser
import requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
from googlesearch import search

# =============================================================
# SETTINGS & PATHS
# =============================================================
BASE_PATH = "/Users/sofiarenata/Desktop/PARETO_FINAL_PROJECT/1. Python Processes/5. Nuno's Competitors/"
INPUT_FILE = os.path.join(BASE_PATH, "competitor_analysis.csv")
ENRICHED_CSV = os.path.join(BASE_PATH, "deep_enriched.csv")
FINAL_HTML = os.path.join(BASE_PATH, "competitor_final_report.html")
ERROR_LOG = os.path.join(BASE_PATH, "errors.log")

# Ensure base path exists
os.makedirs(BASE_PATH, exist_ok=True)

# =============================================================
# KEEP THIS FUNCTION EXACTLY AS-IS
# =============================================================
def deep_search(name, query_suffix, keywords, exclude_keywords=None):
    query = f"{name} {query_suffix}"
    print(f"  🔍 Searching: {query}")
    try:
        # Mandatory sleep to prevent Google blocks
        time.sleep(5)
        for url in search(query, num_results=5):
            url_lower = url.lower()
            if exclude_keywords and any(x in url_lower for x in exclude_keywords):
                continue
            if any(k in url_lower for k in keywords):
                print(f"    ✅ Found: {url}")
                return url
        return "Not Found"
    except Exception as e:
        with open(ERROR_LOG, "a") as log:
            log.write(f"[{datetime.now()}] Search Error ({query}): {e}\n")
        print(f"    ❌ Error: {e}")
        return "Not Found"

# =============================================================
# STEP 1 — READ CSV AND BUILD CANDIDATE LIST
# =============================================================
print("📊 Loading input data...")
try:
    df_raw = pd.read_csv(INPUT_FILE)
    # Filter: subs >= 1000 and sort by Fitness
    df_filtered = df_raw[df_raw['subs'] >= 1000].copy()
    df_filtered = df_filtered.sort_values(by='Total_Fitness', ascending=False)
    
    candidates_list = df_filtered.to_dict('records')
    # Identify Top 3
    top3_names = [c['name'] for c in candidates_list[:3]]
    
    print(f"🚀 Processing {len(candidates_list)} candidates (Subs >= 1k).")
    print(f"⭐ Top 3 Finalists: {', '.join(top3_names)}")
except Exception as e:
    print(f"CRITICAL ERROR reading CSV: {e}")
    exit()

# =============================================================
# STEP 2 & 3 — DEEP SEARCH & SCRAPING LOOP
# =============================================================
enriched_results = []

for idx, cand in enumerate(candidates_list, 1):
    name = cand['name']
    print(f"\n[{idx}/{len(candidates_list)}] ANALYZING: {name.upper()}")
    
    # Search 1 — Website
    website = deep_search(
        name, "official website",
        keywords=[".com", ".io", ".co", ".net", ".org"],
        exclude_keywords=["youtube.com", "linkedin.com", "instagram.com", "facebook.com", "twitter.com", "x.com", "google.com"]
    )
    
    # Search 2 — YouTube
    yt_found = deep_search(
        name, "YouTube channel",
        keywords=["youtube.com/@", "youtube.com/c", "youtube.com/user", "youtube.com/channel"]
    )
    youtube = yt_found if yt_found != "Not Found" else cand.get('channel_url', 'Not Found')
    
    # Search 3 — LinkedIn
    linkedin = deep_search(name, "LinkedIn", keywords=["linkedin.com/in", "linkedin.com/company"])
    
    # Search 4 — Instagram
    instagram = deep_search(name, "Instagram", keywords=["instagram.com/"])
    
    # Search 5 — Webinar
    webinar_url = deep_search(
        name, "webinar register live training masterclass",
        keywords=["webinar", "register", "masterclass", "workshop", "bootcamp", "live-training", "challenge", "summit", "event"]
    )
    has_webinar = webinar_url != "Not Found"
    
    # Search 6 — Course
    course_url = deep_search(
        name, "course buy enroll skool community",
        keywords=["skool.com", "course", "enroll", "pricing", "product", "offer", "academy", "membership", "learn", "shop", "buy", "join"]
    )
    
    # Search 7 — Twitter
    twitter = deep_search(name, "Twitter X account", keywords=["twitter.com/", "x.com/"])
    
    # Site Scraping Logic
    site_headline = "Not Found"
    site_sections = "Not Found"
    site_cta = "Not Found"
    has_pricing = False
    
    if website != "Not Found":
        print(f"  🌐 Scraping homepage: {website}")
        try:
            resp = requests.get(website, headers={"User-Agent":"Mozilla/5.0"}, timeout=8)
            if resp.status_code == 429:
                print("    ⚠️ Rate limited (429). Waiting 45s...")
                time.sleep(45)
                resp = requests.get(website, headers={"User-Agent":"Mozilla/5.0"}, timeout=8)
            
            time.sleep(2)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Headline
            h1 = soup.find('h1')
            if h1: site_headline = h1.get_text().strip()
            
            # Sections
            h2s = [h.get_text().strip() for h in soup.find_all('h2')[:4]]
            if h2s: site_sections = " · ".join(h2s)
            
            # CTA
            btn = soup.find('button')
            if not btn:
                btn = soup.find('a', class_=re.compile(r'btn', re.I))
            if btn: site_cta = btn.get_text().strip()
            
            # Pricing check
            if "$" in resp.text: has_pricing = True
            
            print(f"    ✅ Scraped: \"{site_headline[:40]}...\"")
            
        except Exception as e:
            with open(ERROR_LOG, "a") as log:
                log.write(f"[{datetime.now()}] Scrape Error ({website}): {e}\n")
            print(f"    ❌ Scrape failed: {e}")

    # Prepare entry
    entry = cand.copy()
    entry.update({
        "website": website, "youtube": youtube, "linkedin": linkedin,
        "instagram": instagram, "twitter": twitter, "webinar_url": webinar_url,
        "has_webinar": has_webinar, "course_url": course_url,
        "site_headline": site_headline, "site_sections": site_sections,
        "site_cta": site_cta, "has_pricing": has_pricing
    })
    enriched_results.append(entry)

# =============================================================
# STEP 4 — SAVE ENRICHED CSV
# =============================================================
df_enriched = pd.DataFrame(enriched_results)
df_enriched.to_csv(ENRICHED_CSV, index=False)
print(f"\n✅ CSV saved: {ENRICHED_CSV}. Generating HTML...")

# =============================================================
# STEP 5 — GENERATE HTML
# =============================================================

# Stats for Header
total_analyzed = len(enriched_results)
webs_found = len(df_enriched[df_enriched['website'] != "Not Found"])
webs_active = len(df_enriched[df_enriched['has_webinar'] == True])
courses_found = len(df_enriched[df_enriched['course_url'] != "Not Found"])

# JSON Data for JS
json_data = []
for i, r in df_enriched.iterrows():
    json_data.append({
        "name": r['name'],
        "rank": i + 1,
        "isTop3": r['name'] in top3_names,
        "fitness": r['Total_Fitness'],
        "subs": int(r['subs']),
        "bio": str(r.get('bio', 'No bio available')),
        "website": r['website'],
        "youtube": r['youtube'],
        "linkedin": r['linkedin'],
        "instagram": r['instagram'],
        "twitter": r['twitter'],
        "webinar_url": r['webinar_url'],
        "has_webinar": r['has_webinar'],
        "course_url": r['course_url'],
        "site_headline": r['site_headline'],
        "site_sections": r['site_sections'],
        "has_pricing": r['has_pricing'],
        "top_videos": str(r.get('top_videos', 'N/A')),
        "video_count": r.get('video_count', 0),
        "ghl_connected": r.get('ghl_connected', False)
    })

html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NunoBrain Competitor Intelligence</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg: #0a0f1e; --card-bg: #111827; --blue: #00d4ff; --gold: #ffd700;
            --silver: #c0c0c0; --bronze: #cd7f32; --green: #10b981; --orange: #f59e0b;
            --red: #ef4444; --grey: #374151; --text: #f3f4f6;
        }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Inter', system-ui, sans-serif; margin: 0; line-height: 1.5; }}
        
        /* HERO */
        header {{ padding: 60px 20px; text-align: center; background: linear-gradient(180deg, #111827 0%, #0a0f1e 100%); border-bottom: 1px solid var(--grey); }}
        header h1 {{ font-size: 3.5rem; margin: 0; letter-spacing: -2px; text-transform: uppercase; }}
        header h2 {{ color: var(--blue); font-size: 1.2rem; margin: 10px 0; letter-spacing: 2px; }}
        .stats-row {{ display: flex; justify-content: center; gap: 30px; margin-top: 40px; flex-wrap: wrap; }}
        .stat-item {{ text-align: center; min-width: 150px; }}
        .stat-val {{ font-size: 2.5rem; font-weight: 800; color: var(--text); display: block; }}
        .stat-label {{ color: var(--blue); font-size: 0.8rem; text-transform: uppercase; font-weight: bold; }}

        /* FILTER BAR */
        .filter-bar {{ position: sticky; top: 0; z-index: 100; background: rgba(10, 15, 30, 0.9); backdrop-filter: blur(10px); 
                       padding: 15px 20px; border-bottom: 1px solid var(--grey); display: flex; justify-content: space-between; align-items: center; }}
        .pills {{ display: flex; gap: 10px; }}
        .pill {{ padding: 8px 16px; border-radius: 20px; border: 1px solid var(--grey); background: none; color: white; cursor: pointer; transition: 0.2s; }}
        .pill.active {{ background: var(--blue); border-color: var(--blue); color: #000; font-weight: bold; }}
        #searchInput {{ padding: 8px 15px; border-radius: 20px; border: 1px solid var(--grey); background: var(--card-bg); color: white; width: 250px; }}

        /* GRID */
        .container {{ max-width: 1400px; margin: 40px auto; padding: 0 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(400px, 1fr)); gap: 25px; }}
        
        /* CARDS */
        .card {{ background: var(--card-bg); border-radius: 12px; border: 1px solid var(--grey); padding: 25px; position: relative; transition: transform 0.3s; }}
        .card:hover {{ transform: translateY(-5px); }}
        
        /* TOP 3 SPECIAL */
        .top3-section {{ grid-column: 1 / -1; display: flex; gap: 25px; margin-bottom: 50px; flex-wrap: wrap; }}
        .top3-card {{ flex: 1; min-width: 400px; border-width: 3px !important; }}
        .gold {{ border-color: var(--gold) !important; box-shadow: 0 0 30px rgba(255,215,0,0.15); }}
        .silver {{ border-color: var(--silver) !important; box-shadow: 0 0 30px rgba(192,192,192,0.1); }}
        .bronze {{ border-color: var(--bronze) !important; box-shadow: 0 0 30px rgba(205,127,50,0.1); }}
        .rank-badge {{ font-size: 2rem; position: absolute; top: -15px; left: -15px; background: var(--card-bg); border-radius: 50%; width: 50px; height: 50px; display: flex; align-items: center; justify-content: center; border: 2px solid inherit; }}

        /* CARD INTERNALS */
        .card-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px; }}
        .card-header h3 {{ margin: 0; font-size: 1.4rem; }}
        .fitness {{ background: var(--blue); color: black; padding: 2px 10px; border-radius: 5px; font-weight: 800; font-size: 0.9rem; }}
        .stats {{ color: var(--silver); font-size: 0.9rem; margin-bottom: 20px; }}
        .links-row {{ display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; font-size: 0.85rem; }}
        .links-row a {{ color: var(--blue); text-decoration: none; }}
        .links-row .not-found {{ color: #4b5563; }}
        
        .webinar-box {{ padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid transparent; }}
        .has-web {{ background: rgba(16,185,129,0.1); border-color: var(--green); }}
        .no-web {{ background: rgba(55,65,81,0.2); border-color: var(--grey); color: #9ca3af; }}
        
        .site-intel {{ background: #1f2937; padding: 15px; border-radius: 8px; margin-top: 15px; font-size: 0.85rem; }}
        .headline {{ font-style: italic; color: var(--silver); display: block; margin-bottom: 8px; }}
        
        .collapsible {{ cursor: pointer; color: var(--blue); font-size: 0.8rem; margin-top: 10px; }}
        .content {{ display: none; margin-top: 10px; font-size: 0.8rem; color: #9ca3af; }}
        
        /* TABLE & CHART */
        .section-title {{ font-size: 1.8rem; margin: 60px 0 30px; border-left: 5px solid var(--blue); padding-left: 15px; }}
        table {{ width: 100%; border-collapse: collapse; background: var(--card-bg); border-radius: 10px; overflow: hidden; }}
        th, td {{ padding: 15px; text-align: left; border-bottom: 1px solid var(--grey); }}
        th {{ background: #1f2937; color: var(--blue); }}
        .chart-container {{ background: var(--card-bg); padding: 30px; border-radius: 12px; height: 500px; }}
        
        footer {{ text-align: center; padding: 60px; color: #4b5563; border-top: 1px solid var(--grey); margin-top: 100px; }}
    </style>
</head>
<body>

<header>
    <h2>COMPETITOR INTELLIGENCE REPORT</h2>
    <h1>NUNO TAVARES</h1>
    <p>AI & No-Code Webinar Space · Generated {datetime.now().strftime("%Y-%m-%d")}</p>
    <div class="stats-row">
        <div class="stat-item"><span class="stat-val" id="count-total">0</span><span class="stat-label">Analyzed</span></div>
        <div class="stat-item"><span class="stat-val" id="count-webs">0</span><span class="stat-label">Websites Found</span></div>
        <div class="stat-item"><span class="stat-val" id="count-master">0</span><span class="stat-label">Webinars Active</span></div>
        <div class="stat-item"><span class="stat-val" id="count-course">0</span><span class="stat-label">Course Hubs</span></div>
    </div>
</header>

<div class="filter-bar">
    <div class="pills">
        <button class="pill active" onclick="filterCards('all', this)">👥 All</button>
        <button class="pill" onclick="filterCards('top3', this)">⭐ Top 3</button>
        <button class="pill" onclick="filterCards('webinar', this)">✅ Webinar</button>
        <button class="pill" onclick="filterCards('course', this)">🎓 Course</button>
        <button class="pill" onclick="filterCards('website', this)">🌐 Website</button>
    </div>
    <input type="text" id="searchInput" placeholder="Search by name..." onkeyup="searchNames()">
</div>

<div class="container">
    <div id="top3-grid" class="top3-section"></div>
    <div id="main-grid" class="grid"></div>

    <h2 class="section-title">🎯 Webinar Intelligence — Active Events Found</h2>
    <table id="webinarTable">
        <thead>
            <tr><th>Rank</th><th>Name</th><th>Subscribers</th><th>Webinar Link</th><th>Course Link</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <h2 class="section-title">Digital Footprint Discovery</h2>
    <div class="chart-container">
        <canvas id="footprintChart"></canvas>
    </div>
</div>

<footer>
    Generated by NunoBrain Intelligence System · {datetime.now().strftime("%Y-%m-%d")}<br>
    Data sourced via automated public web search for Nuno Tavares's 2026 Webinar Launch Strategy
</footer>

<script>
    const candidates = {json.dumps(json_data)};

    function renderCards() {{
        const mainGrid = document.getElementById('main-grid');
        const top3Grid = document.getElementById('top3-grid');
        const tableBody = document.querySelector('#webinarTable tbody');
        
        mainGrid.innerHTML = '';
        top3Grid.innerHTML = '';
        tableBody.innerHTML = '';

        candidates.forEach(c => {{
            const isWeb = c.has_webinar;
            const isCourse = c.course_url !== "Not Found";
            const isSite = c.website !== "Not Found";
            
            let borderStyle = 'border: 1px solid var(--grey)';
            if(isWeb && isCourse) borderStyle = 'border: 1px solid var(--blue); box-shadow: 0 0 15px rgba(0,212,255,0.2)';
            else if(isWeb) borderStyle = 'border: 1px solid var(--green)';
            else if(isCourse) borderStyle = 'border: 1px solid var(--orange)';

            const cardHtml = `
                <div class="card ${{c.isTop3 ? 'top3-card ' + (c.rank==1?'gold':c.rank==2?'silver':'bronze') : ''}}" 
                     style="${{borderStyle}}"
                     data-name="${{c.name.toLowerCase()}}"
                     data-webinar="${{isWeb}}" data-course="${{isCourse}}" data-top3="${{c.isTop3}}" data-site="${{isSite}}">
                    
                    ${{c.isTop3 ? `<div class="rank-badge">${{c.rank==1?'🥇':c.rank==2?'🥈':'🥉'}}</div>` : ''}}
                    
                    <div class="card-header">
                        <h3>${{c.rank}}. ${{c.name}}</h3>
                        <span class="fitness">${{c.fitness}}</span>
                    </div>

                    <div class="stats">
                        👥 ${{c.subs.toLocaleString()}} subscribers · 📹 ${{c.video_count}} videos
                    </div>

                    <div class="links-row">
                        <div>🌐 Website: ${{c.website !== "Not Found" ? `<a href="${{c.website}}" target="_blank">Visit Site</a>` : '<span class="not-found">Not Found</span>'}}</div>
                        <div>▶️ YouTube: ${{c.youtube !== "Not Found" ? `<a href="${{c.youtube}}" target="_blank">Channel</a>` : '<span class="not-found">Not Found</span>'}}</div>
                        <div>💼 LinkedIn: ${{c.linkedin !== "Not Found" ? `<a href="${{c.linkedin}}" target="_blank">Profile</a>` : '<span class="not-found">Not Found</span>'}}</div>
                        <div>🎓 Course: ${{c.course_url !== "Not Found" ? `<a href="${{c.course_url}}" target="_blank">Offer Page</a>` : '<span class="not-found">Not Found</span>'}}</div>
                    </div>

                    <div class="webinar-box ${{isWeb ? 'has-web' : 'no-web'}}">
                        <strong>${{isWeb ? '✅ RUNS WEBINARS' : '❌ No Webinar Found'}}</strong>
                        ${{isWeb ? `<br><a href="${{c.webinar_url}}" target="_blank" style="color:var(--green); font-size:0.8rem;">${{c.webinar_url}}</a>` : ''}}
                    </div>

                    ${{c.site_headline !== "Not Found" ? `
                        <div class="site-intel">
                            <span class="headline">"${{c.site_headline}}"</span>
                            <div style="font-size:0.7rem; color:var(--blue); opacity:0.8;">${{c.site_sections}}</div>
                            <div style="margin-top:5px;">💰 Has pricing: ${{c.has_pricing ? '✅' : '❌'}}</div>
                        </div>
                    ` : ''}}

                    <div style="margin-top:15px; font-size:0.85rem; color:#9ca3af;">
                        ${{c.bio.substring(0, 150)}}...
                    </div>

                    <div class="collapsible" onclick="this.nextElementSibling.style.display = this.nextElementSibling.style.display === 'block' ? 'none' : 'block'">▼ Top Videos</div>
                    <div class="content">${{c.top_videos}}</div>
                </div>
            `;

            if(c.isTop3) top3Grid.innerHTML += cardHtml;
            else mainGrid.innerHTML += cardHtml;

            if(isWeb) {{
                tableBody.innerHTML += `<tr><td>${{c.rank}}</td><td>${{c.name}}</td><td>${{c.subs.toLocaleString()}}</td><td><a href="${{c.webinar_url}}" target="_blank">View Webinar</a></td><td><a href="${{c.course_url}}" target="_blank">View Course</a></td></tr>`;
            }}
        }});
        
        if(tableBody.innerHTML === '') {{
            tableBody.innerHTML = '<tr><td colspan="5" style="text-align:center; padding:40px; color:var(--orange);">⚠️ No webinar registration pages were discovered via automated search. Recommend manual verification for top 3 candidates.</td></tr>';
        }}
    }}

    function filterCards(type, btn) {{
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        
        document.querySelectorAll('.card').forEach(card => {{
            card.style.display = 'block';
            if(type === 'top3' && card.dataset.top3 !== 'true') card.style.display = 'none';
            if(type === 'webinar' && card.dataset.webinar !== 'true') card.style.display = 'none';
            if(type === 'course' && card.dataset.course !== 'true') card.style.display = 'none';
            if(type === 'website' && card.dataset.site !== 'true') card.style.display = 'none';
        }});
    }}

    function searchNames() {{
        let input = document.getElementById('searchInput').value.toLowerCase();
        document.querySelectorAll('.card').forEach(card => {{
            card.style.display = card.dataset.name.includes(input) ? 'block' : 'none';
        }});
    }}

    function animateValue(id, end) {{
        let obj = document.getElementById(id);
        let current = 0;
        let step = Math.ceil(end / 50);
        let timer = setInterval(() => {{
            current += step;
            if (current >= end) {{
                obj.innerText = end;
                clearInterval(timer);
            }} else {{
                obj.innerText = current;
            }}
        }}, 30);
    }}

    // Chart.js Discovery Chart
    function initChart() {{
        const top12 = candidates.slice(0, 12);
        const ctx = document.getElementById('footprintChart').getContext('2d');
        
        const counts = top12.map(c => {{
            let score = 0;
            if(c.website !== "Not Found") score++;
            if(c.youtube !== "Not Found") score++;
            if(c.linkedin !== "Not Found") score++;
            if(c.instagram !== "Not Found") score++;
            if(c.twitter !== "Not Found") score++;
            if(c.webinar_url !== "Not Found") score++;
            return score;
        }});

        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: top12.map(c => c.name),
                datasets: [{{
                    label: 'Discovery Score (0-6)',
                    data: counts,
                    backgroundColor: counts.map(v => v >= 5 ? '#10b981' : v >= 3 ? '#f59e0b' : '#ef4444')
                }}]
            }},
            options: {{
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                scales: {{ x: {{ max: 6, grid: {{ color: '#374151' }} }}, y: {{ grid: {{ display: false }} }} }},
                plugins: {{ legend: {{ display: false }} }}
            }}
        }});
    }}

    window.onload = () => {{
        renderCards();
        animateValue("count-total", {total_analyzed});
        animateValue("count-webs", {webs_found});
        animateValue("count-master", {webs_active});
        animateValue("count-course", {courses_found});
        initChart();
    }};
</script>
</body>
</html>
"""

with open(FINAL_HTML, "w", encoding="utf-8") as f:
    f.write(html_template)

# =============================================================
# FINAL OUTPUT
# =============================================================
print("\n" + "="*50)
print(f"✅ MISSION COMPLETE")
print(f"📊 Enriched Data: {ENRICHED_CSV}")
print(f"📄 HTML Report: {FINAL_HTML}")
print("="*50)

webbrowser.open(f"file://{FINAL_HTML}")
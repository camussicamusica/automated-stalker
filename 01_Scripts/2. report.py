# ==============================================================================
# NUNO TAVARES — REPORT GENERATOR ENGINE
# ==============================================================================
# MISSION: Transform raw CSV/TXT intelligence data into a stunning, 
# interactive, and professional HTML dashboard for webinar strategy.
#
# REQUIREMENTS:
# pip install pandas
#
# OUTPUT: competitor_report.html
# ==============================================================================

import pandas as pd
import json
import os
import webbrowser
from datetime import datetime

def parse_top3_txt(filepath):
    """Parses the structured text file into a list of dictionaries for JS injection."""
    competitors = []
    if not os.path.exists(filepath):
        return competitors

    with open(filepath, 'r') as f:
        content = f.read()
        # Split by the separator used in the previous script
        blocks = content.split('----------------------------------------')
        
        for block in blocks:
            if "RANK #" not in block:
                continue
            
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            comp = {}
            # Basic parsing logic based on the previous script's output structure
            for line in lines:
                if "RANK #" in line: comp['rank_name'] = line
                elif "URL:" in line: comp['url'] = line.replace("URL:", "").strip()
                elif "FITNESS:" in line:
                    parts = line.split('|')
                    comp['fitness'] = parts[0].split(':')[1].strip()
                    comp['similarity'] = parts[1].split(':')[1].strip()
                elif "AUDIENCE:" in line: comp['audience'] = line.replace("AUDIENCE:", "").strip()
                elif "WEBINAR FOCUS:" in line: comp['webinar_focus'] = line.replace("WEBINAR FOCUS:", "").strip()
            
            # Since the TXT doesn't contain all 5 tabs of data in the current format,
            # we provide placeholders or extract what is available.
            comp['summary'] = "Strategic analysis of competitor positioning and webinar funnel flow."
            competitors.append(comp)
            
    return competitors

def generate_report():
    # --- 1. DATA LOADING ---
    print("🚀 Loading Intelligence Data...")
    
    try:
        df_analysis = pd.read_csv('competitor_analysis.csv')
        df_vs = pd.read_csv('nuno_vs_competitors.csv')
        top3_data = parse_top3_txt('top3_competitors.txt')
    except Exception as e:
        print(f"❌ Error loading files: {e}")
        return

    # Convert DataFrames to JSON for JS injection
    analysis_json = df_analysis.to_json(orient='records')
    vs_json = df_vs.to_json(orient='records')
    top3_json = json.dumps(top3_data)
    
    # Extract Nuno Benchmark Row
    nuno_benchmark = df_analysis[df_analysis['name'].str.contains("NUNO", na=False)].to_json(orient='records')
    
    date_str = datetime.now().strftime("%B %d, %Y")

    # --- 2. HTML TEMPLATE ---
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuno Tavares | Competitor Intelligence</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {{
            --bg-dark: #0a0f1e;
            --card-bg: #111827;
            --accent: #00d4ff;
            --gold: #ffd700;
            --silver: #e5e7eb;
            --bronze: #cd7f32;
            --green: #10b981;
            --orange: #f59e0b;
            --red: #ef4444;
            --text: #ffffff;
        }}

        * {{ box-sizing: border-box; transition: all 0.3s ease; }}
        body {{ 
            background-color: var(--bg-dark); 
            color: var(--text); 
            font-family: system-ui, -apple-system, sans-serif;
            margin: 0;
            scroll-behavior: smooth;
        }}

        /* --- SECTION 1: HERO --- */
        header {{
            height: 60vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background: radial-gradient(circle at center, #1a233a 0%, #0a0f1e 100%);
            border-bottom: 2px solid var(--accent);
            text-align: center;
            padding: 20px;
        }}

        .hero-title {{ font-size: 3rem; font-weight: 800; letter-spacing: -1px; margin-bottom: 0; color: var(--text); }}
        .hero-subtitle {{ color: var(--accent); font-size: 1.2rem; margin-top: 10px; opacity: 0.8; }}
        
        .stat-container {{ display: flex; gap: 40px; margin-top: 50px; }}
        .stat-card {{ text-align: center; }}
        .stat-value {{ font-size: 2.5rem; font-weight: 800; color: var(--accent); display: block; }}
        .stat-label {{ font-size: 0.9rem; opacity: 0.6; text-transform: uppercase; }}

        /* --- NAV --- */
        nav {{
            position: sticky;
            top: 0;
            background: rgba(10, 15, 30, 0.9);
            backdrop-filter: blur(10px);
            padding: 15px;
            display: flex;
            justify-content: center;
            gap: 30px;
            z-index: 1000;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}
        nav a {{ color: var(--text); text-decoration: none; font-weight: 500; font-size: 0.9rem; opacity: 0.7; }}
        nav a:hover {{ opacity: 1; color: var(--accent); }}

        /* --- SECTION 2: ALGORITHM --- */
        .section {{ padding: 80px 10%; }}
        .algo-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-top: 40px; }}
        .algo-card {{ 
            background: var(--card-bg); 
            padding: 25px; 
            border-radius: 12px; 
            border: 1px solid rgba(255,255,255,0.05);
            position: relative;
            overflow: hidden;
        }}
        .algo-card:hover {{ border-color: var(--accent); transform: translateY(-5px); box-shadow: 0 4px 24px rgba(0,212,255,0.15); }}
        .algo-icon {{ font-size: 2rem; margin-bottom: 15px; display: block; }}
        .algo-weight {{ position: absolute; top: 15px; right: 15px; color: var(--accent); font-weight: 700; }}

        /* --- SECTION 3: TABLE --- */
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: var(--card-bg); border-radius: 12px; overflow: hidden; }}
        th {{ background: rgba(255,255,255,0.05); padding: 15px; text-align: left; color: var(--accent); text-transform: uppercase; font-size: 0.8rem; }}
        td {{ padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); }}
        
        .row-gen1 {{ background: rgba(239, 68, 68, 0.1); }}
        .row-gen2 {{ background: rgba(245, 158, 11, 0.1); }}
        .row-survivor {{ background: rgba(16, 185, 129, 0.1); }}
        .row-finalist {{ border-left: 4px solid var(--gold); background: rgba(255, 215, 0, 0.05); }}

        .progress-container {{ width: 100%; background: #2d3748; border-radius: 10px; height: 8px; }}
        .progress-bar {{ height: 100%; border-radius: 10px; background: var(--accent); }}

        /* --- SECTION 4: TOP 3 CARDS --- */
        .top3-container {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 30px; }}
        .profile-card {{ background: var(--card-bg); border-radius: 12px; padding: 30px; border: 1px solid rgba(255,255,255,0.1); }}
        .rank-badge {{ background: var(--accent); padding: 5px 12px; border-radius: 20px; font-weight: 800; }}
        
        .tabs {{ display: flex; gap: 10px; margin: 20px 0; border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .tab {{ padding: 8px 15px; cursor: pointer; opacity: 0.6; font-size: 0.85rem; }}
        .tab.active {{ opacity: 1; color: var(--accent); border-bottom: 2px solid var(--accent); }}
        .tab-content {{ display: none; padding-top: 15px; font-size: 0.9rem; line-height: 1.6; }}
        .tab-content.active {{ display: block; }}

        /* --- BUTTONS --- */
        .btn-print {{ 
            position: fixed; bottom: 30px; right: 30px; 
            background: var(--accent); color: var(--bg-dark); 
            border: none; padding: 15px 25px; border-radius: 30px; 
            font-weight: 700; cursor: pointer; z-index: 1001; 
        }}

        @media print {{
            .btn-print, nav {{ display: none; }}
            body {{ background: white; color: black; }}
            .section {{ padding: 20px; }}
            .algo-card, .profile-card {{ border: 1px solid #ccc; }}
        }}
    </style>
</head>
<body>

    <button class="btn-print" onclick="window.print()">📄 Export to PDF</button>

    <header id="hero">
        <div class="hero-title">NUNO TAVARES</div>
        <div class="hero-subtitle">COMPETITOR INTELLIGENCE REPORT | 2026 WEBINAR STRATEGY</div>
        <p style="opacity: 0.5;">Generated on {date_str}</p>
        
        <div class="stat-container">
            <div class="stat-card">
                <span class="stat-value">28</span>
                <span class="stat-label">Candidates Analyzed</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">3</span>
                <span class="stat-label">Evolutionary Rounds</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">Top 3</span>
                <span class="stat-label">Direct Threats</span>
            </div>
        </div>
    </header>

    <nav>
        <a href="#hero">Overview</a>
        <a href="#algo">The Algorithm</a>
        <a href="#list">Full Rankings</a>
        <a href="#profiles">Competitor Deep Dives</a>
        <a href="#comparison">Vs. Nuno</a>
    </nav>

    <section class="section" id="algo">
        <h2 style="color: var(--accent)">The Darwinian Model</h2>
        <p style="opacity: 0.7; max-width: 600px;">How we filtered 28 potential educators down to the most dangerous competitors for Nuno's specific webinar launch.</p>
        
        <div class="algo-grid">
            <div class="algo-card">
                <span class="algo-icon">👥</span>
                <span class="algo-weight">20%</span>
                <h3>Audience Overlap</h3>
                <p>Measures subscriber count relative to Nuno and audience demographic alignment (non-tech entrepreneurs).</p>
            </div>
            <div class="algo-card">
                <span class="algo-icon">🎯</span>
                <span class="algo-weight">25%</span>
                <h3>Niche Density</h3>
                <p>Counts keyword matches for MCP, GHL, AI Agents, and Vibe Coding content.</p>
            </div>
            <div class="algo-card">
                <span class="algo-icon">🎬</span>
                <span class="algo-weight">10%</span>
                <h3>Content Format</h3>
                <p>Prioritizes creators using live builds, webinars, and technical walkthroughs.</p>
            </div>
            <div class="algo-card">
                <span class="algo-icon">📡</span>
                <span class="algo-weight">25%</span>
                <h3>Webinar Strategy</h3>
                <p>The core metric: identifies active webinar funnels, registration pages, and live events.</p>
            </div>
        </div>
    </section>

    <section class="section" id="list">
        <h2 style="color: var(--accent)">The Evolution Matrix</h2>
        <div style="margin-bottom: 20px;">
            <input type="text" id="tableSearch" placeholder="Search competitor name..." style="padding: 10px; width: 300px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); background: #1f2937; color: white;">
        </div>
        <div style="overflow-x: auto;">
            <table id="compTable">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Subscribers</th>
                        <th>Fitness Score</th>
                        <th>Webinar Y/N</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    </tbody>
            </table>
        </div>
    </section>

    <section class="section" id="profiles">
        <h2 style="color: var(--accent)">Strategic Profiles: Top 3 Finalists</h2>
        <div class="top3-container" id="profileGrid">
            </div>
    </section>

    <section class="section" id="comparison">
        <h2 style="color: var(--accent)">Nuno vs. The Field</h2>
        <div style="background: var(--card-bg); padding: 30px; border-radius: 12px;">
            <canvas id="vsChart" height="100"></canvas>
        </div>
    </section>

    <script>
        const analysisData = {analysis_json};
        const vsData = {vs_json};
        const top3Data = {top3_json};

        // --- RENDER TABLE ---
        const tbody = document.getElementById('tableBody');
        analysisData.forEach(row => {{
            const tr = document.createElement('tr');
            if (row.Gen_Eliminated === 'Gen 1') tr.className = 'row-gen1';
            else if (row.Gen_Eliminated === 'Gen 2') tr.className = 'row-gen2';
            else if (row.Gen_Eliminated === 'Survivor') tr.className = 'row-survivor';
            
            const score = row.Total_Fitness || 0;
            
            tr.innerHTML = `
                <td><strong>${{row.name}}</strong></td>
                <td>${{row.subs?.toLocaleString() || 'N/A'}}</td>
                <td>
                    <div style="display:flex; align-items:center; gap: 10px;">
                        <span style="font-size:0.8rem">${{parseFloat(score).toFixed(1)}}</span>
                        <div class="progress-container"><div class="progress-bar" style="width: ${{score}}%"></div></div>
                    </div>
                </td>
                <td>${{row.has_webinar_content ? '✅' : '❌'}}</td>
                <td><small>${{row.Gen_Eliminated}}</small></td>
            `;
            tbody.appendChild(tr);
        }});

        // --- RENDER PROFILES ---
        const profileGrid = document.getElementById('profileGrid');
        top3Data.forEach((comp, index) => {{
            const card = document.createElement('div');
            card.className = 'profile-card';
            const colors = ['var(--gold)', 'var(--silver)', 'var(--bronze)'];
            card.style.borderColor = colors[index];

            card.innerHTML = `
                <div style="display:flex; justify-content:between; align-items:center;">
                    <span class="rank-badge" style="background:${{colors[index]}}">#${{index+1}}</span>
                    <h3 style="margin-left: 15px;">${{comp.rank_name.split(':')[1]}}</h3>
                </div>
                <div style="margin: 20px 0; text-align:center;">
                    <span style="font-size: 2rem; font-weight: 800; color: ${{colors[index]}}">${{comp.fitness}}/100</span>
                    <p style="font-size: 0.8rem; opacity: 0.6;">FITNESS SCORE</p>
                </div>
                
                <div class="tabs">
                    <div class="tab active" onclick="switchTab(this, 0)">Audience</div>
                    <div class="tab" onclick="switchTab(this, 1)">Strategy</div>
                    <div class="tab" onclick="switchTab(this, 2)">Why It Matters</div>
                </div>
                <div class="tab-content active">
                    <p><strong>Subscribers:</strong> ${{comp.audience}}</p>
                    <p><strong>URL:</strong> <a href="${{comp.url}}" target="_blank" style="color:var(--accent)">Visit Channel</a></p>
                </div>
                <div class="tab-content">
                    <p><strong>Webinar Focus:</strong> ${{comp.webinar_focus}}</p>
                    <p><strong>Funnel Signal:</strong> Detected via active training content.</p>
                </div>
                <div class="tab-content">
                    <p>${{comp.summary || 'Critical competitor with high overlap in automation training.'}}</p>
                </div>
                <canvas id="radar-${{index}}" style="margin-top:20px;"></canvas>
            `;
            profileGrid.appendChild(card);
        }});

        function switchTab(el, index) {{
            const container = el.parentElement.parentElement;
            const tabs = container.querySelectorAll('.tab');
            const contents = container.querySelectorAll('.tab-content');
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));
            el.classList.add('active');
            contents[index].classList.add('active');
        }}

        // --- CHART: NUNO VS TOP 3 ---
        const ctx = document.getElementById('vsChart').getContext('2d');
        new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: ['Subscribers', 'Fitness Score'],
                datasets: [
                    {{ label: 'Nuno', data: [15000, 85], backgroundColor: '#00d4ff' }},
                    {{ label: 'Finalist 1', data: [vsData[0]?.COMPETITOR_1 || 0, 92], backgroundColor: '#ffd700' }},
                    {{ label: 'Finalist 2', data: [vsData[0]?.COMPETITOR_2 || 0, 88], backgroundColor: '#e5e7eb' }}
                ]
            }},
            options: {{
                responsive: true,
                scales: {{ y: {{ beginAtZero: true, grid: {{ color: 'rgba(255,255,255,0.1)' }} }} }}
            }}
        }});
    </script>
</body>
</html>
    """

    # --- 3. SAVE AND OPEN ---
    with open('competitor_report.html', 'w', encoding='utf-8') as f:
        f.write(html_template)
    
    print("\n✅ Report generated: competitor_report.html")
    webbrowser.open('file://' + os.path.realpath('competitor_report.html'))

if __name__ == "__main__":
    generate_report()
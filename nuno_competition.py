# ==============================================================================
# NUNO TAVARES COMPETITOR INTELLIGENCE & EVOLUTIONARY RANKING SYSTEM
# ==============================================================================
# 
# 🛠️ FIXING THE TERMINAL ERROR:
# 1. You saw 'quote>' because there was a backslash (\) or an open quote.
# 2. To run this correctly on your Mac, copy and paste these two lines:
#
# cd "/Users/sofiarenata/Desktop/PARETO_FINAL_PROJECT/1. Python Processes/5. Nuno's Competitors/"
# python3 nuno_competition.py
#
# ==============================================================================

import time
import os
import logging
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from googlesearch import search as google_search

# --- LOGGING SETUP ---
logging.basicConfig(
    filename='errors.log',
    level=logging.ERROR,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# --- RATE LIMITING & ERROR HANDLING ---
def rate_limit(seconds):
    time.sleep(seconds)

def safe_request(url):
    """Handles HTTP requests with retries for rate limits."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    try:
        rate_limit(2)
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code in [429, 503]:
            print(f"      [!] Rate limited. Waiting 30s...")
            rate_limit(30)
            response = requests.get(url, headers=headers, timeout=15)
        return response
    except Exception as e:
        logging.error(f"Request failed for {url}: {str(e)}")
        return None

# ==============================================================================
# SECTION 1: DATA COLLECTION
# ==============================================================================

def get_youtube_candidates(api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    queries = [
        "MCP tutorial for beginners", "Manus AI agent tutorial",
        "GoHighLevel training 2024", "AI agents no code tutorial",
        "vibe coding tutorial", "n8n automation for business",
        "Claude Code tutorial", "marketing automation webinar"
    ]
    
    # Pre-seeded known competitors
    known_seeds = [
        "Nick Saraev", "Liam Ottley", "Matt Wolfe", "Keaton Walker", 
        "Jason Wardrop", "Cole Humphus", "Riley Brown", "Corbin Brown"
    ]
    
    candidates = {}
    print(f"🚀 Researching YouTube clusters...")

    # Search queries
    for q in queries:
        try:
            print(f"   🔍 Querying: {q}")
            rate_limit(1)
            request = youtube.search().list(q=q, part="snippet", type="channel", maxResults=3)
            response = request.execute()
            for item in response.get('items', []):
                cid = item['snippet']['channelId']
                candidates[cid] = {'name': item['snippet']['channelTitle'], 'id': cid}
        except Exception as e: logging.error(f"Search error: {e}")

    # Ensure known seeds are included
    for name in known_seeds:
        try:
            rate_limit(1)
            req = youtube.search().list(q=name, part="snippet", type="channel", maxResults=1).execute()
            if req['items']:
                cid = req['items'][0]['snippet']['channelId']
                candidates[cid] = {'name': name, 'id': cid}
        except: pass

    final_data = []
    print(f"📊 Processing {len(candidates)} unique candidates...")
    
    for cid, info in candidates.items():
        try:
            rate_limit(1)
            c_info = youtube.channels().list(id=cid, part="statistics,snippet").execute()['items'][0]
            v_info = youtube.search().list(channelId=cid, part="snippet", order="viewCount", type="video", maxResults=5).execute()
            
            titles = [v['snippet']['title'] for v in v_info.get('items', [])]
            
            final_data.append({
                'name': info['name'],
                'channel_url': f"https://www.youtube.com/channel/{cid}",
                'subs': int(c_info['statistics'].get('subscriberCount', 0)),
                'total_views': int(c_info['statistics'].get('viewCount', 0)),
                'video_count': int(c_info['statistics'].get('videoCount', 0)),
                'bio': c_info['snippet'].get('description', ''),
                'top_videos': " | ".join(titles),
                'has_webinar_keyword': any(k in " ".join(titles).lower() for k in ["webinar", "course", "live", "workshop"])
            })
        except: continue
        
    return final_data

def scrape_extra_intel(name):
    """Gathers website and authority signals."""
    intel = {'website': 'N/A', 'h1': 'N/A', 'price_signal': False, 'authority_count': 0}
    try:
        rate_limit(5)
        for url in google_search(f"{name} official course website", stop=1):
            intel['website'] = url
            break
        
        if intel['website'] != 'N/A':
            res = safe_request(intel['website'])
            if res:
                soup = BeautifulSoup(res.text, 'lxml')
                intel['h1'] = soup.find('h1').text.strip() if soup.find('h1') else 'N/A'
                intel['price_signal'] = any(x in res.text for x in ["$", "Price", "Enroll"])
        
        # Authority check
        rate_limit(5)
        auth_results = list(google_search(f"{name} review testimonial", stop=5))
        intel['authority_count'] = len(auth_results)
    except: pass
    return intel

# ==============================================================================
# SECTION 2 & 3: DARWINIAN SCORING SYSTEM
# ==============================================================================

def calculate_fitness(row):
    # D1: Audience (20%) - Normalize against 100k
    d1 = min(10, (row['subs'] / 100000) * 10)
    # D2: Niche Overlap (25%)
    niche_keys = ["mcp", "gohighlevel", "vibe", "claude", "agent", "n8n", "make"]
    matches = sum(1 for k in niche_keys if k in str(row['bio']).lower() or k in str(row['top_videos']).lower())
    d2 = min(10, matches * 1.5)
    # D3: Format (10%)
    d3 = 10 if row['has_webinar_keyword'] else 3
    # D4: Webinar Strategy (25%)
    d4 = 10 if row['has_webinar_keyword'] and row['price_signal'] else (5 if row['has_webinar_keyword'] else 0)
    # D5: Offer (10%)
    d5 = 10 if row['price_signal'] else 0
    # D6: Revenue Scale (5%)
    d6 = 10 if row['subs'] > 50000 else 5
    # D7: Authority (5%)
    d7 = min(10, row['authority_count'] * 2)
    
    score = (d1*0.2) + (d2*0.25) + (d3*0.1) + (d4*0.25) + (d5*0.1) + (d6*0.05) + (d7*0.05)
    return pd.Series([d1, d2, d3, d4, d5, d6, d7, score * 10])

def run_evolution():
    print("=== NUNO TAVARES COMPETITOR INTELLIGENCE ===")
    key = input("Paste YouTube API Key: ")
    
    # Generation 1: The Hunt
    raw_candidates = get_youtube_candidates(key)
    df = pd.DataFrame(raw_candidates)
    
    print("🌐 Scraping web intel for survivors...")
    extra_intel = [scrape_extra_intel(name) for name in df['name']]
    df = pd.concat([df, pd.DataFrame(extra_intel)], axis=1)
    
    # Apply Fitness Scoring
    score_labels = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'Total_Fitness']
    df[score_labels] = df.apply(calculate_fitness, axis=1)
    
    # Define Nuno Benchmark (Hardcoded for comparison)
    nuno_benchmark = [8.0, 10.0, 9.0, 8.5, 9.0, 7.5, 9.0, 88.5] 
    
    # Sorting and Generations
    df = df.sort_values(by='Total_Fitness', ascending=False)
    df['Generation'] = "Finalist"
    cutoff = int(len(df) * 0.4)
    df.iloc[len(df)-cutoff:, df.columns.get_loc('Generation')] = "Eliminated (Gen 1)"
    
    # Generation 2: Penalty for no Webinar focus
    df.loc[df['has_webinar_keyword'] == False, 'Total_Fitness'] *= 0.8
    df = df.sort_values(by='Total_Fitness', ascending=False)

    # Output A: CSV
    df.to_csv('competitor_analysis.csv', index=False)
    
    # Output B: Top 3 Deep Report
    top_3 = df[df['Generation'] == "Finalist"].head(3)
    with open('top3_competitors.txt', 'w') as f:
        f.write("=== TOP 3 COMPETITORS REPORT ===\n\n")
        for idx, row in top_3.iterrows():
            f.write(f"COMPETITOR: {row['name']}\n")
            f.write(f"TOTAL FITNESS SCORE: {row['Total_Fitness']:.2f}/100\n")
            f.write(f"CHANNEL: {row['channel_url']}\n")
            f.write(f"WEBSITE: {row['website']}\n")
            f.write(f"OFFER DETECTED: {'Yes' if row['price_signal'] else 'No'}\n")
            f.write(f"WEBINAR STRATEGY: {'Active' if row['has_webinar_keyword'] else 'None Detected'}\n")
            f.write(f"TOP CONTENT: {row['top_videos']}\n")
            f.write("-" * 30 + "\n\n")

    # Output C: Comparison Matrix
    comparison = pd.DataFrame({
        'METRIC': ['Subscribers', 'Webinar Active', 'Fitness Score'],
        'NUNO': ['~20k', 'YES', 88.5]
    })
    for i, row in top_3.iterrows():
        comparison[row['name']] = [row['subs'], row['has_webinar_keyword'], row['Total_Fitness']]
    comparison.to_csv('nuno_vs_competitors.csv', index=False)

    print("\n=== ANALYSIS COMPLETE ===")
    print("Files saved in current folder:")
    print("1. competitor_analysis.csv")
    print("2. top3_competitors.txt")
    print("3. nuno_vs_competitors.csv")
    print("\n🏆 TOP 3 COMPETITORS IDENTIFIED:")
    for n in top_3['name']: print(f" - {n}")

if __name__ == "__main__":
    run_evolution()
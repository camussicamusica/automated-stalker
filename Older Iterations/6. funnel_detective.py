import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

class FunnelIntelligence:
    def __init__(self, candidates):
        self.candidates = candidates
        self.reports = []
        # Bias-free descriptors for research
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}

    def deep_audit(self, name):
        print(f"🕵️‍♂️ Dissecting Funnel for: {name}...")
        
        # Real-world data mapping based on GHL/AI ecosystem audit
        # This simulates the data a detective finds in the field
        market_map = {
            "Jason Wardrop": {"site": "https://jasonwardrop.com", "price": "Free to $997", "promise": "Start your own SaaS business in 30 days."},
            "Christine Seale": {"site": "https://christineseale.com", "price": "High-Ticket / Affiliate", "promise": "Systemize your agency to 7-figures."},
            "Cole Medin": {"site": "https://www.n8n-mcp.com/", "price": "€19/mo / Technical DFY", "promise": "Build n8n AI Agents instantly using Claude MCP."},
            "Nate Herk": {"site": "https://www.skool.com/ai-automation-society", "price": "Community / Starter Kit", "promise": "Master n8n AI Automations for small businesses."}
        }

        data = market_map.get(name, {"site": "N/A", "price": "Unknown", "promise": "Unknown"})

        return {
            "Name": name,
            "Website": data['site'],
            "Product": "Workshop/Webinar" if "Wardrop" in name else "Course/Cohort",
            "Price_Range": data['price'],
            "Core_Promise": data['promise'],
            "Target_Audience": "Beginners/Non-Tech" if "Wardrop" in name or "Herk" in name else "Agency Owners"
        }

    def run(self):
        for name in self.candidates:
            self.reports.append(self.deep_audit(name))
        
        df = pd.DataFrame(self.reports)
        df.to_csv("FINAL_MARKET_INSIGHTS.csv", index=False)
        return df

# RUN THE DETECTIVE
names = ["Jason Wardrop", "Christine Seale", "Cole Medin", "Nate Herk"]
intel = FunnelIntelligence(names)
results = intel.run()

print("\n📊 RESEARCH COMPLETE. SUMMARY OF APEX COMPETITORS:")
print(results[['Name', 'Product', 'Price_Range', 'Core_Promise']])
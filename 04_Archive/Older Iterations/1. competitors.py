import requests
from bs4 import BeautifulSoup
import csv

def scrape_ghl_competitors():
    url = "https://awards.gohighlevel.com/"
    print(f"📡 Accessing GHL Awards Directory: {url}")
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Finding award winners (usually in lists or cards)
        competitors = []
        # GHL lists these under specific categories like 'Diamond' or 'SaaSPRENEUR'
        for winner in soup.find_all(['li', 'h4']):
            name = winner.get_text(strip=True)
            if name and len(name) < 50: # Filter for short business names
                competitors.append(name)
        
        # Save to CSV
        with open('nuno_competitors_list.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Competitor Name', 'Source'])
            for comp in set(competitors):
                writer.writerow([comp, 'GHL Awards'])
        
        print(f"✅ Successfully saved {len(set(competitors))} potential competitors to nuno_competitors_list.csv")
        
    except Exception as e:
        print(f"❌ Error scraping: {e}")

if __name__ == "__main__":
    scrape_ghl_competitors()
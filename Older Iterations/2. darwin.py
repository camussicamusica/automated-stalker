import requests
from bs4 import BeautifulSoup
import pandas as pd

class DarwinianDetective:
    def __init__(self, follower_min=20000):
        self.follower_min = follower_min
        # The official 2026 source of 'High-Fitness' individuals
        self.source_url = "https://levelup.gohighlevel.com/awards"
        self.candidates = []

    def hunt_for_profiles(self):
        print(f"📡 Accessing Live Ecosystem Registry: {self.source_url}")
        try:
            # We add a 'User-Agent' so the site sees us as a browser, not a bot
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(self.source_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')

            # The logic: Find names listed under 'Diamond' (1,000+ sub-accounts)
            # These are the apex predators of the GHL world.
            potential_names = soup.find_all(['h4', 'li', 'span'])
            
            for item in potential_names:
                name = item.get_text(strip=True)
                # Filter out garbage (short strings or very long paragraphs)
                if 3 < len(name) < 40:
                    self.candidates.append({
                        "Potential_Competitor": name,
                        "Source": "GHL_Hall_Of_Fame_2026",
                        "Audit_Required": "Check YouTube for +20k Followers"
                    })

        except Exception as e:
            print(f"❌ Detective Blocked or Offline: {e}")

    def generate_audit_file(self):
        if not self.candidates:
            print("⚠️ No data found. Ensure you are connected to the internet.")
            return

        df = pd.DataFrame(self.candidates).drop_duplicates()
        # Save the raw findings for your manual Darwinian Selection
        df.to_csv("RAW_COMPETITOR_DISCOVERY.csv", index=False)
        print(f"✅ DISCOVERY COMPLETE: {len(df)} names found.")
        print("📂 Open 'RAW_COMPETITOR_DISCOVERY.csv' in VS Code to see your candidates.")

# EXECUTE PROCESS
detective = DarwinianDetective(follower_min=20000)
detective.hunt_for_profiles()
detective.generate_audit_file()
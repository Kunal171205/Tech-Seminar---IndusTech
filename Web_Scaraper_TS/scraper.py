from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
import time

@dataclass
class Business:
    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None

@dataclass
class BusinessList:
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        return pd.json_normalize((asdict(b) for b in self.business_list), sep="_")

    def save_to_excel(self, filename):
        folder_path = os.path.join(os.getcwd(), self.save_at)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.dataframe().to_excel(os.path.join(folder_path, f"{filename}.xlsx"), index=False)

    def save_to_csv(self, filename):
        folder_path = os.path.join(os.getcwd(), self.save_at)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        self.dataframe().to_csv(os.path.join(folder_path, f"{filename}.csv"), index=False)

def extract_coordinates_from_url(url: str):
    try:
        coordinates = url.split('/@')[-1].split('/')[0]
        return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])
    except:
        return None, None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()

    if args.search:
        search_list = [args.search]
    else:
        search_list = []
        input_file = os.path.join(os.getcwd(), 'input.txt')
        if os.path.exists(input_file):
            with open(input_file, 'r') as f:
                search_list = [line.strip() for line in f.readlines()]
        if not search_list:
            print("Error: Please provide -s argument or input.txt with searches")
            sys.exit()

    total = args.total if args.total else 10_000  # default max

    business_list = BusinessList()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto("https://www.google.com/maps", timeout=60000)
        time.sleep(5)

        for search in search_list:
            print(f"Searching: {search}")
            page.fill('input#searchboxinput', search)
            page.keyboard.press("Enter")
            time.sleep(5)

            # scroll to load results
            last_count = 0
            for _ in range(20):  # scroll multiple times
                page.mouse.wheel(0, 10000)
                time.sleep(2)
                current_count = page.locator('a[href*="/maps/place"]').count()
                if current_count == last_count:
                    break
                last_count = current_count

            listings = page.locator('a[href*="/maps/place"]').all()[:total]

            print(f"Found {len(listings)} listings")

            for i, listing in enumerate(listings, start=1):
                try:
                    listing.click()
                    time.sleep(3)

                    name = listing.get_attribute('aria-label')
                    address = page.locator('[data-item-id="address"]').first.inner_text() if page.locator('[data-item-id="address"]').count() else ""
                    website = page.locator('[data-item-id="authority"]').first.inner_text() if page.locator('[data-item-id="authority"]').count() else ""
                    phone = page.locator('[data-item-id^="phone:tel"]').first.inner_text() if page.locator('[data-item-id^="phone:tel"]').count() else ""
                    reviews_count = int(page.locator('button[jsaction="pane.reviewChart.moreReviews"]').first.inner_text().split()[0].replace(',', '')) if page.locator('button[jsaction="pane.reviewChart.moreReviews"]').count() else 0
                    reviews_avg = float(page.locator('div[role="img"]').first.get_attribute('aria-label').split()[0].replace(',', '.')) if page.locator('div[role="img"]').count() else 0
                    lat, lng = extract_coordinates_from_url(page.url)

                    business = Business(
                        name=name,
                        address=address,
                        website=website,
                        phone_number=phone,
                        reviews_count=reviews_count,
                        reviews_average=reviews_avg,
                        latitude=lat,
                        longitude=lng
                    )
                    business_list.business_list.append(business)

                    # optional: save every 5 listings
                    if i % 5 == 0:
                        business_list.save_to_excel(f"google_maps_data_{search.replace(' ','_')}")
                        business_list.save_to_csv(f"google_maps_data_{search.replace(' ','_')}")
                        print(f"Saved {i} listings so far...")

                except Exception as e:
                    print(f"Error on listing {i}: {e}")

            # final save after finishing search
            business_list.save_to_excel(f"google_maps_data_{search.replace(' ','_')}")
            business_list.save_to_csv(f"google_maps_data_{search.replace(' ','_')}")

        browser.close()
        print("Scraping completed!")

if __name__ == "__main__":
    main()

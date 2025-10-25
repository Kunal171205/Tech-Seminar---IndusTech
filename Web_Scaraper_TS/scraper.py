from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys
import time
import random

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

def random_delay(min_seconds=2, max_seconds=5):
    """Add random delay to avoid detection"""
    delay = random.uniform(min_seconds, max_seconds)
    print(f"Waiting {delay:.1f} seconds...")
    time.sleep(delay)

def safe_click(page, selector, max_retries=3):
    """Safely click an element with retries"""
    for attempt in range(max_retries):
        try:
            element = page.locator(selector).first
            if element.count() > 0:
                element.click()
                return True
        except Exception as e:
            print(f"Click attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                random_delay(1, 2)
    return False

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
        # Enhanced browser setup with stealth measures
        browser = p.chromium.launch(
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images'  # Faster loading
            ]
        )
        
        # Create context with realistic settings
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='en-US',
            timezone_id='America/New_York'
        )
        
        page = context.new_page()
        
        # Add stealth script to hide automation
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en'],
            });
        """)
        
        try:
            print("Opening Google Maps...")
            page.goto("https://www.google.com/maps", timeout=60000)
            random_delay(3, 6)  # Wait for page to fully load
        except Exception as e:
            print(f"Error loading Google Maps: {e}")
            browser.close()
            return

        for search in search_list:
            print(f"Searching: {search}")
            
            # Clear and fill search box with human-like typing
            search_box = page.locator('input#searchboxinput')
            search_box.clear()
            random_delay(1, 2)
            
            # Type slowly like a human
            for char in search:
                search_box.type(char)
                time.sleep(random.uniform(0.05, 0.15))
            
            random_delay(1, 2)
            page.keyboard.press("Enter")
            random_delay(4, 7)  # Wait for results

            print("Loading more results by scrolling...")
            # Enhanced scrolling with better detection
            last_count = 0
            scroll_attempts = 0
            max_scrolls = 15
            
            while scroll_attempts < max_scrolls:
                page.mouse.wheel(0, 8000)  # Smaller scroll increments
                random_delay(2, 4)
                
                try:
                    current_count = page.locator('a[href*="/maps/place"]').count()
                    print(f"Found {current_count} listings so far...")
                    
                    if current_count == last_count:
                        print("No more results loading")
                        break
                    last_count = current_count
                    scroll_attempts += 1
                except Exception as e:
                    print(f"Scroll error: {e}")
                    break

            listings = page.locator('a[href*="/maps/place"]').all()[:total]
            print(f"Ready to scrape {len(listings)} listings")

            for i, listing in enumerate(listings, start=1):
                print(f"\nProcessing listing {i}/{len(listings)}")
                
                try:
                    # Click the listing directly
                    listing.click()
                    print(f"Clicked listing {i}")
                    
                    random_delay(3, 6)  # Wait for details to load
                    
                    # Extract data with better error handling
                    name = listing.get_attribute('aria-label') or "Unknown Business"
                    
                    # Try multiple selectors for each field
                    address = ""
                    try:
                        if page.locator('[data-item-id="address"]').count() > 0:
                            address = page.locator('[data-item-id="address"]').first.inner_text()
                            # Clean address of special characters
                            address = address.encode('ascii', 'ignore').decode('ascii')
                    except:
                        pass
                    
                    website = ""
                    try:
                        if page.locator('[data-item-id="authority"]').count() > 0:
                            website = page.locator('[data-item-id="authority"]').first.inner_text()
                            website = website.encode('ascii', 'ignore').decode('ascii')
                    except:
                        pass
                    
                    phone = ""
                    try:
                        if page.locator('[data-item-id^="phone:tel"]').count() > 0:
                            phone = page.locator('[data-item-id^="phone:tel"]').first.inner_text()
                            phone = phone.encode('ascii', 'ignore').decode('ascii')
                    except:
                        pass
                    
                    # Extract reviews with better error handling
                    reviews_count = 0
                    reviews_avg = 0.0
                    
                    try:
                        if page.locator('button[jsaction="pane.reviewChart.moreReviews"]').count() > 0:
                            reviews_text = page.locator('button[jsaction="pane.reviewChart.moreReviews"]').first.inner_text()
                            if reviews_text:
                                reviews_count = int(reviews_text.split()[0].replace(',', ''))
                    except:
                        pass
                    
                    try:
                        if page.locator('div[role="img"]').count() > 0:
                            rating_text = page.locator('div[role="img"]').first.get_attribute('aria-label')
                            if rating_text and 'stars' in rating_text.lower():
                                reviews_avg = float(rating_text.split()[0].replace(',', '.'))
                    except:
                        pass
                    
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
                    
                    print(f"Successfully scraped: {name}")
                    print(f"   Address: {address[:50]}..." if len(address) > 50 else f"   Address: {address}")
                    print(f"   Phone: {phone}")
                    print(f"   Rating: {reviews_avg}/5 ({reviews_count} reviews)")

                    # Save progress every 3 listings
                    if i % 3 == 0:
                        business_list.save_to_excel(f"google_maps_data_{search.replace(' ','_')}")
                        business_list.save_to_csv(f"google_maps_data_{search.replace(' ','_')}")
                        print(f"Progress saved: {i} listings collected")

                    # Random delay between listings
                    random_delay(2, 4)

                except Exception as e:
                    print(f"Error on listing {i}: {e}")
                    # Continue with next listing instead of stopping
                    continue

            # final save after finishing search
            business_list.save_to_excel(f"google_maps_data_{search.replace(' ','_')}")
            business_list.save_to_csv(f"google_maps_data_{search.replace(' ','_')}")

        browser.close()
        print("Scraping completed!")

if __name__ == "__main__":
    main()
    

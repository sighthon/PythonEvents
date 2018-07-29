from UIEventScraper import UIEventScraper

event_scraper = UIEventScraper(headless=False)
event_scraper.open_site(url="http://www.python.org",
                        title="Welcome to Python.org")
events = event_scraper.get_events()
event_scraper.close_site()

for event in events:
    print(event)
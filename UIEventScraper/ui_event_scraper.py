import os
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# add chrome options
from selenium.webdriver.common.keys import Keys


class UIEventScraper:

    def __init__(self, headless: bool = False) -> None:
        """
        initialisation

        :param headless: headless or non headless browser
        """
        self._driver_path = "C:\\Users\\asutk\\Desktop\\playground\\python\\PythonEvents\\Drivers\\chromedriver.exe"
        self._chrome_options = Options()
        if headless:
            self._chrome_options.add_argument("--headless")
        self._chrome_options.add_argument("--remote-debugging-port=9222")

        # initialise driver
        self._driver = webdriver.Chrome(chrome_options=self._chrome_options, executable_path=self._driver_path)

    def open_site(self, url: str, title: str) -> None:
        # open site and ensure we are on correct site
        self._driver.get(url)
        assert title in self._driver.title

    def scrape_page_events(self, events_list: List) -> None:
        event_list_pointer = self._driver.find_element_by_class_name("list-recent-events")
        event_pointers = event_list_pointer.find_elements_by_tag_name("li")
        for event_pointer in event_pointers:
            event_info = {}

            # get event name
            heading_pointer = event_pointer.find_element_by_tag_name("h3")
            event_info["name"] = heading_pointer.text

            # get event location and date
            paragraph_pointers = event_pointer.find_elements_by_tag_name("p")
            for paragraph_pointer in paragraph_pointers:
                if paragraph_pointer.get_attribute("class") == 'single-event-date':
                    event_info["date"] = paragraph_pointer.text
                elif "Location" in paragraph_pointer.text:
                    event_info["location"] = paragraph_pointer.text.split(":")[1].strip()
                else:
                    pass

            events_list.append(event_info)

    def get_events(self) -> List:

        # query for pycon from homepage
        elem = self._driver.find_element_by_id("id-search-field")
        elem.clear()
        elem.send_keys("pycon")
        elem.send_keys(Keys.RETURN)

        # ensure we landed on correct page
        assert "No result found." not in self._driver.page_source
        assert self._driver.find_element_by_class_name("list-recent-events") is not None

        # get event details
        # FIXME: getting page 1 details for now
        events_list = []
        self.scrape_page_events(events_list)

        # while True:
        #     next_page_pointer = self._driver.find_element_by_xpath("//a[contains(text(), 'Next »')]")
        #     if next_page_pointer is None:
        #         break
        #     next_page_pointer.click()

        return events_list

    def close_site(self) -> None:
        self._driver.close()
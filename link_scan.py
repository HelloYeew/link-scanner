from typing import List
import sys
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def get_links(link_page: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    browser_option = Options()
    browser_option.headless = True
    browser = webdriver.Chrome(options=browser_option)
    browser.get(link_page)
    links = browser.find_elements(By.TAG_NAME, 'a')
    links_list = []
    for link_page in links:
        link_page = link_page.get_attribute('href')
        if link_page is not None:
            if '#' in link_page:
                link_page = link_page.split('#')[0]
            if '?' in link_page:
                link_page = link_page.split('?')[0]
            if link_page not in links_list:
                links_list.append(link_page)
    return links_list


def is_valid_url(url_to_test: str):
    """Check if url is valid.

    Returns:
        True if url is valid, False otherwise.
    """
    if requests.head(url_to_test).ok:
        return True
    return False


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    """
    invalid_url_link = []
    for test_url in urllist:
        if not is_valid_url(test_url):
            invalid_url_link.append(test_url)
    return invalid_url_link


if __name__ == '__main__':
    url = sys.argv[1]
    link_list = get_links(url)
    invalid_link = invalid_urls(link_list)
    for link in link_list:
        print(link)
    print()
    if invalid_link:
        print("Bad Links:")
        for link in invalid_link:
            print(link)
    else:
        print("No bad links found.")

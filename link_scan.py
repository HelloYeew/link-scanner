from typing import List
import sys
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


def get_links(link_page: str):
    """Find all links on page at the given url.

    Returns:
        a list of all unique hyperlinks on the page,
        without page fragments or query parameters.
    """
    browser = webdriver.Chrome()
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


def is_valid_url(url: str):
    """Check if url is valid.

    Returns:
        True if url is valid, False otherwise.
    """
    if requests.head(url).ok:
        return True
    return False


def invalid_urls(urllist: List[str]) -> List[str]:
    """Validate the urls in urllist and return a new list containing
    the invalid or unreachable urls.
    """
    invalid_link = []
    for url in urllist:
        if not is_valid_url(url):
            invalid_link.append(url)
    return invalid_link


if __name__ == '__main__':
    """Main function."""
    url = sys.argv[1]
    for link in get_links(url):
        print(link)
    print()
    print("Bad Links:")
    for link in invalid_urls(get_links(url)):
        print(link)

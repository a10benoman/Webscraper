import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import csv

# send a GET request to the sitemap URL
sitemap_url = "https://jsa.org/sitemap.xml"
response = requests.get(sitemap_url)

# parse the XML content of the sitemap using ElementTree
root = ET.fromstring(response.content)

# create a list to store all the extracted links
all_links = []

# iterate over all the <sitemap> elements in the index sitemap
for sitemap in root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap"):
    # send a GET request to the sitemap URL and parse the XML content using ElementTree
    sitemap_url = sitemap.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text
    sitemap_response = requests.get(sitemap_url)
    sitemap_root = ET.fromstring(sitemap_response.content)

    # iterate over all the <url> elements in the sitemap and extract their <loc> elements (i.e. the links)
    for url in sitemap_root.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}url"):
        link_url = url.find("{http://www.sitemaps.org/schemas/sitemap/0.9}loc").text

        # send a GET request to the link URL and parse the HTML content using BeautifulSoup
        link_response = requests.get(link_url)
        link_soup = BeautifulSoup(link_response.content, "html.parser")

        # extract all the links from the page and add them to the list
        for link in link_soup.find_all("a"):
            if link.has_attr("href"):
                all_links.append([link_url, link["href"]])

# save the list of links to a CSV file
with open("links.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Source URL", "Link"])
    writer.writerows(all_links)
    
# open the CSV file in a text editor or spreadsheet program
with open("links.csv") as f:
    print(f.read())

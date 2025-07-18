import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def print_results(all_links):
    for i,link in enumerate(all_links):
        print(f"{i}. {link}")
        
def saving_results(results,url):
    with open(f'Results/scrapeResult_{url}_{time.strftime('%m_%d')}.txt', 'w') as file:
        for result in results:
            file.write(result + '\n')

    print(f"\nResults exported to scrapeResult_{url}_{time.strftime('%m_%d')}.txt")
    print("="*80)

def scrape(input):
    url = "https://" + input 
   
    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'lxml') 
    links = soup.find_all('a')

    all_links = set()

    for link in links:
        href = link.get('href')

        if href and href.startswith('http'):
            full_links = href
        elif href:
            full_links = urljoin(url,href)

        if full_links not in all_links:
            all_links.add(full_links)
        
    return sorted(all_links)
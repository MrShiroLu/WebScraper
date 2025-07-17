import Modules.scraper as sc
import Modules.greeting as op
import sys
import requests

try:
    url = sys.argv[1]
except IndexError:
    print("Usage: python main.py <site_url>")
    sys.exit(1)

try:
    result = sc.scrape(url) 
    
    op.opening()
    sc.print_results(result)
    sc.saving_results(result,url)

except requests.exceptions.RequestException as e:
    print(f"+"*10+"Request ERROR!"+"+"*10)

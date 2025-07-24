import scraper as sc
import greeting as op
import sys
import requests
import time

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

except requests.exceptions.RequestException as err:
    print(f"+"*10+" ERROR "+"+"*10)
    print(f"Message: {err}")
    print(f"+"*10+" ERROR "+"+"*10)

ask = input("Do you want to find a url? (yes/no): ")

if ask == 'yes':
    
    word = input("Enter your word: ")
    finds = [find_url for find_url in result if word in find_url.lower()]
    
    for url in finds:
        print(url)
else:
    print("Thank you for using the scraper!")
    sys.exit(0)
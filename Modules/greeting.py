from pyfiglet import figlet_format

def opening():
    wellcome = figlet_format("Welcome To")
    webScraping = figlet_format("Web Scraping", font="slant")
    
    print(wellcome)
    print(webScraping)
    print("This program will scrape the links from the given URL.")
    print("="*80)
import Modules.scraper as sc
import Modules.greeting as op
import sys

url = sys.argv[1]

op.opening()

result = sc.scrape(url)

sc.print_results(result)
sc.saving_results(result,url)
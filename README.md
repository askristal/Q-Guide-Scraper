# Q-Guide-Scraper

### Requirements
- Python
- IPython Notebook
- Selenium Webdriver
- Beautiful Soup
- Pandas

## How to use:
1. Web Scraping: getguide.ipynb, run all prep cells, then run the scrapeIds function. Must fill in username and password for HarvardKey.
2. Preprocessing: run preprocessfolders.py for all folders. This will unfoldered courses with /'s.
3. Info Extraction/Processing: run process.py for all folders. This will run through all Term folders and aggregate info on each page to a CSV.
4. Postprocessing: run appendyearstocsvs.py for all CSVs to add the term and year as columns. This is to differentiate courses once they've been aggregated into the main allyears CSV.
5. Standardization: run standardizeworkload.py for all CSVs to add a Standard Workload column so you can compare workloads across the F2014 change.
6. Aggregation: run concatcsv.py to combine all Term CSVs into a single allyears CSV.
7. Analysis: analysis.ipynb, run all prep cells, load up CSVs, then have fun. Sort by workload, section ratings, or any combination of metrics. 

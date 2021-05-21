<h1 align="center">Examining the Relationship between Professional Industry and Salary to Regional Key</h2>
Performance Indicators

There is increasing concern for living in big cities, due to unemployment and the cost of living. This
project scrapes and analyzes job postings from job boards to optimize job selections based on
Key Performance Indicators including quality of life index and crime rates for various regions.

- The KPI data is obtained from https://numbeo.com. 
- The current job market is analyzed by obtaining job posting data from https://www.jobbank.gc.ca.
- NOC dataset is obtained from open government https://open.canada.ca/data/en/dataset/2192de22-84bf-4672-b0c0-f64c0cb43c94

## Setup Instructions:
The notebook that analyzes that datasets is called Final_Notebook.ipynb. For the Final_notebook.ipynb notebook to run successfuly, the DataSet folder is required to be in the same dirctory as the Final_notebook.ipynb file. All the python dependencies to run the code is located within the notebook.

The code used to scrape the numbeo and job bank data is located within the DataCollection. The .py files require one to install the depenendcies within the requirements.txt file. these dependencies can be installed by executing the command ```$ pip install -r requirements.txt```.
- scrapeJobPosting.py :  scrapes each of the job posts within https://www.jobbank.gc.ca, extracts the main html content of each page and saves the result within .bz2 files named mainsList. The files can be found with the DataSet/JobPostProcessed directory. 
- JobPostScrapeDetails.py : iterates through each of the files within the DataSet/JobPostProcessed directory and parses the HTML to extract job post details such as the job title and the expected pay. The job details are then stored in a .csv file in the DataSet/JobPostDetails directory
- scrapeNumbeo.py: scrapes the public web pages within the https://numbeo.com website and then uploads the result to a .csv file within the DataSet/Numbeo Data directory. The exact web pages that are scrapped is listed below. The data for each of the webpages is stored within its own .csv file. 

  - https://www.numbeo.com/cost-of-living/country_result.jsp?country=Canada
  - https://www.numbeo.com/property-investment/country_result.jsp?country=Canada
  - https://www.numbeo.com/health-care/country_result.jsp?country=Canada
  - https://www.numbeo.com/traffic/country_result.jsp?country=Canada
  - https://www.numbeo.com/quality-of-life/country_result.jsp?country=Canada
  - https://www.numbeo.com/crime/country_result.jsp?country=Canada 

## Reproduction Instructions:

 1. Download a web driver (such as geckodriver)
 2. Put geckodriver at the following location: SYSC4906-Project\DataCollection\geckodriver\geckodriver.exe
 3. cd DataCollection/
 4. Run python webscrape.py
 5. Run python cleanRefsList.py
 6. Change scrapeJobPosting.py so that runner = "the name of the runner"
 7. Run python scrapeJobPosting.py
 8. Run python JobPostScrapeDetails.py
 9. Run python NocValueSkillLevel.py
 10. Run python scrapeNumbeo.py
 11. Download NOC data from open data into DataSet/NOC
 12. cd to project root
 13. Run jupyter notebook
 14. Run Final_Notebook.ipynb cell by cell until completion 

## Raw and Cleaned Data:
All datasets are found in the DataSet directory.
- Job Bank Canada: 
  - Cleaned Data: ./DataSet/JobPostDetails 
  - Raw Data: ./DataSet/JobPostProcessed
- NOC Dataset:
  - ./DataSet/NOC
- Numbeo:
  - ./DataSet/NumbeoData/


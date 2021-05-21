import bz2
import pickle
from bs4 import BeautifulSoup
import requests
import time
from pathlib import Path

def removeElemsMatching(rootElem, elemToRemove, details):
	for elem in rootElem.findAll(elemToRemove, details):
		elem.decompose()

sfile = bz2.BZ2File('../DataSet/refsListCleaned.bz2', 'rb')
refs = pickle.load(sfile)
print(len(refs))
Path("./scrape").mkdir(exist_ok=True)

# first tests
#ref = 'https://www.jobbank.gc.ca/jobsearch/jobposting/34039145?source=searchresults'
# job removed:
#ref = 'https://www.jobbank.gc.ca/jobsearch/jobposting/34021435?source=searchresults'
# more info
#ref = 'https://www.jobbank.gc.ca/jobsearch/jobposting/33895735?source=searchresults'

sections = {
    "ben":0,
    "christopher":20000,
    "rahul":40000,
    "christophe":60000,
    "michael":80000
}

runner = "christopher"

relevant_refs = refs[sections[runner]:sections[runner]+20000]

listOfMains = []
for i, ref in enumerate(relevant_refs):

	html_text = requests.get(ref).text
	soup = BeautifulSoup(html_text,'lxml')
	main = soup.find('main')

	removeElemsMatching(main, 'div', {'class': 'job-posting-details-similar-jobs-wrapper'})
	removeElemsMatching(main, 'section', {'id': 'employment-groups-help-popup'})
	removeElemsMatching(main, 'section', {'class': 'job-posting-details-similar-jobs-wrapper'})
	removeElemsMatching(main, 'section', {'id': 'lightbox-resumesharing'})
	removeElemsMatching(main, 'div', {'class': 'job-posting-detail-common'})
	removeElemsMatching(main, 'div', {'id': 'jm-content'})
	removeElemsMatching(main, 'ul', {'class': 'job-posting-details-nav'})

	listOfMains.append(str(main))
	print(f"Job at {sections[runner] + i} completed")

	if len(listOfMains) == 1000:
		with bz2.BZ2File('./scrape/mainsList{}.bz2'.format(sections[runner] + i + 1), 'w') as f:
			pickle.dump(listOfMains, f)
		listOfMains = []

	#with open('test2.html', 'w') as f:
	#f.write(str(main))

# 	time.sleep(0.01)



outputFileName = 'mainsList.bz2'
with bz2.BZ2File(outputFileName, 'w') as f:
	pickle.dump(listOfMains, f)


'''
jobTitle = soup.find("h2", class_="title").text.strip()

data = soup.find("ul", class_="job-posting-brief colcount-lg-2")
city = data.find("span", class_="city").text.replace(' ','')

basePay = data.find("li", class_="fa fa-dollar")
pay = data.find("span", property="minValue").text
payUnit = data.find("span", property="unitText").text.strip()'''

#print(f'''
#Job Title: {jobTitle}
#City: {city}
#Pay: {pay}
#PayUnit: {payUnit}
#''')


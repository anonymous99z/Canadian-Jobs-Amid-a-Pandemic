from selenium import webdriver
import time
import bz2
import pickle

driver = webdriver.Firefox(executable_path= r"geckodriver\\geckodriver.exe")

listOfRefs = []

for i in range(1, 3801):
	driver.get('https://www.jobbank.gc.ca/jobsearch/jobsearch?page={}&sort=D'.format(i))

	time.sleep(5)
	articles = driver.find_elements_by_tag_name('article')

	for article in articles:
		listOfRefs.append(article.find_element_by_xpath('.//a[@href]').get_attribute("href"))

	if i % 100 == 0:
		print(i)
		with bz2.BZ2File('./scrape/refsList{}.bz2'.format(i), 'w') as f:
			pickle.dump(listOfRefs, f)

print(len(listOfRefs))

outputFileName = 'refsList.bz2'
sfile = bz2.BZ2File(outputFileName, 'w')
pickle.dump(listOfRefs, sfile)

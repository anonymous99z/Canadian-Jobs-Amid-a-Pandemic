import os
import bz2
import pickle
import pandas
from lxml import etree
import time

totalHtmlFilesToProcess = 0
jobPostDetails = []

def extractInfo(htmlFile, i):
    #soup = BeautifulSoup(htmlFile,'lxml')
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(htmlFile, htmlparser)
    #tree.xpath(xpathselector)

    r = tree.xpath('//span[@property="title"]')
    jobTitle = r[0].text.strip() if len(r)>0 else ''

    # Not available or to be discussed or messy string
    r = tree.xpath('//ul[@class="job-posting-brief colcount-lg-2"]/li[2]')
    rawPay = ''.join(r[0].itertext()).replace('Salary','').strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="minValue"]')
    minPay = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="maxValue"]')
    maxPay = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="unitText"]')
    payUnit = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="workHours"]')
    workHours = r[0].text.strip() if len(r)>0 else ''

    #start date
    r = tree.xpath('//span[@class="fa fa-calendar"]')
    startDate = ''.join(r[0].getparent().itertext()).replace('Start date','').strip() if len(r)>0 else ''

    #r = tree.xpath('//span[@class="fa fa-file-text-o"]')
    r = tree.xpath('//span[@property="employmentType"]')
    employmentTypeList = list(r[0].itertext()) if len(r)>0 else ''
    employmentTerms = employmentTypeList[0].strip() if len(employmentTypeList)>0 else ''
    fullOrPartTime = employmentTypeList[1].strip() if len(employmentTypeList)>1 else ''

    r = tree.xpath('//span[@class="fa fa-user"]')
    vacancies = list(r[0].getparent().itertext())[3].strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="specialCommitments"]')
    specialCommitment = r[0].text.strip() if len(r)>0 and r[0].text != None else ''
    r = tree.xpath('//span[@property="benefits"]')
    benefits = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//div[@class="job-posting-details-jmi-wrapper"]//dd')
    medianWage = ''.join(r[0].itertext()).strip() if len(r)>0 else ''
    r = tree.xpath('//time[@property="dateModified"]')
    dateModified = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//span[@property="hiringOrganization"]')
    hiringOrg = ''.join(r[0].itertext()).strip() if len(r)>0 else ''
    r = tree.xpath('//span[@class="source-image"]')
    jobSource = ''.join(r[0].itertext()).strip() if len(r)>0 else ''
    r = tree.xpath('//span[@class="noc-no"]')
    nocNo = r[0].text.strip()[4:] if len(r)>0 else ''
    r = tree.xpath('//span[@class="noc-title"]')
    nocTitle = r[0].text.strip() if len(r)>0 else ''

    r = tree.xpath('//p[@property="educationRequirements"]')
    educationReqs = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//p[@property="qualifications"]')
    qualifications = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//p[@property="description experienceRequirements"]')
    experienceReqs = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//dd[@property="responsibilities"]')
    responsibilities = r[0].text.strip() if len(r)>0 else ''
    r = tree.xpath('//div[@property="skills"]')
    skills = ' '.join(r[0].itertext()).strip() if len(r)>0 else ''
    r = tree.xpath('//div[@class="job-posting-detail-requirements"]/p')
    language = r[0].text.strip() if len(r)>0 else ''

    postingId = refs[i][47:55]
    href = 'https://www.jobbank.gc.ca/jobsearch/jobposting/{}'.format(postingId)

    # Location
    address = ''
    city = ''
    postalCode = ''
    singleCity = tree.xpath('//span[@class="city"]')
    multiCity = tree.xpath('//ul[@class="colcount-sm-2"]/li')
    if len(singleCity)>0:
        locationList = list(singleCity[0].itertext())
        #rawCity = ' '.join(locationList).strip() if len(r)>0 else ''

        if len(locationList)==1:
            city = locationList[0]
        elif len(locationList)==3:
            address = locationList[0]
            city = locationList[1]
            postalCode = locationList[2]
        jobPostDetails.append((jobTitle, rawPay, minPay, maxPay, payUnit, workHours, startDate,
        employmentTerms, fullOrPartTime, vacancies, specialCommitment, benefits, medianWage,
        dateModified, hiringOrg, jobSource, nocNo, nocTitle, educationReqs, qualifications, experienceReqs,
        responsibilities, skills, language, postingId, href, address, city, postalCode))

    elif len(multiCity)>0:
        locationList = list(multiCity[0].getparent().itertext()) if len(r)>0 else ''
        locationsPerCity = int(len(locationList) / len(multiCity))

        for index, cityElem in enumerate(multiCity):
            if locationsPerCity < 2:
                city = cityElem.text
            elif locationsPerCity == 3:
                tripleIndex = 3*index
                address = locationList[tripleIndex]
                city = locationList[tripleIndex+1]
                postalCode = locationList[tripleIndex+2]
            jobPostDetails.append((jobTitle, rawPay, minPay, maxPay, payUnit, workHours, startDate,
                employmentTerms, fullOrPartTime, vacancies, specialCommitment, benefits, medianWage,
                dateModified, hiringOrg, jobSource, nocNo, nocTitle, educationReqs, qualifications, experienceReqs,
                responsibilities, skills, language, postingId, href, address, city, postalCode))
    #end function


startTime = time.perf_counter()
sfile = bz2.BZ2File('../DataSet/refsListCleaned.bz2', 'rb')
refs = pickle.load(sfile)

files = []
directory = "../DataSet/JobPostProcessed"
for filename in os.listdir(directory):
    i = 0
    if filename.endswith(".bz2"):
        file = bz2.BZ2File(os.path.join(directory, filename), 'rb')
        file = pickle.load(file)

        print(os.path.join(directory, filename))
        totalHtmlFilesToProcess += len(file)

        startingNumber = int(filename[9:-4])-1000
        for htmlFile in file:
            extractInfo(htmlFile, startingNumber+i)
            i+=1

df = pandas.DataFrame(jobPostDetails, columns = ['Job Title', 'RawPay','MinPay', 'MaxPay', 'PayUnit', 'WorkHours', 'StartDate',
    'EmploymentTerms', 'FullOrPartTime', 'Vacancies', 'SpecialCommitment', 'Benefits', 'MedianWage',
    'DateModified', 'HiringOrg', 'JobSource', 'NocNo', 'NocTitle', 'EducationReqs', 'Qualifications', 'ExperienceReqs',
    'Responsibilities', 'Skills', 'Language', 'PostingId', 'Href', 'Address', 'City', 'PostalCode'])
df.to_csv('../DataSet/JobPostDetails/data.csv', index = False)
            
endTime = time.perf_counter()
print(f"Spent {endTime - startTime:0.4f} seconds")




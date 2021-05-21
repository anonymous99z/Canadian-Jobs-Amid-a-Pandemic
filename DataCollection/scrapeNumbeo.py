from bs4 import BeautifulSoup
import requests
import pandas as pd 


def get_data(key,url):
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    table_data = soup.find('table', id = 't2')

    headers = table_data.find('thead')
    colNamesHTML = headers.find_all('div')
    headers_list = []
    for headerName in colNamesHTML:
        headers_list.append(headerName.text)


    row_data = table_data.find_all('tr')

    array_2d = []
    for data in row_data:
        content = data.find_all('td')
        vals = []
        for values in content:
            vals.append(values.text)

        array_2d.append(vals)

    array_2d.pop(0) # Remove an empty list that always appears 
    #print(array_2d)

    df = pd.DataFrame(array_2d, columns = headers_list) 
    #df
    
    # Save to CSV
    df.to_csv('../DataSet/Numbeo Data/' + key + '.csv', index = False)
    print('Data saved to: ../DataSet/Numbeo Data/' + key +'.csv')


urls = {
    'CostofLiving': 'https://www.numbeo.com/cost-of-living/country_result.jsp?country=Canada',
    'PropertyPrices': 'https://www.numbeo.com/property-investment/country_result.jsp?country=Canada',
    'HealthCare': 'https://www.numbeo.com/health-care/country_result.jsp?country=Canada',
    'Traffic': 'https://www.numbeo.com/traffic/country_result.jsp?country=Canada',
    'Quality of Life': 'https://www.numbeo.com/quality-of-life/country_result.jsp?country=Canada',
    'Crime': 'https://www.numbeo.com/crime/country_result.jsp?country=Canada'

}

for key in urls:
    get_data(key, urls[key])
from selenium import webdriver
import bs4 as bs
import time
import re
import csv

from flask import Flask
app= Flask(__name__)

@app.route('/green')


BASEURL = 'http://oceandatacenter.ucsc.edu/SCOOP/index.html'

def loadDriver():
    ## handles the web browser which selenium will control

    driver = webdriver.Chrome()
    return driver

def handleUrl(driver, BASEURL):
    ## bulk of the work for the web driver... implicitly waits until the data is loaded
    ## before returning the page source

    driver.get(BASEURL)
    driver.implicitly_wait(100)
    gTags = driver.find_elements_by_css_selector('script')
    pgs = driver.page_source

    return pgs

def closeDriver(driver):
    ## simply handles closing the driver to avoid slower processes
    ## the driver is not needed as soon as Beautiful Soup can take over

    driver.close()


def convertToBs(pageSource):
    ## converts page source to a Beautiful Soup object

    soup = bs.BeautifulSoup(pageSource, 'lxml')
    print('succesfully converted page source to beautiful soup')


    return soup

def parseTable(table):
    varList = []
    factsList = []

    table = soup.find('table', {'id':table})
    for row in table.find_all('td', {'class':'text'}):
        divOrNot = row.find('div', {'align': 'left'})
        if divOrNot != None:
            varList.append(divOrNot.text)
        else:
            total = row.text
            scriptTag = row.script

            if scriptTag != None:
                unwanted = scriptTag.text

                dataList = total.split(unwanted)
                splitList = dataList[1].split(' ')

                value = splitList[0].strip('\n')
                units = splitList[-1]

                factsList.append([value, units])

            else:
                pass

    return varList, factsList

def getFacts(soup):
    weatherVars , weatherFacts = parseTable('met_table')
    waterVars, waterFacts = parseTable('ctd_table')

    return weatherVars, weatherFacts, waterVars, waterFacts

def saveToText(weatherVars, weatherFacts, waterVars, waterFacts):

    f = open('liveData.txt', 'a+')

    for i in range(0, len(weatherVars)-1):
        f.write(weatherVars[i] + '...' + weatherFacts[i][0] + '\n')

    f.write('\n$$$$$$$$$$$$$$$\n\n')

    for i in range(0, len(waterVars)-1):
        f.write(waterVars[i] + '...' + waterFacts[i][0] + '\n')
    f.write('\n\n\n')

    f.close()

## handles all things to do with the web driver
driver = loadDriver()
pgs = handleUrl(driver, BASEURL)
closeDriver(driver)

#converts the page source found by the driver into a parseable object for Beautiful Soup
soup = convertToBs(pgs)
weatherVars, weatherFacts, waterVars, waterFacts = getFacts(soup)
saveToText(weatherVars, weatherFacts, waterVars, waterFacts)

print('DONE!')

from flask import Flask

app = Flask(__name__)

from bs4 import BeautifulSoup
from urllib.request import urlopen
import re


def getDogDataByAppNum(appNum):

    dogArray = []
    newObj = {}

    url = "https://api.ofa.org/api/as.php?a=/advanced-search/&appnum=" + appNum
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")

    textToChange = soup.find("table", {"id": "as_detail_tests"})
    # print(textToChange)

    pattern = "<thead>.*?</thead>"
    match_results = re.search(pattern, html, re.IGNORECASE)
    title = match_results.group()
    title = re.sub("<.*?>", "  ", title) # Remove HTML tags
    headerList = title.split("  ")
    headerList = [x for x in headerList if x and x!='&ZeroWidthSpace;' and x!='(m)'] # Remove empty elements
    for header in headerList:
        newObj[header] = ''



    prj=textToChange.get_text(strip=True)
    trs = soup.find('table', attrs= {'id': 'as_detail_tests'}).find_all('tr')

    table_data = [[cell.text for cell in row("td")]
                            for row in trs]

    table_data.pop(0)


    for row in table_data:
        newObj = {}
        for i in range(len(row)):
            newObj[headerList[i]] = row[i]
        dogArray.append(newObj)

    return dogArray

def getDogFullDeets(regnum):

    from bs4 import BeautifulSoup
    import requests

    url = "https://api.ofa.org/api/as.php"

    # Post specific day to get one day of data
    # params ={'api_action': 'as_action',
    # 'api_key':'',
    # 'api_preset':'cst',
    # 'api_sort': '',
    # 'api_sort_prior': 'name',
    # 'api_sort_dir': 'A',
    # 'api_page': '',
    # 'api_layout': 'S',
    # 'as_filter[regnum]': 'TR90342204',
    # 'as_filter[regnums]': '',
    # 'as_filter[regname]': '' ,
    # 'as_filter[fullpart]':'F',
    # 'as_filter[ofanum]': '',
    # 'as_filter[special][chic]': 'N',
    # 'as_filter[special][dnabank]': 'N',
    # 'as_filter[special][photo]': 'N',
    # 'as_filter[brdname]': '',
    # 'as_filter[brdvar][]': '',
    # 'as_filter[birthyear_from]': '',
    # 'as_filter[birthyear_thru]': '',
    # 'as_filter[sire_regnum]': '',
    # 'as_filter[dam_regnum]': '',
    # 'as_filter[testname]': '',
    # 'as_filter[notation_combo][]': 'A'} 
    params ={'api_action': 'as_action',
    'api_key':'',
    'api_preset':'cst',
    'api_sort': '',
    'api_sort_prior': 'name',
    'api_sort_dir': 'A',
    'api_page': '',
    'api_layout': 'S',
    'as_filter[regnum]': regnum,
    'as_filter[regnums]': '',
    'as_filter[regname]': '' ,
    'as_filter[fullpart]':'F',
    'as_filter[ofanum]': '',
    'as_filter[special][chic]': 'N',
    'as_filter[special][dnabank]': 'N',
    'as_filter[special][photo]': 'N',
    'as_filter[brdname]': '',
    'as_filter[birthyear_from]': '',
    'as_filter[birthyear_thru]': '',
    'as_filter[sire_regnum]': '',
    'as_filter[dam_regnum]': '',
    'as_filter[testname]': '',
    'as_filter[notation_combo][]': 'A'} 
    response = requests.post(url,data=params)
    content = response.content
    # print(content)

    soup = BeautifulSoup(content, "html.parser")

    # print(soup)

    trHeader = soup.find_all('tr')
    table_header = [th.text for th in trHeader[0].find_all('th')]


    trs = soup.find_all('tr', attrs= {'class': 'as_results_row'})



    table_data = [[cell.text for cell in row("td")]
                                for row in trs]

    new_Table_data = []

    for row in table_data:
        row = row[0:7]
        new_Table_data.append(row)


    idArray = []

    sample = soup.find_all('tr', attrs= {'class': 'as_results_row'})
    for record in sample:
        use = sample[0]
        id = re.search(pattern="<tr .*?>(.+?)>", string=str(use))
        splitID = id.group(0).split('data-appnum="')[1].split('"')[0]
        idArray.append(splitID)

    array = []

    for row in new_Table_data:
        newObj = {}
        for i in range(len(row)):
            newObj[table_header[i]] = row[i]
        newObj['appNum'] = idArray.pop(0)
        array.append(newObj)

    # print(soup)
    for dog in array:
        dog['TestHistory'] = getDogDataByAppNum(dog['appNum'])

    return array

@app.route("/")
def hello_world():
    return getDogFullDeets("TR90342204")

@app.route("/dog/<dogId>")
def dog_endpoint(dogId):
    return getDogFullDeets(dogId)
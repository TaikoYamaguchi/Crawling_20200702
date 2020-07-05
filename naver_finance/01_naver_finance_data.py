import requests
from bs4 import BeautifulSoup
import pandas as pd
import lxml
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import re

#페이지 정보 갖고오
browser = Chrome('/Users/taikoyamaguchi/Desktop/chromedriver')
browser.maximize_window()



def stock_crawler(code):
    # code = 종목번호
    name = code
    base_url = 'https://finance.naver.com/item/coinfo.nhn?code=' + name + '&target=finsum_more'

    browser.get(base_url)
    # frmae구조 안에 필요한 데이터가 있기 때문에 해당 데이터를 수집하기 위해서는 frame구조에 들어가야한다.
    browser.switch_to_frame(browser.find_element_by_id('coinfo_cp'))

    # 재무제표 "연간" 클릭하기
    browser.find_elements_by_xpath('//*[@class="schtab"][1]/tbody/tr/td[3]')[0].click()

    html0 = browser.page_source
    html1 = BeautifulSoup(html0, 'html.parser')

    # 기업명 뽑기
    title0 = html1.find('head').find('title').text
    print(title0.split('-')[-1])

    html22 = html1.find('table', {'class': 'gHead01 all-width', 'summary': '주요재무정보를 제공합니다.'})

    # date scrapy
    thead0 = html22.find('thead')
    tr0 = thead0.find_all('tr')[1]
    th0 = tr0.find_all('th')

    date = []
    for i in range(len(th0)):
        date.append(''.join(re.findall('[0-9/]', th0[i].text)))

    # columns scrapy
    tbody0 = html22.find('tbody')
    tr0 = tbody0.find_all('tr')

    col = []
    for i in range(len(tr0)):

        if '\xa0' in tr0[i].find('th').text:
            tx = re.sub('\xa0', '', tr0[i].find('th').text)
        else:
            tx = tr0[i].find('th').text

        col.append(tx)

    # main text scrapy
    td = []
    for i in range(len(tr0)):
        td0 = tr0[i].find_all('td')
        td1 = []
        for j in range(len(td0)):
            if td0[j].text == '':
                td1.append('0')
            else:
                td1.append(td0[j].text)

        td.append(td1)

    td2 = list(map(list, zip(*td)))

    return pd.DataFrame(td2, columns=col, index=date)

newdata = stock_crawler('005930')
newdata['CMP_CODE']= "005930"
print(newdata)
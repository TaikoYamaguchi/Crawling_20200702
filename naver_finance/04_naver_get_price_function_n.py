import requests
from bs4 import BeautifulSoup

#페이지 정보 갖고오
def get_bs_obj(company_code):
    url = "https://finance.naver.com/item/main.nhn?code="+ company_code
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj

#가격 가져오기
def get_price(company_code):
    bs_obj = get_bs_obj(company_code)
    no_today = bs_obj.find("p", {"class": "no_today"})
    blind_now = no_today.find("span", {"class": "blind"})
    return blind_now.text

company_codes=["005930","000660"]
for item in company_codes:
    print(get_price(item))
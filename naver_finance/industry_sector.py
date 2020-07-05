import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

# 페이지 정보 갖고오기
index_code = ['G1010', 'G1510', 'G2010', 'G2020', 'G2030', 'G2510', 'G2520', 'G2530', 'G2550', 'G2560', 'G3010',
              'G3020', 'G3030', 'G3510', 'G3520', 'G4010', 'G4020', 'G4030', 'G4040', 'G4050', 'G4510', 'G4520',
              'G4530', 'G4535', 'G4540', 'G5010', 'G5020', 'G5510']

def get_bs_obj():
    url0 = "http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20200701&sec_cd=" + index_code[0]
    result0 = requests.get(url0)
    bs_obj0 = BeautifulSoup(result0.content, "html.parser")
    value0 = json.loads(bs_obj0.text)["list"]
    for i in index_code[1:]:
        url = "http://www.wiseindex.com/Index/GetIndexComponets?ceil_yn=0&dt=20200701&sec_cd=" + i
        result = requests.get(url)
        bs_obj = BeautifulSoup(result.content, "html.parser")
        value_instance = json.loads(bs_obj.text)["list"]
        value0 = value0 + value_instance
    return value0


final_data = pd.DataFrame(get_bs_obj())
print(final_data)
final_data.info()
final_data.to_excel('sector_data.xlsx')
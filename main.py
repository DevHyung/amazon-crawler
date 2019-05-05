import requests
import my_util
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import time


'''========== CONFIG AREA START =========='''
FILENAME = "아마존"  # without file extention
headerList = ['키워드','상품명','가격','이미지링크','상품링크']
excelWidthDict = {  # 엑셀 column 조정 dict
    'A': 20,
    'B': 40,
    'C': 10,
    'D': 30,
    'E': 50,
}
excel = my_util.ExcelDriver(FILENAME,headerList)
excel.set_col_width(excelWidthDict)
'''========== CONFIG AREA END   =========='''

if __name__ == "__main__":
    baseUrl = 'https://www.amazon.co.jp'
    driver = webdriver.Chrome('./chromedriver')
    driver.get(baseUrl)

    while True:
        k = input(">>> INPUT KEYWORD. If you want exit, input 0 : ").strip()
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').clear()
        driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(k+'\n')
        time.sleep(random.randint(3,7))
        if k == '0':
            break
        bs = BeautifulSoup(driver.page_source,'lxml')

        # 몇번째 상품
        products = bs.find_all('div',class_='sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32')

        dataList = []
        idx : int = 1
        for div in products:
            # info쪽 div잡아서 정보추출
            info = div.find('div',class_='a-section a-spacing-medium')
            infos = info.find_all('div',class_='sg-col-inner')

            # 0 없고 1이미지 2별점 3가격
            try:
                title = infos[2].h2.get_text().strip()
                imgLink = infos[1].find('img',class_='s-image')['src']# 이미지
                productLink = baseUrl+infos[1].find('a',class_='a-link-normal')['href'] # 링크
                price = infos[3].find('span',class_='a-price').find('span',class_='a-price-whole').get_text().strip()
                print("{}번째 상품 : {} 추출완료".format(idx,title))
                dataList.append([k,title,price,imgLink,productLink])
            except:
                print("{}번째 상품 : {} 오류".format(idx, title))
            finally:
                idx += 1
        excel.append_data_list(dataList)

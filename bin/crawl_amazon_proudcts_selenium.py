from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager 
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup

import time 
import urllib
import random
import re
import pandas as pd
import os 
import sys 
import requests


current_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current_path)
sys.path.append(os.path.normpath(os.path.join(current_path, '../')))
sys.path.append(os.path.normpath(os.path.join(current_path, '../../')))


class ACrawler():
    def __init__(self, parent):
        self.parent = parent
        self.driver = None
        self.img_search_page = None
        self.valid_max_num_page = None
        self.contents = None
        self.product_title = None
        self.product_price = None
        self.product_img_url = None
        self.product_rating = None
        self.product_rating_count = None
        self.product_delivery_site = None
        self.data = []
        self.data_frame = []
        self.count = 1
        self.title = None
        self.price = None
        self.img_url = None
        self.rating = None
        self.rating_count = None
        self.delivery_site = None
    
    # 초기 드라이버 세팅하기
    def set_init_driver(self, chrome_options):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        time.sleep(1)
        
    # 찾는 개수중에서 숫자만 parsing해오기
    def validate_max_num_page(self, total_page_num):
        for i in total_page_num.split():
            if ':' in i:
                self.valid_max_num_page = re.findall(r'\d+', total_page_num[1:])[0]
        self.valid_max_num_page =  int(re.findall(r'\d+', total_page_num)[0])
    
    # 아마존 1번째 구매 사이트 로딩하기
    def load_searching_page(self, search_key):
        # https://amazon.kr/s?k=나이키+신발&page=1
        for page_idx in range(1, self.valid_max_num_page+1):
            for key in search_key.split():
                if ':' in key:
                    if len(search_key.split()) >= 3:
                        self.img_search_page = 'https://amazon.com/s?k={}&page={}'.format('+'.join(e for e in search_key.split()[1:]), page_idx)
                        break
                    else: 
                        self.img_search_page = 'https://amazon.com/s?k={}&page={}'.format(search_key.split()[1], page_idx)
                        break
                else:
                    if len(search_key.split()) >= 2:
                        self.img_search_page = 'https://amazon.com/s?k={}&page={}'.format('+'.join(e for e in search_key.split()), page_idx)
                        break
                    else:
                        self.img_search_page = 'https://amazon.com/s?k={}&page={}'.format(search_key.split()[0], page_idx)
                        break
            self.driver.get(url=self.img_search_page)
            self.driver.implicitly_wait(time_to_wait=10)
            self.set_random_time_out()
            self.get_all_relevent_contents()
        self.write_data_to_the_csv_file()
    
    # 랜덤한 시간동안 타이머 멈추기
    def set_random_time_out(self):
        return time.sleep(random.uniform(0.3, 0.7))
    
    # 검색 된 사진 한장 한장 클릭하면서 HD 이미지 다운로드 하기
    def get_all_relevent_contents(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for result in results:
            try:
                # 'class' 속성이 'a-size-mini'인 모든 'h2' 태그의 text을 찾는다.
                title = result.find('h2', {'class': 'a-size-mini'}).text.strip()
            except AttributeError:
                title = 'N/A'

            try:
                price = result.find('span', {'class': 'a-offscreen'}).text.strip()
            except AttributeError:
                price = 'N/A'
                
            try:
                img_url = result.find('img', {'class': 's-image'}).get('src')
            except AttributeError:
                img_url = 'N/A'

            try:
                reviews = result.find('span', {'class': 'a-icon-alt'}).text.strip()
            except AttributeError:
                reviews = 'N/A'

            try:
                review = result.find('span', {'class': 'a-size-base'}).text.strip()
            except AttributeError:
                review = 'N/A'
            
            try:
                review_count = result.find('span', {'class': 'a-size-base s-underline-text'}).text.strip().replace('(', '').replace(')', '')
            except AttributeError:
                review_count = 'N/A'

            print(f'Count: {self.count}')
            print(f'Title: {title}')
            print(f'Price: {price}')
            print(f'Image URL: {img_url}')
            print(f'Reviews: {reviews}')
            print(f'Review: {review}')
            print(f'Review Count: {review_count}')
            print('\n')
            
            self.count += 1
            self.data.append([title, price, img_url, review, review_count])
                 
    def write_data_to_the_csv_file(self):
        self.data_frame = pd.DataFrame(self.data, columns = ['product_title', 'product_price', 'product_img_url', 'product_rating', 'product_rating_count'])
        self.data_frame.to_csv(os.path.normpath(os.path.join(self.parent.save_file_line_edit.text(), 'amazon_products.csv')), index=True)
    
    def run(self):
        self.set_init_driver(webdriver.ChromeOptions())
        self.validate_max_num_page(self.parent.max_num_page_line_edit.text().strip())
        self.set_random_time_out()
        self.load_searching_page(self.parent.search_line_edit.text().strip())
        self.parent.time_worker.working = False















            
        # # HTML 코드를 파싱합니다.
        # soup = BeautifulSoup(html, 'html.parser')
        
        # # 추출하고자 하는 데이터를 선택합니다.
        # items = soup.select('div.s-card-container')
        # for item in items:
        #     # 제목 추출
        #     try:
        #         self.title = item.select(".s-result-item .a-text-normal").text.strip()
        #         #  soup.select(".s-result-item .a-text-normal")
        #     except:
        #         self.title ='N/A'
        #     print('{} title is {}'.format(self.count, self.title))
                
        #     # 가격 추출
        #     try:
        #         self.price = item.select_one('.a-offscreen').text.strip()
        #     except:
        #         self.price ='N/A'
        #     print('{} price is {}'.format(self.count, self.price))
            
        #     # 이미지 URL 추출
        #     try:
        #         self.img_url = item.select_one('.s-image')['src']
        #     except:
        #          self.img_url  ='N/A'
        #     print('{} img_url is {}'.format(self.count, self.img_url))
            
        #     # 제품 평점 추출
        #     try:
        #         self.rating = item.select_one('.a-size-base').text.strip()
        #         if len(self.rating) > 3:
        #             self.rating = 'N/A'
        #     except:
        #          self.rating  ='N/A'
        #     print('{} rating is {}'.format(self.count, self.rating))
            
        #     # 제품 평점 수 추출
        #     try:
        #         self.rating_count = item.select_one('.a-size-base.s-underline-text').text.strip().replace('(','').replace(')','')
        #         if not self.rating_count.replace(',', '').isnumeric():
        #             self.rating_count  ='N/A'
        #     except:
        #          self.rating_count  ='N/A'
        #     print('{} rating_count is {}'.format(self.count, self.rating))

            # self.count += 1
            # self.data.append([self.title, self.price, self.img_url, self.rating, self.rating_count])

# ===================== Component Debugging Code ========================#
#             print('{} img_url is {}'.format(self.count, self.img_url))
#             self.count += 1

# # 검색 된 사진 한장 한장 클릭하면서 HD 이미지 다운로드 하기
#     def get_all_relevent_contents(self):
#         # 전체 제품을 담은 컨텐츠 카드 추출해 오기
#         self.contents = self.driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div/div/div')
#         print('There are {} number of contents available on this page'.format(len(self.contents)))
#         for content in self.contents:
            
#             # 1: 제목 가져오기
#             try:
#                 self.product_title = content.find_element(By.TAG_NAME, 'h2').text
#             except:
#                 self.product_title = 'N/A'
#             # print('product_title is ', product_title)
            
#             # 2: 가격 가져오기
#             try:
#                 self.product_price = content.find_element(By.CLASS_NAME, 'a-price-whole').text + '.'+ content.find_element(By.CLASS_NAME, 'a-price-fraction').text
#             except:
#                 self.product_price = 'N/A'
#             # print('product_price is ', product_price)
            
#             # 3: 이미지 가져오기
#             try:
#                 self.product_img_url = content.find_element(By.TAG_NAME, 'img').get_attribute('src') 
#             except:
#                 self.product_img_url = 'N/A'
#             # print('product_img_url is ', product_img_url)
            
#             # 4: 제품 리뷰 가져오기
#             try:
#                 self.product_rating = content.find_element(By.CLASS_NAME, 'a-size-base').text
#             except:
#                 self.product_rating = 'N/A'
#             # print('product_rating is ', product_rating)
            
#             # 5: 제품 리뷰 수 가져오기
#             try:
#                 self.product_rating_count = content.find_element(By.CLASS_NAME, 'a-size-base.s-underline-text').text.replace('(', '').replace(')','')
#             except:
#                 self.product_rating_count = 'N/A'
#             # print('product_rating_count is ', product_rating)
            
#             # 6: 제품 배달 도착장소 가져오기
#             try:
#                 self.product_delivery_site = ' '.join(e for e in content.find_element(By.CLASS_NAME, 'a-size-small.a-color-base').text.split()[2:])
#             except:
#                 self.product_delivery_site = 'N/A'
            
#             print('제품 제목은 ', self.product_title)
#             print('제품 가격은 ', self.product_price)
#             print('제품 이미지은 ', self.product_img_url)
#             print('제품 평점은 ', self.product_rating)
#             print('제품 평점 개수는 ', self.product_rating_count)
#             print('제품 배달지역은 ', self.product_delivery_site)
            
#             self.data.append([self.product_title, self.product_price, self.product_img_url, self.product_rating, self.product_rating_count, self.product_delivery_site])
# from selenium.webdriver.common.keys import Keys
# from selenium import webdriver 
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager 

# import pandas as pd
# import time 
# import urllib
# import pymysql

# # 필요한 크롬 드라이버 셋업하기 
# headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
# chrome_options = webdriver.ChromeOptions()

# # 자동화 봇 감지 오류를 피하기 위해서 크롬 옵션을 추가해주기
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# # 기본 아마존 페이지를 처음에 한번 로드합니다.
# main_url = 'https://amazon.kr'
# driver.get(url=main_url)
# time.sleep(2.5)

# # 키워드를 검색한 이후에 전체 페이지 수를 파악 

# item_search_input = driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]')

# searchKey = 'Intel Core'
# item_search_input.send_keys(searchKey)
# item_search_input.send_keys(Keys.ENTER)

# 스크롤 내리기 전 높이
# 윈도우에서 Javascript 명령어를 실행하기
prev_height = driver.execute_script("return window.scrollY")
# 무한 스크롤 
while True:
    # 맨 아래로 스크롤 내리기
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(1)
    
    # 스크롤 후의 높이 
    post_height = driver.execute_script("return window.scrollY")
    if post_height == prev_height:
        break 
    prev_height = post_height

# product_title과 product_price을 조사해서 parsing합니다

# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[3]/div/div/div/div
# //*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[4]/div/div/div/div

cnt = 1
items = driver.find_elements(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div/div/div/div')
# print('length of items is ', len(items))

for item in items:
    try:
        product_title = item.find_element(By.CLASS_NAME, 'a-size-medium').text
    except:
        product_title = 'N/A'
    try:
        product_whole_price = item.find_element(By.CLASS_NAME, 'a-price-whole').text
    except:
        product_whole_price = 'N/A'
    try:
        product_fraction_price = item.find_element(By.CLASS_NAME, 'a-price-fraction').text 
    except:
        product_fraction_price = 'N/A'
    
    # print(f'{[cnt]}', product_title)
    final_price = product_whole_price + '.' + product_fraction_price
    # print('final_price is ', final_price)
    cnt += 1
    

# product_id는 int 
# product_title는 varchar(255)
# final_price는 double로 저장하기


# localhost란 내 컴퓨터 기기라는 뜻이고, user는 계정정보를 의미하며 (root 계정), 비밀번호는 mysql 생성시에 사용했던 비밀번호이며, utf8로 인코딩을 해서 db에 접속한다라는 의미이다.
# 그리고 이를 db라는 변수에 담는다.
try:
    db = pymysql.connect(host='localhost', user='root', password='0000', charset='utf8')
    print('db connection succeeds!')
except:
    print('db connection fails!')

try:
    # db의 cursor을 생성해서 지정해준다. 
    cursor = db.cursor()
    print('db cursor succeeds!')
except:
    print('database cursor fails!')

print('지금 데이터 베이스 object는 ', db)

# 없으면 Amazon database를 만들어 준다.
try:
    sql_query = 'CREATE DATABASE if NOT EXISTS Amazon'
    cursor.execute(sql_query)
    print('create_database succeeds!')

except:
    print('database creation fail!')

try:
    sql_query = 'USE Amazon'
    cursor.execute(sql_query)
    print('changing the database succeeds!')

except:
    print('changing the database fails!')

# Amazon DB 안에, product_id, product_title, product_price column(attribute)을 만들어준다.
try:
    sql_query = ''' CREATE TABLE IF NOT EXISTS Products (
        
    product_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    product_title VARCHAR(255),
    product_price VARCHAR(255)
)
'''
    cursor.execute(sql_query)
    print('table creation succeeds!')

except:
    print('table creation fails!')

try:
    item = 'candy'
    sql_query = ''' INSERT INTO Products (product_id, product_title, product_price) 
                    VALUES (product_id, '%s', '200')''' % (item)
                
    sql_query_2 = ''' INSERT INTO Products (product_id, product_title, product_price) 
                    VALUES (product_id, '%s', '200') ''' % (item)
               
    sql_query_3 = ''' INSERT INTO Products (product_id, product_title, product_price) 
                    VALUES (product_id, '%s', '200') ''' % (item)
               
    cursor.execute(sql_query)
    cursor.execute(sql_query_2)
    cursor.execute(sql_query_3)
    print('data insertion succeeds!')

except:
    print('data insertion fails!')

try:
    db.commit()
    db.close()
    print('db commit and cursor close succeeds!')
except:
    print('db commit and close fails!')


while True:
    pass


import requests
from bs4 import BeautifulSoup

keyword = '아마존'
num_pages = 5

url = f'https://www.amazon.com/s?k={keyword}&page={{}}'

for page in range(1, num_pages+1):
    page_url = url.format(page)
    
    response = requests.get(page_url)
    html = response.text
    
    soup = BeautifulSoup(html, 'html.parser')
    
    items = soup.select('div.s-result-item')
    
    for item in items:
        title = item.select_one('h2 a').text.strip()
        price = item.select_one('span.a-price-whole').text.strip()
        rating = item.select_one('span.a-icon-alt').text.strip()
        
        print(title, price, rating)
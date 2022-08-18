import requests
from bs4 import BeautifulSoup
import pandas as pd



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

#aramada birden fazla kelime olursa aralarına '+' işareti atmak için;
search_query = 'kindle'.replace(' ', '+')

# Bir arama yapıldığında (kindle) örnek link şu şekildedir:
# https://www.amazon.com/s?k=kindle&sprefix=kin%2Caps%2C243&ref=nb_sb_ss_ts-doa-p_1_3
#ortadaki kindle yazısına ulaşmak için:
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

items = []
#ilk 5 sayfayı getirmesini istedim
for i in range(1, 5):
    
    #Eğer kindle yazıp 2. sayfaya tıklarsam link şu şekilde olur:
    #https://www.amazon.com.tr/s?k=kindle&page=2&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=ITUXR3K0FLF5&qid=1660681078&sprefix=kindle%2Caps%2C224&ref=sr_pg_2
    #linkin içinde kindle'dan sonra &'ler içinde page=2 yazmaktadır. Bu kısıma ulaşmak gerekmektedir.
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    #ürün adı div'in içinde gösterilmektedir.
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        
        #ürün adı
        product_name = result.h2.text

        try:
            #puanlama
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})[0].text
        except AttributeError:
            continue

        try:
            #fiyatlar
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price1 + price2)
            #ürün linki
            product_url = 'https://amazon.com' + result.h2.a['href']
            items.append([product_name, rating, rating_count, price, product_url])
        except AttributeError:
            continue
    
#sonuçları dataFrame'e aktarmak için
df = pd.DataFrame(items, columns=['product', 'rating', 'rating count', 'price', 'product url'])
df.to_csv('search_query.csv', index=False)

print(search_query)
print(df)
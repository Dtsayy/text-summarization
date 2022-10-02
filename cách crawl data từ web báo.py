import requests
from bs4 import BeautifulSoup
import pandas as pd

res = requests.get('https://tuoitre.vn/tin-moi-nhat.htm')
objBTFS = BeautifulSoup(res.text, 'html.parser')
#print(objBTFS)
# tìm đến tag_a tại thẻ a có id là như v
#tag_a = objBTFS.find('a', attrs={'data-id': '20220421102822161'})
#print(tag_a.get_text())

# tìm số lượng lớn
tag_pa = objBTFS.find('ul', attrs={'class': 'list-news-content'})
#print(tag_pa.get_text())
tag_li = tag_pa.find_all('li')
results = []
#catogory = []
#title = []
#description = []
#print(len(tag_li))
for tag_li_item in tag_li:
    tag_a_cat = tag_li_item.find('a', attrs={'class': 'category-name fl mgl10 mgb4 uppercase'})
    tag_a = tag_li_item.find('h3').a
    tag_p = tag_li_item.find('p')
    tag_img = tag_li_item.find('img')

    # lấy link bài viết
    link = tag_li_item.find('a').get('href')
    news_response = requests.get('https://tuoitre.vn/' + link)
    news_data = news_response.text
    news_soup = BeautifulSoup(news_data, 'html.parser')
    #tag_st = news_soup.find_all('div', attrs={'class': 'content fck'})
    #print(tag_st)
    newsentence = []
    for new in news_soup.find('div', class_="content fck"):
        newsentence.append(new.text.strip())
        #print(new_sentence)
    #print(len(news_soup))
    #res1 = requests.get(tag_img['src'])
    #print(res1.content)
   # with open('ings/' + tag_img['src'].split('/')[-1].replace('-', ' '), 'wb') as f:
        #[-1] là chỉ lấy câu sau cùng kể từ dấu ('/')
    #    f.write(res1.content)

    collection_data = {
                       'catogory': tag_a_cat.get_text(),
                       'title': tag_a.get_text(),
                       'description': tag_p.get_text(),
                       #'image': tag_img['src']
                       'content': newsentence
                       }
    results.append(collection_data)
    #catogory.append(tag_a_cat.get_text())
    #title.append(tag_a.get_text())
    #description.append(tag_p.get_text())
#print(results)
df = pd.DataFrame(results)
df.to_csv('dataset.csv', index=False)
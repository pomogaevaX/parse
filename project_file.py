import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

cats = ['vibrators-massagers', 'vibrators']
root_url = 'https://www.pinkcherry.com'
url = f'{root_url}/collections/vibrators-massagers'
get_site_info = requests.get(url)
with open('all_parse.txt', 'w') as all_parse_file:
    all_parse_file.write(get_site_info.text)

soup = BeautifulSoup(get_site_info.text)
div_toys = soup.find_all('div', {'class': 'item_list_container'})


def parse_div(div):
    who = ['man', 'men', 'boy', 'male', 'female', 'girl', 'woman', 'women', 'trans', 'couple']
    what = ['sex', 'masturbation', 'massage', 'solo', 'shared', 'sensual']
    toy_name = ''
    rating = 0
    toy_link = ''
    for_who = []
    for_what = []

    toy_div = div.find('div', {'class': 'product-info'})
    toy_name = toy_div.find('span', {'class': 'product-name'}).find('a').get('title')
    print(toy_name)
    toy_link = root_url + (toy_div.find('span', {'class': 'product-name'}).find('a').get('href'))
    print(toy_link)
    rating = len(toy_div.find_all('span', {'class': 'star empty-star full-star'}))
    print(rating)
    toy_page = requests.get(toy_link)
    toy_description_soup = BeautifulSoup(toy_page.text)

    def descript_func(page):
        description_span = page.find('span', {'class': 'short-description'})
        description_span = str(description_span)
        for a in who:
            if a in description_span:
                for_who.append(a)

        for b in what:
            if b in description_span:
                for_what.append(b)
        print(f'It is suitable for {for_what}. {for_who} can use it.')

    descript_func(toy_description_soup)
    return [toy_name, toy_link, rating, for_who, for_what]


res = pd.DataFrame()

for i in div_toys:
    # print(i)
    data = parse_div(i)
    print(data)
    res = res.append(pd.DataFrame([data],
                                  columns=['Name', 'Link', 'Rating', 'For who', 'For what']), ignore_index=True)

res.to_excel('result_table.xlsx')

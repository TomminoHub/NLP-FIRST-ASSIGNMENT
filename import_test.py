import os
import requests
from bs4 import BeautifulSoup


#import some medical texts and some non-medical texts
call_count = 100

def get_page_text(title ):
    global call_count
    if call_count == 0:
        return
    call_count -= 1
    
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "parse",
        "page": title,
        "format": "json",
        "prop": "text",
        "redirects": ""
    }

    response = requests.get(url, params=params)
    data = response.json()

    raw_html = data['parse']['text']['*']
    soup = BeautifulSoup(raw_html, 'html.parser')
    text = ''

    for p in soup.find_all('p'):
        text += p.text

    
    return text

def get_wikipedia_pages(category_name, max_call ):
    global call_count
    if call_count == 0:
        return
    url = "https://en.wikipedia.org/w/api.php"
    params_category = {
      "action": "query",
      "list": "categorymembers",
      "cmtitle": f"{category_name}",
      "format": "json",
      "cmlimit": 500, 
      "cmtype": "page|subcat"  
    }

    response_category = requests.get(url, params=params_category)
    data_category = response_category.json()
    

    page_titles = [page["title"] for page in data_category["query"]["categorymembers"] if page["ns"] == 0]

    subcategories = [page["title"] for page in data_category["query"]["categorymembers"] if page["ns"] == 14]
    
    for title in page_titles:
        if '/' in title or '\ ' in title:
            continue
        if call_count > 0:
            page_text = get_page_text(title )
            with open(f'testi_da_classificare\{title}.txt', 'w', encoding='utf-8') as file:
                file.write(page_text)


    for subcategory in subcategories:
        if call_count > 0:
            get_wikipedia_pages(subcategory, max_call)


get_wikipedia_pages('Category:Heart diseases' , 200)
file_list_positive = os.listdir('testi_da_classificare')
gold_positive = [1] * len(file_list_positive)
print(len(gold_positive))
call_count = 100
get_wikipedia_pages('Category:House types' , 200)
file_list_negative = os.listdir('testi_da_classificare')
gold_negative = [0] * (len(file_list_negative) - len(gold_positive))

gold_labels = gold_positive + gold_negative

with open('goldlabels.txt', 'w', encoding='utf-8') as file:
    for elemento in gold_labels:
        file.write(str(elemento) + '\n')

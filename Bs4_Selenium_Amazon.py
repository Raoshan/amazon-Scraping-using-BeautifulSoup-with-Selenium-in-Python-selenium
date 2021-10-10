import csv
from bs4 import BeautifulSoup
from selenium import webdriver

def get_url(search_term):
    """Generate a url from search term"""
    template = 'https://www.amazon.in/s?k={}&ref=nb_sb_noss_2' 
    # https://www.amazon.in/s?k=laptop&ref=nb_sb_noss_2
    search_term = search_term.replace(' ', '+')
    # add term query to url
    url = template.format(search_term)
    # add page query placeholder
    url+= '&page{}'
    return url  

def extract_record(item):
    '''Extract and return data from a singal record'''
    atag = item.h2.a
    Description = atag.text.strip()
    # print(description)
    Url = 'https://www.amazon.in'+atag.get('href')
    # print(product_link)
    try:
        Price = item.find('span', 'a-price').find('span', 'a-offscreen').text
        # print(price)
    except AttributeError:
        return
    try:
        # rank and rating
        Rating = item.i.text
        # print(ratings)
        ReviewCount = item.find('span', {'class':'a-size-base'}).text
        # print(review_count)
    except AttributeError:
        return
    result = (Description, Price, Rating, ReviewCount, Url) 
    return result  

def main(search_term):
    driver = webdriver.Chrome(executable_path=r"F:\\driver\\chromedriver.exe")
    driver.maximize_window()
    # print(driver)
    records = []
    url = get_url(search_term)    

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('div', {'data-component-type':'s-search-result'})
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
    driver.close()

    with open('amazon.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow({'Description', 'Price', 'Rating', 'ReviewCount', 'Url'})
        writer.writerows(records)


main('laptop')


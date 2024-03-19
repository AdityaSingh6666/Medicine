from  bs4 import BeautifulSoup
import requests
import pandas as pd
import time

def get_name(soup):
    try:
        name = new_soup.find(class_ = "E_ D_ bJ").text.strip()
    except AttributeError:
        name = " "
    return name

def get_comp(soup):
    try:
        comp = new_soup.find("div", class_ ="JT KT").text.strip()
    except AttributeError:
        comp = " "
    return comp

def get_manufacturer(soup):
    try:        
        manufacture_name  = new_soup.find_all("div", class_ ="JT")[1].text.strip()
    except AttributeError:
        manufacture_name = " "
    return manufacture_name

def get_expiry(soup):
    try: 
        expiry_date  = new_soup.find_all("div", class_ ="JT")[4].text.strip()
    except AttributeError:
        expiry_date = " "
    return expiry_date

# def get_availability(soup):
#     try:
#         availability = new_soup.find("div", class_ = "sP").text.strip()
#         if availability == "Delivery By":
#             return True
#         else:
#             return False     
#     except AttributeError:
#         return False
    
# def get_price(soup):  
#     price_tag = soup.find('div', class_ = "ProductCard_productDetails__JB0I6")
#     price = price_tag.text
#     print(price)


if __name__ == "__main__":
    URL = 'https://www.apollopharmacy.in/search-medicines/Azithromycin'

    # Headers for Request
    HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36','Accept-Language' : 'en-US en;q=0.5'})


    d = {"Name": [], "Composition": [], "Manufacturer": [], "Expiry": [],"Price": []}
    # "Availability": [], "Price": []}

    count = 0
    for page_num in range(1,6):
        page_url = f"{URL}?page={page_num}"
        webpage = requests.get(URL, headers=HEADERS)
        soup = BeautifulSoup(webpage.content , "html.parser")

        links = soup.find_all("a", class_="ProductCard_proDesMain__58sO_")
        links_list = []

        for link in links:    
            link = links_list.append(link.get("href"))

        for link in links_list:
            new_webpage =  requests.get("https://apollopharmacy.in" + link , headers=HEADERS)

            new_soup = BeautifulSoup(new_webpage.content , "html.parser")

            d['Name'].append(get_name(new_soup))
            d['Composition'].append(get_comp(new_soup))
            d['Manufacturer'].append(get_manufacturer(new_soup))
            d['Expiry'].append(get_expiry(new_soup))
            # d['Availability'].append(get_availability(new_soup))
            # d['Price'].append(get_price(new_soup))

            count += 1
            
            if count == 70:
                break

            time.sleep(1)

        if count == 70:
            break
        
    medicine_df = pd.DataFrame.from_dict(d)
    medicine_df.replace({"Name" : " "}, inplace = True)
    medicine_df = medicine_df.dropna(subset=['Name'])
    medicine_df.to_csv("medicine_data.csv",header=True, index=False)

    print(medicine_df)
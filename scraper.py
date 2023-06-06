""" Script for webscraping icecream flavours
"""
import bs4
import requests

BASE_URL="https://gelatomessina.com"

def main():
    sections=[
        ('','icecream_all'),
        ('/Vegan', 'icecream_vegan'),
        ('/Alcohol-Free', 'icecream_alcohol_free'),
        ('/Egg-Free', 'icecream_egg_free'),
        ('/Gluten-Free', 'icecream_gluten_free'),
        ('/Nut-Free', 'icecream_nut_free'),
    ]

    for section in sections:
        these_flavours=get_flavours_through_pagination('/collections/classic-flavours'+section[0])
        export_to_file(section[1],these_flavours)        

def export_to_file(file_name, flavours):
    with open(file_name+'.txt', 'w') as f:
        for flavour in flavours:
            f.write(flavour)
            f.write("\n")    

def get_flavours_through_pagination(url_end):
    next=(True, url_end)
    flavours_collected=[]
    while True:
        full_url=BASE_URL+next[1]
        response =requests.get(full_url)
        flavours=get_flavours(response)
        flavours_collected.extend(flavours)
        next=get_next_pagination_href(full_url)
        print("next is ", next)
        if next[0] == False:
            print("finished!")
            break
    return flavours_collected


def get_next_pagination_href(base_url):
    """ Returns a tuple with a boolean and the href if present

    If boolean True -> there is a next page, and the second element is the link

    """
    response =requests.get(base_url)
    soup = bs4.BeautifulSoup(response.content,"lxml")
    ul=soup.find('ul',{"class":"pagination flex items-center"})  
    if ul is not None:
        for element in ul.children:
            try:
                anchor=element.find("a")
                span=anchor.find("span")
                if "Next" in span.text:
                    return (True, anchor['href']) 
            except:
                pass
    return (False, None)


def get_flavours(response):
    """Extracts the flavour names from a page and returns them in a list
    """
    soup = bs4.BeautifulSoup(response.content,"lxml")
    divs=soup.find_all('a',{"class":"increase-target"})
    flavours=[]
    for div in divs:
        span=div.find("span")
        flavours.append(span.text)
    return flavours

if __name__ == "__main__":
    main()
# Icecream web scraper

Web scraper for downloading lists of icecream flavours through site pagination.

I created this web scraper to have data to practice in my [PostgreSQL Database Design Exercise](https://github.com/lmponcio/postgresql-icecream-db).

Something to note in this project: I figured a way to navigate through pagination (sending a request for each "Next" button found):
```python
# scraper.py
# ...
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
# ...
```
The `url_end` variable contains the last part of the url of the next page I need to navigate to. After the first loop, this information is extracted from the `href` attribute of the anchor in the "Next" web page button (if present).

```python
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
```
When the "Next" button can't be found, the script will not try to send a new request for that section (tuple with `False` as first item is returned).

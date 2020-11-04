import FileIO 
import requests
from bs4 import BeautifulSoup
import Sahbndnİlan
headers=''
url="https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?pagingSize=50"
headers = { 
    'Accept': '*/*',
    'Host': 'www.sahibinden.com',       
    'User-Agent': 'aaaaaaaaaaaaaaaaaaaa'
    }
        
'''
ilan sonuçları:
    ilan: <tr data-id

'''
### Queries ###
lastXdays = lambda a : "date="+a + "days" # date=30days
getOffset = lambda pageNumb: "pagingOffset=" + str(pageNumb * 50)  #pagingOffset=950

r = requests.get(url,headers=headers, timeout=None)
FileIO.saveResponse("bepsi.html",r.text)
print( 'get: ', r.status_code)

soup = BeautifulSoup(r.text, 'html.parser')
links= soup.find_all("tr")

###TODO: find count of listings
listings=(x for x in links if x.has_attr("data-id"))
#count= sum(1 for x in listings)
#print(count)

#e: her bir ilan elementi, data-id attr'sine sahip her bir tr
for e in listings:
    id= e.get("data-id")    #listing id
    url = e.find('td',class_="searchResultsLargeThumbnail").find("a").get("href") #link
    title=e.find('td',class_="searchResultsLargeThumbnail").find("a").get("title") #title
   
    brand= e.find_all('td',class_="searchResultsTagAttributeValue")[0].get_text()  #brand: apple
    model = e.find_all('td',class_="searchResultsTagAttributeValue")[1].get_text()  #model: iphone 7 plus

    price= e.find('td',class_="searchResultsPriceValue").div.get_text()    #price

    date1= e.find('td',class_="searchResultsDateValue").find_all("span")[0].get_text() #4 kasım
    date2=e.find('td',class_="searchResultsDateValue").find_all("span")[1].get_text() #2020
    for i,text in enumerate(e.find('td',class_="searchResultsLocationValue").stripped_strings): #ilki il, ikincisi ilçe
        city= text if i == 0 else "null"
        town = text if i==1  else "null"

    ilan= Sahbndnİlan.Shbndnİlan(url,price,date1+" "+date2,id,brand,model,title=title,city=city,town=town)
    ilan.print()
print(31)

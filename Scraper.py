import FileIO 
import requests
from bs4 import BeautifulSoup
import Sahbndnİlan
import sys
from io import StringIO
#utils
def stdoutToStr(ilan):
    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout
    
    ilan.print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output


#Request style: host + relative url + queries
#ilk requeest manual olmalı
url="https://www.sahibinden.com"
#url="https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?pagingSize=50"
headers = { 
    'Accept': '*/*',
    'Host': 'www.sahibinden.com',      
    'Connection': 'keep-alive', 
    'X-Requested-With':'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.317'
    }
        
'''
ilan sonuçları:
    ilan: <tr data-id

'''
### Request Queries ###
lastXdays = lambda a : "date="+a + "days" # date=30days
getOffset = lambda pageNumb: "pagingOffset=" + str(pageNumb * 50)  #pagingOffset=950
###
s = requests.Session()
r = s.get(url +"/cep-telefonu-modeller/ikinci-el?" +"pagingSize=50",headers=headers, timeout=None)
print( 'get: ', r.status_code)
soup = BeautifulSoup(r.text, 'html.parser')
pageCount= int(soup.find("p", class_="mbdef").text.split()[1].replace(".",""))
FileIO.saveResponse("bepsi.html",r.text)

nextPageUrl="/cep-telefonu-modeller/ikinci-el?pagingSize=50"

i=0
while i<pageCount:
    r = s.get(url+"/cep-telefonu-modeller/ikinci-el?pagingSize=50"+"&" +getOffset(i),headers=headers, timeout=None)
    #FileIO.saveResponse("bepsi.html",r.text)
    print( 'get: ', r.status_code)
    i+=1
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.url, i,getOffset(i))
    #nextPageUrl=soup.find(lambda btn:btn.name=="a" and "Sonraki" in btn.text).get("href")
    #print(nextPageUrl)
    
    links= soup.find_all("tr")
    
    ###TODO: find count of listings
    #listings=(x for x in links if x.has_attr("data-id"))
    #count= sum(1 for x in listings)
    #print(count)
    
    #e: her bir ilan elementi, data-id attr'sine sahip her bir <tr>
    for e in links:
        if e.has_attr("data-id") is not True: continue
        id= e.get("data-id")    #listing id
        listingUrl = e.find('td',class_="searchResultsLargeThumbnail").find("a").get("href") #link
        title=e.find('td',class_="searchResultsLargeThumbnail").find("a").get("title") #title
    
        brand= e.find_all('td',class_="searchResultsTagAttributeValue")[0].get_text()  #brand: apple
        model = e.find_all('td',class_="searchResultsTagAttributeValue")[1].get_text()  #model: iphone 7 plus

        price= e.find('td',class_="searchResultsPriceValue").div.get_text()    #price

        date1= e.find('td',class_="searchResultsDateValue").find_all("span")[0].get_text() #4 kasım
        date2=e.find('td',class_="searchResultsDateValue").find_all("span")[1].get_text() #2020
        for j,text in enumerate(e.find('td',class_="searchResultsLocationValue").stripped_strings): #ilki il, ikincisi ilçe
            city= text if j == 0 else "null"
            town = text if j==1  else "null"

        ilan= Sahbndnİlan.Shbndnİlan(listingUrl,price,date1+" "+date2,id,brand,model,title=title,city=city,town=town)
        #ilan.print()
        file=open("ekmek.txt","a", encoding="utf8")
        file.write(ilan.listingId+"\n")
        file.close()  
    
    if(i==20 ):
        file=open("ekmek.txt","a", encoding="utf8")
        file.write( "\n\n\n\n 20. SAYFANIN SONUĞ \n\n\n\n")
        file.close()  
 


print(31)

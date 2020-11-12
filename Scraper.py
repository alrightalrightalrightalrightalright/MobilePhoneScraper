import FileIO 
import requests
from bs4 import BeautifulSoup
import Sahbndnİlan
import sys
import _thread
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


### Request Queries ###
lastXdays = lambda a : "date="+a + "days" # date=30days
getOffset = lambda pageNumb: "pagingOffset=" + str(pageNumb * 50)  #pagingOffset=950
###
class Scraper:
    #Request kullanımı: host + relative url + ek queries
    baseUrl="https://www.sahibinden.com" #url="https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?pagingSize=50"
    listingUrl="/ilan/ikinci-el-ve-sifir-alisveris-cep-telefonu-modeller-"
    requestUrl=""
    headers = { 
        'Accept': '*/*',
        'Host': 'www.sahibinden.com',      
        'Connection': 'keep-alive', 
        'X-Requested-With':'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.317'
        }
    


    def __init__(self):
        s=self.s = requests.Session()
        r=self.r = s.get(self.baseUrl +"/cep-telefonu-modeller/ikinci-el?pagingSize=50"+"&sorting=date_desc",headers=self.headers, timeout=None)
        self.s.headers=self.headers
        print( 'get: ', r.status_code)
        soup=self.soup = BeautifulSoup(r.text, 'html.parser')

        self.pageCount= int(soup.find("p", class_="mbdef").text.split()[1].replace(".",""))
        self.listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        

    def crawl(self, soup,level=0):
        listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        if listingCount<=1000 or len(soup.find("div",id="searchCategoryContainer").find_all("li"))==0 :
            self.scrape(soup,level)
            #_thread.start_new_thread( self.scrape,(soup,level) )
            return

        subCategs=soup.find("div",id="searchCategoryContainer").find_all("li")#phone models
        for phoneModel in subCategs:
            self.requestUrl=phoneModel.a.get("href")
            r = self.s.get(self.baseUrl +self.requestUrl ,headers=self.headers, timeout=None)
            print(level*"\t"+ 'crawling: ', phoneModel.text.replace("\n",""), " with url:",phoneModel.a.get("href"))
            soup = BeautifulSoup(r.text, 'html.parser')
            self.crawl(soup,level+1)
            print(level*"\t"+ 'crawling done for: ', phoneModel.text.replace("\n",""))

    #FileIO.saveResponse("bepsi.html",r.text)

    def scrape(self, soup,level=0): 
             
        listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        pageCount= 20 if int(listingCount)//50 >=20 else int(listingCount)//50 #çünkü az ilanlı kategoride sonraki sayfa butonları yok      
        i=0
        while i<=pageCount:
            r = self.s.get(self.baseUrl+self.requestUrl+"&" +getOffset(i),headers=self.headers, timeout=None)
            print(level*"\t"+"scraping page: ",str(i)+ "/"+str(pageCount))  
            #FileIO.saveResponse("bepsi.html",r.text)
            i+=1
            soup = BeautifulSoup(r.text, 'html.parser')
            #nextPageUrl=soup.find(lambda btn:btn.name=="a" and "Sonraki" in btn.text).get("href")
            #print(nextPageUrl)
            
            links= soup.find_all("tr")
            
            ###TODO: find count of listings
            #listings=(x for x in links if x.has_attr("data-id"))
            #count= sum(1 for x in listings)
            #print(count)
            file=open("ekmek.txt","a", encoding="utf8")
            #e: her bir ilan elementi, data-id attr'sine sahip her bir <tr>
            for e in links:
                if e.has_attr("data-id") is not True: continue
                id= e.get("data-id")    #listing id
                listingUrl = e.find('td',class_="searchResultsLargeThumbnail").find("a").get("href") #link
                title=e.find('td',class_="searchResultsLargeThumbnail").find("a").get("title") #title

                #yaprak üzerinde scrape
                if len(e.find_all('td',class_="searchResultsTagAttributeValue")) ==0: #model üzerinden scrape yapılıyorsa: ...>apple>iphone 3g
                    model =soup.find("li",class_="breadcrumbItem leaf").span.text
                    brand=soup.find("li",class_="breadcrumbItem leaf").find_previous("li").span.text
                else:
                    brand =soup.find("li",class_="breadcrumbItem leaf").span.text
                    model = e.find_all('td',class_="searchResultsTagAttributeValue")[0].get_text()  #model: iphone 7 plus

                price= e.find('td',class_="searchResultsPriceValue").div.get_text()    #price

                date1= e.find('td',class_="searchResultsDateValue").find_all("span")[0].get_text() #4 kasım
                date2=e.find('td',class_="searchResultsDateValue").find_all("span")[1].get_text() #2020
                for j,text in enumerate(e.find('td',class_="searchResultsLocationValue").stripped_strings): #ilki il, ikincisi ilçe
                    city= text if j == 0 else "null"
                    town = text if j==1  else "null"

                ilan= Sahbndnİlan.Shbndnİlan(listingUrl,price,date1+" "+date2,id,brand,model,title=title,city=city,town=town)
                #ilan.print()
                
                file.write(ilan.listingId+"\n")
                
            file.close()  

    def deepScrape(self,id):
        r = self.s.get(self.baseUrl+self.listingUrl+id+ "/detay",headers=self.headers, timeout=None)
        print("page: ",r.status_code)  
        soup = BeautifulSoup(r.text, 'html.parser')
        info= soup.find("div",class_="classifiedInfo")

        infoList=info.find("ul",class_="classifiedInfoList").find_all("li")
        price=info.find("h3").text.split(" ")[17] #HARDCODED. !!!
        location="".join(info.find("h2").text.split())
        
        listingDate=" ".join(infoList[1].span.text.split(" ")[16:])
        brand=infoList[2].span.text.replace("\xa0","")
        model=infoList[3].span.text.replace("\xa0","")
        os=infoList[4].span.text.split("\t")[1]
        internalMem=infoList[5].text.split("\t")[1].split()[0]
        screenSize=infoList[6].text.split()[2]
        ramMem=infoList[7].text.split()[2]#gb#'501 MB - 1 GB\n' wtf
        camRes=infoList[8].text.split()[1]#mp
        frontCamRes=infoList[9].text.split()[2]
        color=infoList[10].text.split()[1]
        guarantee=" ".join(infoList[11].text.split()[1:])
        seller=infoList[12].text.split()[1]
        usedStatus=" ".join(infoList[14].text.split()[1:])


        x=2
        

    def lightScrape(self):
        self.crawl(self.soup)



bepsi=Scraper()
#bepsi.crawl(bepsi.soup)
file=open("ekmek.txt","r")
laynsss=file.readlines()
for ln in laynsss:
    bepsi.deepScrape(ln.replace("\n",""))







print("HÜAĞHÜAEÇHEAĞHĞAEHÇAEĞH")



import FileIO 
import requests
from bs4 import BeautifulSoup
import Sahbndnİlan
import sys
import _thread
from io import StringIO
import Firebase
import backoff
import random
import time
#utils
def stdoutToStr(ilan):
    old_stdout = sys.stdout
    new_stdout = StringIO()
    sys.stdout = new_stdout
    
    ilan.print()

    output = new_stdout.getvalue()
    sys.stdout = old_stdout

    return output
randWait= lambda : time.sleep( random.randrange(800,2000)/1000)

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
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        'Host': 'www.sahibinden.com',      
        'Connection': 'keep-alive', 
        "Upgrade-Insecure-Requests": "1",
        'X-Requested-With':'XMLHttpRequest',
        "Cache-Control":"max-age=0",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 OPR/71.0.3770.441"
        }
    frbs=Firebase.Firebase()
    
    def _scrapeListing(self,soup, e):
        """Smallest scraping work, scrapes all the listings in the web page and returns its data as object
        :param soup: bs4 soup of webpage that contains many listings.
        :param e: each listing element. some data scraped from breadcrumb bar thats why there is also soup param."""
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
        return ilan

    def __init__(self):
        s=self.s = requests.Session()
        self.s.headers=self.headers
        r=self.r = s.get(self.baseUrl +"/cep-telefonu-modeller/ikinci-el?pagingSize=50"+"&sorting=date_desc", timeout=None) 
        print( 'get: ', r.status_code)
        soup=self.soup = BeautifulSoup(r.text, 'html.parser')


        self.subCategs=soup.find("div",id="searchCategoryContainer").find_all("li")#phone models
        self.pageCount= int(soup.find("p", class_="mbdef").text.split()[1].replace(".",""))
        self.listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        
    @backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException,
                      requests.exceptions.MissingSchema)
    def crawl(self, soup,level=0):
        """Scrapes whole mobile phone listings in website. So that website has
        multiple categories with sub-categories itself, a recursive scraping method 
        that works like a crawler is required to do this job.  

        :param soup: bs4 soup of the webpage with all the main categories itself.
        :param level: recursion level.
        """
        listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        if listingCount<=1000 or len(soup.find("div",id="searchCategoryContainer").find_all("li"))==0 :
            self.scrape(soup,level)
            #_thread.start_new_thread( self.scrape,(soup,level) )
            return
        random.shuffle(self.subCategs)    
        for phoneModel in self.subCategs:
            self.requestUrl=phoneModel.a.get("href")
            self.s.headers.update({'Referer': self.r.url})
            r = self.s.get(self.baseUrl +self.requestUrl , timeout=None)
            print(level*"\t"+ 'crawling: ', phoneModel.text.replace("\n",""), " with url:",phoneModel.a.get("href"))
            soup = BeautifulSoup(r.text, 'html.parser')
            self.crawl(soup,level+1)
            #time.sleep(60)
            print(level*"\t"+ 'crawling done for: ', phoneModel.text.replace("\n",""))


    def scrape(self, soup,level=0): 
        #time.sleep(32)
        """Does the scraping job where the webpage has listings.

        :param soup: bs4 soup of the webpage to be scraped.
        :param level: since the scraping process used in crawling, level specifies the recursion level 
        of the crawling process. it is used in printing or visualising.
        """
        listingCount=int(soup.find("div", class_="result-text").find_all("span")[1].text.split()[0].replace(".",""))
        pageCount= 20 if int(listingCount)//50 >=20 else int(listingCount)//50 #çünkü az ilanlı kategoride sonraki sayfa butonları yok      
        i=0
        while i<=1:#i<=pageCount
            randWait()    
            self.s.headers.update({'Referer': self.r.url})    
            r = self.s.get(self.baseUrl+self.requestUrl+"&" +getOffset(i),timeout=None)
            print(level*"\t"+"scraping page: ",str(i)+ "/"+str(pageCount))  
            #FileIO.saveResponse("bepsi.html",r.text)
            i+=1
            soup = BeautifulSoup(r.text, 'html.parser')
            #nextPageUrl=soup.find(lambda btn:btn.name=="a" and "Sonraki" in btn.text).get("href")
            
            links= soup.find_all("tr")
            
            file=open("aekmek.txt","a", encoding="utf8")
            #e: her bir ilan elementi, data-id attr'sine sahip her bir <tr>
            random.shuffle(links)
            for i,e in enumerate (links):
                if i >=random.randrange(3,9): return
                if e.has_attr("data-id") is not True: continue
                ilan=self._scrapeListing(soup,e)
                if self.frbs.isExists(ilan.listingId) is True: continue
                randWait()
                self.deepScrape(ilan)
                #ilan.print()
                self.frbs.AddListing(ilan)
                file.write(ilan.getCSV()+"\n")
                
            file.close()  

    def deepScrape(self,ilan):
        #time.sleep(32)
        """Scrapes a listing form its listing page. it requests the listing with id parameter
        then scrapes its data.
        :param id: listing id"""
        r = self.s.get(self.baseUrl+self.listingUrl+ilan.listingId+ "/detay",headers=self.headers, timeout=None)
        print("page: ",r.status_code)  
        if r.status_code == 429: raise requests.exceptions.MissingSchema
        if r.status_code == 410: return
        soup = BeautifulSoup(r.text, 'html.parser')
        info= soup.find("div",class_="classifiedInfo")
    
        infoList=info.find("ul",class_="classifiedInfoList").find_all("li")
    
        #data= {x: -1 for x in self.fields}
        for inf in infoList:
            for field in ilan.fields:
                if inf.text.find(field) == -1 :continue
                ilan.data[field]=" ".join(inf.text.split("\xa0")[1].split())
        print(ilan.data)
        return

        ilan.price= info.find("h3").text.split(" ")[17] #HARDCODED. !!!
        ilan.city="".join(info.find("h2").text.split()[0])
        #ilan.town="".join(info.find("h2").text.split()[2])
        ilan.listingDate =" ".join(infoList[1].span.text.split(" ")[16:])
        ilan.brand=infoList[2].span.text.replace("\xa0","")
        ilan.model=infoList[3].span.text.replace("\xa0","")
        ilan.os=infoList[4].span.text.split("\t")[1]

        #TODO: fix interval values like 501mb-1gb
        takozmu = True if infoList[5].text.find("Dahili Hafıza") ==-1 else False
        ilan.internalMem= infoList[5].text.split("\t")[1].split()[0]
        ilan.screenSize=infoList[6].text.split()[2]

        #4 durum: 15gb, 256mb, 510mb- 2 gb, yok
        ramText=" ".join(infoList[7].text.split())#kamera 1mb ve altı
        ramUnitMultiplier=1 if ramText.split()[2]=="Yok" or ramText.split()[3]=="MB" else  1024
        ramSize= 0 if ramText.find("Yok") != -1 else int(ramText.split()[2])*ramUnitMultiplier
        ilan.ram= ramSize

        ilan.cameraRes=infoList[8].text.split()[1]#mp
        ilan.frontCamRes=infoList[9].text.split()[2]
        ilan.color=infoList[10].text.split()[1]
        ilan.warrantyStatus=" ".join(infoList[11].text.split()[1:])
        ilan.fromWho=infoList[12].text.split()[1]
        #ilan.usedStatus=" ".join(infoList[14].text.split()[1:]) no need


        

    def lightScrape(self):
        self.crawl(self.soup)



bepsi=Scraper()

bepsi.crawl(bepsi.soup)







print("HÜAĞHÜAEÇHEAĞHĞAEHÇAEĞH")



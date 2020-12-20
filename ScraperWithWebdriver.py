from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import Firebase
import sys
import time
import Sahbndnİlan
import winsound
import FileIO

#############config#######################################################################:
scrapeLink="https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?date=1day&pagingSize=50&sorting=date_desc"
headlessMode=False
chromeDriverPath="./chromedriver.exe"
listingsToScrapePerPage=50            
pagesToScrape=20
##########################################################################################
#TODO: TIKLANMIŞ LİNKLERİ NEXTLE
#TODO: ilanların bulunduğu sayfada id alıp firebasede kontrol ettikten sonra 
#TOFIX: alt kategori seçerken yukarıdaki bi ilana yapılan hover
#sonucu elementin yarısı gözüküyor, tıkalyamıyor. other element woul
#receive the ciclk, ElementClickInterceptedException


randWait= lambda : time.sleep( random.randrange(800,3500)/1000)


def closeTab(driver):
    oldHandle= driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(oldHandle)

def kanser():
    frequency = 5000  
    duration = 1000  
    winsound.Beep(frequency, duration)
    for i in range(0,1000):
        winsound.Beep(frequency, duration)


def hoverOn(element, driver):
    ActionChains(driver).move_to_element(element).perform()

def click(element,driver):
    driver.execute_script("window.scrollTo(0, 0)") 
    driver.execute_script("window.scrollTo(0, 180)") 
    hoverOn(element,driver)
    driver.execute_script("window.scrollTo(0, 180)") 
    i=0
    while True:
        try:         
            element.click()
            return    
        except Exception:
            drag= driver.find_element_by_xpath('//*[@id="searchCategoryContainer"]')
            if i<2:
                drag.send_keys(Keys.DOWN)
                i=i+1
            elif i>=2:
                drag.send_keys(Keys.UP)          
                i=i+1
            else:
                print("hizbullah <3")
        
    element.click()
    #ElementClickInterceptedException AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

#get page component
def getListingCountFromPage(driver):
    return int(driver.find_element_by_xpath('//div[@class="result-text"]/span').text.split()[0].replace(".",""))

def getListingCount(element):
    return int(element.find_element_by_tag_name("span").text.replace("(","").replace(")",""))

def getSubCategs(driver):
    categs= driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li") 
    random.shuffle(categs)
    return  categs

def getCategByIndex(i,driver):
    for j,categ in enumerate (getSubCategs(driver),start=0):    
        if i == j : 
            #driver.execute_script('var topPos=document.getElementsByClassName("cl")['+str(i)+'].offsetTop;document.getElementsByClassName("jspContainer")[0].scrollTop=topPos-10;') 
            ActionChains(driver).move_to_element(categ).perform()
            driver.execute_script("window.scrollTo(0, 180)") 
            return categ

def getPrice(driver):
    fiyat=-1
    try:#get kapalı ilanlarda
        fiyat= driver.find_element_by_xpath('//*[@class="classifiedInfo "]/h3').text.split()[0]
    except NoSuchElementException:
        fiyat= driver.find_element_by_xpath('//*[@class="price-value "]').text.split()[0]
        driver.execute_script("window.scrollTo(0, 240)") 
    finally:
        return fiyat

#scraping        #driver.find_element_by_xpath('//*[@class="statusMessage"]')   

def scrapeListing(driver):
    start_time = time.time()

    driver.execute_script("window.scrollTo(0, 102)") 
    driver.execute_script("window.scrollTo(0, 120)") 
    try:      
        infoList =driver.find_elements_by_xpath('//*[@class="classifiedInfoList"]/li')
        infoList.pop()  #last element is empty: ""
        ilan= Sahbndnİlan.Shbndnİlan()
        ilan.data["Fiyat"] = getPrice(driver)
        for inf in infoList:
            key=inf.text.split("\n")[0]
            val= inf.text.split("\n")[1].strip()
            ilan.data[key]=val
        print(ilan.data)
        print("--- %s seconds ---" % (time.time() - start_time))
        frbs.AddListing(ilan)
        return
    except IndexError as ex:
        print("hata geldi ama korkma. büyük ihtimal olağan bir hata:",ex)
        return
    except BaseException as ex:
        print("eywah hata bune yaw:",ex)
        FileIO.dosyayaYaz("hata.txt", Firebase.getTime()+ str(ex) +"\n")
        return

def checkIfExists(driver):
    return
    
def travelPages(driver):
    '''travels all the available listing pages one by one.'''
    try:
        i=0
        while True:
            try:
                nextpageBtn = driver.find_element_by_xpath('//a[@title="Sonraki"]')#NoSuchElementException
            except NoSuchElementException :
                nextpageBtn= None
            except Exception:
                print("yeah reall kill yourself")
                nextpageBtn= None
            except BaseException :
                print("suicide")
                nextpageBtn= None
            listings = driver.find_elements_by_xpath('//*[@id="searchResultsTable"]/tbody/tr[@data-id]')
            random.shuffle(listings)
            for j,e in enumerate (listings):
                ActionChains(driver).move_to_element(e).perform()#eski hoveron
                link=e.find_element_by_tag_name("a").get_attribute("href")
                print(link)
                #TIKLANMIŞ LİNK KONTROL
                #listingId=link.split("-")[len(link.split("-"))-1].split("/")[0]
                #if frbs.isExists(listingId): continue
                #checkIfExists(driver)

                oldHandle= driver.current_window_handle
                driver.execute_script("window.open('"+ link+  "');")
                driver.switch_to.window(driver.window_handles[1])
                scrapeListing(driver)
                
                driver.close()
                driver.switch_to.window(oldHandle)##???? gerekli mi
                if j >= listingsToScrapePerPage: break

            i=i+1
            if nextpageBtn is None or i >pagesToScrape: return
            driver.execute_script("arguments[0].click();", nextpageBtn) 
            WebDriverWait(driver, 10).until(EC.staleness_of(nextpageBtn))
            
    except Exception as ex:
        print("amanın. kritik hata.", str(ex))
        FileIO.dosyayaYaz("hata.txt", Firebase.getTime()+ str(ex) +"\n")
        #raise ex
        

#page navigation
def backOneLevel(driver):
    #TODO: fix this with decorator
    firstElement=driver.find_element_by_xpath('//*[@class="searchResultsItem     "]')
    driver.execute_script("window.scrollTo(0, 0)") 
    if len(getSubCategs(driver)) <=0:
        driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[4]/div/a').click()
    else:
        driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[3]/div/a').click()
    WebDriverWait(driver, 10).until(EC.staleness_of(firstElement))



print("ayy lmao")

frbs=Firebase.Firebase()

options = Options()
options.headless = headlessMode
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(chromeDriverPath,options=options)

driver.get(scrapeLink)

print("lesgooo")
driver.find_element_by_xpath('//*[@id="closeCookiePolicy"] ').click()


def Traverse(driver):
    randWait()
    if getListingCountFromPage(driver) <=1000 or len(getSubCategs(driver)) <=0 :
        travelPages(driver)
        backOneLevel(driver)
        return
    for i in range(0,len(getSubCategs(driver))):#layer 0: tüm ana modeller.
        categs=getSubCategs(driver)
        nextSubCat=categs[i].find_element_by_tag_name("a")
        ActionChains(driver).move_to_element(nextSubCat).perform()
        driver.execute_script("window.scrollTo(0, 180)") 
        FileIO.dosyayaYaz("categs.txt",nextSubCat.text + "\n")
        if (nextSubCat.text == "" # skip top and bottom that cant be seen because send keys
        or nextSubCat.text == "Diğer" or nextSubCat.text == "Toplu Satış"): continue 

        drag= driver.find_element_by_xpath('//*[@id="searchCategoryContainer"]')
        drag.send_keys(Keys.DOWN)
        drag.send_keys(Keys.UP)          
        firstElement=driver.find_element_by_xpath('//*[@class="searchResultsItem     "]')
        click(nextSubCat,driver)
        WebDriverWait(driver, 10).until(EC.staleness_of(firstElement))
        Traverse(driver)     

while True:  
    try:
        Traverse(driver)
    except BaseException as ex:
        FileIO.dosyayaYaz("hata.txt", Firebase.getTime()+ str(ex) +"\n")
        driver.close()
            
print("TÜM VERİLER TOPLANDI. BU ÇIKTIYI GÖRDÜYSEN HELAL.")


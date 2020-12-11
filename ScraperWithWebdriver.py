from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import random
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

import Firebase
import sys
import time
import Sahbndnİlan
randWait= lambda : time.sleep( random.randrange(800,3500)/1000)
frbs=Firebase.Firebase()


#TODO: ilanların bulunduğu sayfada id alıp firebasede kontrol ettikten sonra 
#TOFIX: alt kategori seçerken yukarıdaki bi ilana yapılan hover
#sonucu elementin yarısı gözüküyor, tıkalyamıyor. other element woul
#receive the ciclk, ElementClickInterceptedException

#tab methotd
def waitForLoad(driver):
    '''waits for next page to load'''
    oldTitle= driver.title
    while page_title_changed(oldTitle,driver) is False:pass

def page_title_changed(oldTitle,driver):
    return True if driver.title != oldTitle else False

def closeTab(driver):
    oldHandle= driver.current_window_handle
    driver.switch_to.window(driver.window_handles[1])
    driver.close()
    driver.switch_to.window(oldHandle)

def hoverOn(element, driver):
    ActionChains(driver).move_to_element(element).perform()

def click(element,driver):
    driver.execute_script("window.scrollTo(0, 0)") 
    driver.execute_script("window.scrollTo(0, 180)") 
    hoverOn(element,driver)
    #driver.execute_script("window.scrollTo(0, 0)") 
    driver.execute_script("window.scrollTo(0, 180)") 
  
    element.click()


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



#scraping
def scrapeListing(driver):
    start_time = time.time()

    driver.execute_script("window.scrollTo(0, 180)") 
    driver.execute_script("window.scrollTo(0, 190)") 

    infoList =driver.find_elements_by_xpath('//*[@class="classifiedInfoList"]/li')
    infoList.pop()  #last element is empty: ""
    ilan= Sahbndnİlan.Shbndnİlan()
    for inf in infoList:
        key=inf.text.split("\n")[0]
        val= inf.text.split("\n")[1].strip()
        ilan.data[key]=val
        #for field in ilan.fields:
    print(ilan.data)
    print("--- %s seconds ---" % (time.time() - start_time))
    frbs.AddListing(ilan)
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
            for e in listings:
                hoverOn(e,driver)
                ActionChains(driver).move_to_element(e).perform()
                link=e.find_element_by_tag_name("a").get_attribute("href")
                print(link)

                #listingId=link.split("-")[len(link.split("-"))-1].split("/")[0]
                #if frbs.isExists(listingId): continue
                #checkIfExists(driver)

                oldHandle= driver.current_window_handle
                driver.execute_script("window.open('"+ link+  "');")
                driver.switch_to.window(driver.window_handles[1])
                scrapeListing(driver)
                driver.close()
                driver.switch_to.window(oldHandle)##???? gerekli mi

            i=i+1
            if nextpageBtn is None or i >1: return
            driver.execute_script("arguments[0].click();", nextpageBtn) 
            waitForLoad(driver)
            
    except Exception as ex:
        print("amanın. kritik hata.", str(e))
        return
        raise ex

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







options = Options()
options.headless = True
options.page_load_strategy = 'eager'
driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.get("https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?date=1day&pagingSize=50")

print("ytararararararar")
driver.find_element_by_xpath('//*[@id="closeCookiePolicy"] ').click()

#subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
#def getNextCateg(driver,categ):

def hoxx(driver):
    randWait()
    if getListingCountFromPage(driver) <=1000 or len(getSubCategs(driver)) <=0 :
        travelPages(driver)
        print(driver.title + "yalandan sayfalar tarandı...")
        return
    #subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
    for i in range(0,len(getSubCategs(driver))):
    #for categ in subCategs:
        categ = getCategByIndex(i,driver)
        if categ is None or categ.text.find("Diğer") !=-1 or categ.text.find("Toplu Satış") !=-1 : 
            continue
        else:
            oldTitle=driver.title
            #driver.execute_script("arguments[0].click();",getCategByIndex(i,driver).find_element_by_tag_name("a"))
            nextSubCat=getCategByIndex(i,driver).find_element_by_tag_name("a")
            if nextSubCat.text == "" or nextSubCat.text == "Diğer" or nextSubCat.text == "Toplu Satış": continue # skip top bottom because send keys
            drag= driver.find_element_by_xpath('//*[@id="searchCategoryContainer"]')
            drag.send_keys(Keys.DOWN)
            drag.send_keys(Keys.UP)          
            firstElement=driver.find_element_by_xpath('//*[@class="searchResultsItem     "]')
            click(nextSubCat,driver)
            #WebDriverWait(driver, 10).until(lambda driver: driver.title != oldTitle)
            WebDriverWait(driver, 10).until(EC.staleness_of(firstElement))
        hoxx(driver)     
        backOneLevel(driver)
        
        #subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
hoxx(driver)

print(13)

modellerBtn=driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[3]/div/a').get_attribute("href")
subModel=driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[4]/div/a').get_attribute("href")

# TODO: ÇEREZ ÇARPIYA TIKLA


assert "No results found." not in driver.page_source
driver.close()



#middle click link driver.execute_script("window.open('"+ nextpageBtn.get_attribute('href')+  "');")

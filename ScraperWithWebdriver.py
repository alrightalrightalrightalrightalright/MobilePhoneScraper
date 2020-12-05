from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains

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

def getListingCountFromPage(driver):
    return int(driver.find_element_by_xpath('//div[@class="result-text"]/span').text.split()[0].replace(".",""))

def getListingCount(element):
    return int(element.find_element_by_tag_name("span").text.replace("(","").replace(")",""))

def travelPages(driver):
    '''travels all the available listing pages one by one.'''
    try:
        while True:
            nextpageBtn = driver.find_element_by_xpath('//a[@title="Sonraki"]')#NoSuchElementException
            listings = driver.find_elements_by_xpath('//*[@id="searchResultsTable"]/tbody/tr[@data-id]')
            for e in listings:
                print(e.find_element_by_tag_name("a").get_attribute("href"))
                #driver.execute_script("window.open('"+ e.find_element_by_tag_name("a").get_attribute("href")+  "');")
                #yalandan dataları almışız...
                #closeTab(driver)
            driver.execute_script("arguments[0].click();", nextpageBtn) 
            waitForLoad(driver)
            
    except Exception as ex:
        raise ex

def getSubCategs(driver):
    return  driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")

def backOneLevel(driver):
    #TODO: fix this with decorator
    oldTitle= driver.title   
    if len(getSubCategs(driver)) <=0:
        driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[4]/div/a').click()
    else:
        driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[3]/div/a').click()
    while page_title_changed(oldTitle,driver) is False:pass
def getCategByIndex(i,driver):
    for j,categ in enumerate (getSubCategs(driver),start=0):    
        if i == j : 
            ActionChains(driver).move_to_element(categ).perform()
            return categ

options = Options()
#options.headless = True
options.page_load_strategy = 'eager'
driver = webdriver.Chrome("./chromedriver.exe",options=options)
driver.get("https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?pagingSize=50")
print("ytararararararar")




#subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
#def getNextCateg(driver,categ):

def hoxx(driver):
    if getListingCountFromPage(driver) <=1000 or len(getSubCategs(driver)) <=0 :
        #travelPages(driver)
        print("yalandan sayfalar tarandı...")
        return
    #subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
    #categ = getNextCateg(driver,categ)
    for i in range(0,len(getSubCategs(driver))):
    #for categ in subCategs:
        categ = getCategByIndex(i,driver)
        if categ is None:
            print("yalandan sayfalaran tanadı yaprak düğüm")
        else:
            oldTitle=driver.title
            driver.execute_script('var topPos=document.getElementsByClassName("cl")['+str(i)+'].offsetTop;document.getElementsByClassName("jspContainer")[0].scrollTop=topPos-10;') 
            categ.find_element_by_tag_name("a").click()  
            while page_title_changed(oldTitle,driver) is False:pass
        hoxx(driver)     
        backOneLevel(driver)
        
        #subCategs =driver.find_elements_by_xpath("//*[@id='searchCategoryContainer']//*/ul/li")
hoxx(driver)

print(13)

modellerBtn=driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[3]/div/a').get_attribute("href")
subModel=driver.find_element_by_xpath('//*[@id="search_cats"]/ul/li[4]/div/a').get_attribute("href")

# TODO: ÇEREZ ÇARPIYA TIKLA



listingCountCateg=int(bepsi[3].find_element_by_tag_name("span").text.replace("(","").replace(")",""))
listingCount=driver.find_element_by_xpath('//div[@class="result-text"]/span').text.split()[0].replace(".","")

assert "No results found." not in driver.page_source
driver.close()



#middle click link driver.execute_script("window.open('"+ nextpageBtn.get_attribute('href')+  "');")

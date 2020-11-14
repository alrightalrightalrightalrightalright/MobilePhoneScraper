#sahibinden mobil telefon ilanı
class Shbndnİlan:
    def __init__(self,link='',fiyat=0,listingDate='',listingId=0,brand=0,model="",os=0,
    storageCap=0,screenSize=0,ramSize=0,cameraRes=0,frontCamRes=0,color=0,
    warrantyStatus=0,fromWho=0,title="",city="",town=""):
        self.link=link
        self.fiyat=fiyat
        self.listingDate=listingDate
        self.listingId=listingId
        self.brand=brand
        self.os=os
        self.storageCap=storageCap#internal storage, gb
        self.screenSize=screenSize
        self.ramSize=ramSize
        self.cameraRes=cameraRes
        self.frontCamRes=frontCamRes
        self.color=color
        self.warrantyStatus=warrantyStatus
        self.fromWho=fromWho
        self.city=city
        self.town=town
        self.title=title
        self.model=model

    def print(self):
        print('link: {}\n{}₺, {} {} {} \n%{} gb storage, {} inch screen size, {} ram\n{}mb main cam, {}mb front cam, {} color \n{} of warranty, from: {}\n {} {}{} '
        '\n---------------------------\n'
        .format(self.link, self.fiyat  , self.brand ,self.model, self.os, self.storageCap, self.screenSize,
        self.ramSize, self.cameraRes, self.frontCamRes,  self.color, self.warrantyStatus, self.fromWho,
        self.city,self.town, self.listingDate))
    def getCSV(self):
        return ",".join(str(x) for x in(self.link,self.fiyat,self.listingDate,self.listingId,self.brand,self.os,self.storageCap,self.screenSize,self.ramSize,self.cameraRes,self.frontCamRes,self.color,self.warrantyStatus,self.fromWho,self.city,self.town,self.title,self.model))
 
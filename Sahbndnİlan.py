#sahibinden mobil telefon ilanı
class Shbndnİlan:
    fields = ("İlan No","İlan Tarihi","Marka","Model","İşletim Sistemi","Dahili Hafıza","Ekran Boyutu",
    "RAM Bellek","Kamera","Ön Kamera","Renk","Garanti","Kimden","Takas","Durumu")
    
    
    #yazık....
    def __init__(self,link='',fiyat=0,listingDate='',listingId=0,brand=0,model="",os=0,
    storageCap=0,screenSize=0,ram=0,cameraRes=0,frontCamRes=0,color=0,
    warrantyStatus=0,fromWho=0,title="",city="",town=""):
        self.data= {x: -1 for x in self.fields}
        self.link=link
        self.price=fiyat
        self.listingDate=listingDate
        self.listingId=listingId
        self.brand=brand
        self.os=os
        self.storageCap=storageCap#internal storage, gb
        self.screenSize=screenSize
        self.ram=ram    #MB
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
        .format(self.link, self.price  , self.brand ,self.model, self.os, self.storageCap, self.screenSize,
        self.ram, self.cameraRes, self.frontCamRes,  self.color, self.warrantyStatus, self.fromWho,
        self.city,self.town, self.listingDate))
    def getCSV(self):
        return ",".join(str(x) for x in self.data.values())
        #return ",".join(str(x) for x in(self.link,self.price,self.listingDate,self.listingId,self.brand,self.os,self.storageCap,self.screenSize,self.ram,self.cameraRes,self.frontCamRes,self.color,self.warrantyStatus,self.fromWho,self.city,self.town,self.title,self.model))
 
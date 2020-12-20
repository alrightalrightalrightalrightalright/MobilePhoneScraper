#sahibinden mobil telefon ilanı
class Shbndnİlan:
    fields = ("İlan Tarihi","Marka","Model","İşletim Sistemi","Dahili Hafıza","Ekran Boyutu",
    "RAM Bellek","Kamera","Ön Kamera","Renk","Garanti","Kimden","Takas","Durumu","Fiyat")
    
    #yazık....
    def __init__(self):
        self.data= {x: -1 for x in self.fields}
  
    def print(self):
        for x in self.data.values():
            print(str(x) ,", ")
        print("\n")

    def getCSV(self):
        return ",".join(str(x) for x in self.data.values())
 
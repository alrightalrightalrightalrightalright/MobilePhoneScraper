import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time



getTime = lambda : time.strftime("%H:%M:%S")
getDate = lambda : time.strftime("%d-%m-%Y")

#TODO: yeni gün için gün ve count değerini başlat, kodda oto olucak şekilde düzenle
class Firebase:
    certfFilePath="bepisyes-56453-firebase-adminsdk-qc39n-19680640eb.json"
    dbURL="https://bepisyes-56453.firebaseio.com/"
    #set anahtarın değerini yazar ve var olan değerleri siler, anahtar yoksa oluşturur
    #push anahtarı da değerini de yazar ve eşsiz ve kornolojik bir anahtarın altına yazar
    #update sadece istenen anahtarı edğişrweeqweewewrw
    def __init__(self): 
        self.cred = credentials.Certificate(self.certfFilePath)
        self.default_app=firebase_admin.initialize_app(self.cred,{"databaseURL":self.dbURL})
        self.ref = db.reference("dataset1")
    incrCountGlobal= lambda self: db.reference().update({"!Count":1}) if db.reference().child("!Count").get() is None else db.reference().update({"!Count": db.reference().child("!Count").get()+1})
    #increments for that day
    incrCount= lambda self: self.ref.update({"!Count":1}) if self.ref.child("!Count").get() is None else self.ref.update({"!Count":self.ref.child("!Count").get()+1})
    uptLastRun= lambda self: db.reference().child("!Last Run").set(getTime())

    def AddListing(self, obj):
        self.ref.child(obj.data["İlan No"]).set(obj.getCSV())
        self.incrCount()
        self.uptLastRun()

    isExists= lambda self, id: False if self.ref.child(id).get() is None else True
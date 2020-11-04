
import FileIO 
import requests
headers=''
headers = { 
    'Accept': '*/*',
    'Host': 'www.sahibinden.com',       
    'User-Agent': 'aaaaaaaaaaaaaaaaaaaa'
    }
        
r = requests.get("https://www.sahibinden.com/cep-telefonu-modeller/ikinci-el?",headers=headers, timeout=None)

### Queries ###
lastXdays = lambda a : "date="+a + "days" # date=30days


f = open("asd.html","w")
f.write(r.text)
f.close()

print( 'get: ', r.status_code)

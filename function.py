import  socket
import  requests
from    colorama import Fore, Back, Style
from    urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def getIP(url):
    s = socket.gethostbyname(url)
    print('IP: '+ s)
    return str(s)

def printMe(statusCode, url, length, full):
    if statusCode == 403:
        print(Fore.RED + str(statusCode) + Fore.WHITE + ' ' + url + ' - Length: ' + str(length))
    elif statusCode != 403 and statusCode != 200:
        print(Fore.YELLOW + str(statusCode) + Fore.WHITE + ' ' + url + ' - Length: ' + str(length))
    else:
        print(Fore.GREEN + str(statusCode) + Fore.WHITE + ' ' + url + ' - Length: ' + str(length))

    '''
    if statusCode == 200:
        print("CODE: 200 print content")
        print(full.text)
    '''

def requestT(url, headers):
    urlT = url._replace(scheme="http")
    r = requests.get(urlT.geturl(), allow_redirects = False, headers=headers, verify = False)
    if 'content-length' in r.headers.keys():
        l = r.headers['Content-Length']
    else:
        l = 0
    
    printMe(r.status_code, urlT.geturl(), l, r)
    #print(str(r.status_code) + ' ' + urlT.geturl() + ' - Length: ' + str(l))

    urlT = url._replace(scheme="https")
    r = requests.get(urlT.geturl(), allow_redirects = False, headers=headers, verify = False)
    if 'content-length' in r.headers.keys():
        l = r.headers['Content-Length']
    else:
        l = 0

    printMe(r.status_code, urlT.geturl(), l, r)
    #print(str(r.status_code) + ' ' + urlT.geturl() + ' - Length: ' + str(l))
   
def requestP(url, headers):
    ## RAW Test
    urlT = url._replace(scheme="http")
    s = requests.Session()
    s.verify = False

    req = requests.Request(method='GET', url=urlT.geturl(), headers=headers)
    prep = req.prepare()

    # aqui iria el mutator
    prep.url = urlT.geturl()
    t = s.send(prep, allow_redirects = False)
    if 'content-length' in t.headers.keys():
        l = t.headers['Content-Length']
    else:
        l = 0

    printMe(t.status_code, urlT.geturl(), l, t)
    #print(Fore.GREEN + str(t.status_code) + ' ' + Fore.WHITE + prep.url)

    ## HTTPS
    urlT = url._replace(scheme="https")
    s = requests.Session()
    s.verify = False
    s.max_redirects = 1
    req = requests.Request(method='GET', url=urlT.geturl(), headers=headers)
    prep = req.prepare()
 
    # aqui iria el mutator
    prep.url = urlT.geturl()
    t = s.send(prep, allow_redirects = False)

    if 'content-length' in t.headers.keys():
        l = t.headers['Content-Length']
    else:
        l = 0

    printMe(t.status_code, urlT.geturl(), l, t)
    #print(Fore.GREEN + str(t.status_code) + ' ' + Fore.WHITE + prep.url)

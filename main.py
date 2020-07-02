import  requests
from    colorama import Fore, Back, Style
import  argparse
import  socket
from    function import *
import  urllib
from    urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

print(Fore.BLUE + Style.BRIGHT + """
                       _     _               
                      (_)   | |              
__   ____ _ _ __ _ __  _ ___| |__   ___ _ __ 
\ \ / / _` | '__| '_ \| / __| '_ \ / _ \ '__|
 \ V / (_| | |  | | | | \__ \ | | |  __/ |   
  \_/ \__,_|_|  |_| |_|_|___/_| |_|\___|_|   
                                             
                                             """)

print(Style.RESET_ALL)

#print('Use -u for a single url or -iL for url list')

## arguments <3
parser = argparse.ArgumentParser()

parser.add_argument('-u', help='URL', dest='url')
parser.add_argument('-iL', help='URL List path', dest='fileList')
parser.add_argument('-d', help='debugmode', dest='debug')

args = parser.parse_args() # arguments to be parsed

## This is to retrieve content-length
headers = {'Accept-Encoding': 'None' } 

## crazy paths for now only two pretty much static
paths = ['{}///', '/love/..{}']

## ipHeader test
ipHeader = ['127.0.0.1']
xIPHeader = ['X-Forwarded-For', 'Real-IP', 'X-Real-IP']

if args.url:
    print('URL: '+ args.url)
    urlParsed = urllib.parse.urlparse(args.url)
    try:
        ipHeader.append(getIP(urlParsed.netloc))
    except:
        print('NO IP')

    if args.debug:
        print('\n>>>>> ' + str(urlParsed) + '\n')
        r = requests.get(urlParsed.geturl(), allow_redirects = False, headers={'Accept-Encoding': None })
        print(r.headers)
        print(ipHeader)

    print('\n')
    print(Fore.YELLOW + 'Request via http & via https [non altered]')
    print(Style.RESET_ALL)

    r = requestT(urlParsed, headers)

    print('\n')

    ## lets try crazy paths
    print(Fore.YELLOW + 'Crazy paths')
    print(Style.RESET_ALL)

    for i in paths:
        alterPath = i.replace("{}",urlParsed.path)
        alterUrl = urlParsed._replace(path=alterPath)
        ##print(alterUrl)
        r = requestP(alterUrl, headers)

    print('\n')
    ## lets try just proto
    print(Fore.YELLOW + 'Request with X-Forwarded-Proto')
    print(Style.RESET_ALL)

    headers.update({'X-Forwarded-Proto':'https'})
    r = requestT(urlParsed, headers)

    print('\n')
    ## lets try crazy paths
    print(Fore.YELLOW + 'Crazy paths + X-Forwarded-Proto')
    print(Style.RESET_ALL)

    for i in paths:
        alterPath = i.replace("{}",urlParsed.path)
        alterUrl = urlParsed._replace(path=alterPath)
        ##print(alterUrl)
        r = requestP(alterUrl, headers)

    #print('\n')
    ## lets X-Forwarded-For and IPs HEADER
    #print(Fore.YELLOW + 'IP Headers ' + str(xIPHeader))
    #print(Style.RESET_ALL)

    for i in xIPHeader:
        headers.update({i:''})

    for i in ipHeader:
        print('\n')
        ## lets X-Forwarded-For and IPs HEADER
        print(Fore.YELLOW + 'IP Headers ' + str(xIPHeader) + ' and IP: ' + i)
        print(Style.RESET_ALL)

        headers = headers.fromkeys(xIPHeader, i)
        r = requestT(urlParsed, headers)

    ## lets try with HOST
    print('\n')
    print(Fore.YELLOW + 'Request with Host value as server')
    print(Style.RESET_ALL)
    headers.update({'Host':str(ipHeader[1])})
    r = requestT(urlParsed, headers)

    ## lets try with HOST
    print('\n')
    print(Fore.YELLOW + 'Request with Host value as server + X-Forwarded-Proto')
    print(Style.RESET_ALL)
    headers.update({'Host':str(ipHeader[1])})
    headers.update({'X-Forwarded-Proto':'https'})
    r = requestT(urlParsed, headers)

    ## HOST
    print('\n')
    print(Fore.YELLOW + 'Crazy paths + Host + X-Forwarded-Proto')
    print(Style.RESET_ALL)
    headers.update({'Host':str(ipHeader[1])})
    headers.update({'X-Forwarded-Proto':'https'})

    for i in paths:
        alterPath = i.replace("{}",urlParsed.path)
        alterUrl = urlParsed._replace(path=alterPath)
        ##print(alterUrl)
        r = requestP(alterUrl, headers)

    ## lets try with HOST
    print('\n')
    print(Fore.YELLOW + 'Request with Host uppercase + X-Forwarded-proto')
    print(Style.RESET_ALL)
    headers.update({'Host':str(urlParsed.netloc).upper()})
    headers.update({'X-Forwarded-Proto':'https'})
    r = requestT(urlParsed, headers)
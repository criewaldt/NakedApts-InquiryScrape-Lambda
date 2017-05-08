import requests
import json
import datetime
import traceback
from bs4 import BeautifulSoup
import pprint
import boto3
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import time, random

class NakedApts(object):
    def __init__(self, username, password, proxies):
        self.ads = []
        self.user = username
        self.proxies = proxies
        self.session = requests.Session()
        self.session.headers={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
        self.status = self.Login(username, password)

    def get_ads(self,):
        url = "http://www.nakedapartments.com/broker/listings?all=true&listings_scope=published&order=asc&page=1&sort=rent"
        r = self.session.get(url, proxies=self.proxies)
        soup = BeautifulSoup(r.content, "html.parser")
        trs = soup.find_all("tr")
        del trs[0]
        del trs[-1]
        for tr in trs:
            address = tr.find("td", {"class":"listing"})
            webid = address.a.text.split("Web ID:")[1].strip()
            address = address.a.text.split("Web ID")[0].strip().split(',')[0]
            size = tr.find("td", {"class":"aptSize"}).text.strip()
            rent = tr.find("td", {"class":"listing-rent"}).text.strip()
            try:
                img = tr.find("img").get('src')
            except AttributeError:
                img = "static/images/missing.jpg"
            self.ads.append([('''<img src='''+img+'''" alt="" height="68" width="90">'''), address, size, rent, webid, ('''<input type="checkbox" name="'''+webid+'''" id="'''+webid+'''">''')])
        return self.ads

    def get_inquiry_data(self,):
        iCount = 0
        hardStop = False
        inquiries = []
        inquiryData = []

        inbox_url = "https://www.nakedapartments.com/broker/messages?page="
        archived_url = "https://www.nakedapartments.com/broker/messages/archived?page="
        deleted_url = "https://www.nakedapartments.com/broker/messages/deleted?page="
        
        while True:
            #inbox
            print "Checking inbox inquiries"
            pageCount = 1
            while True:
                print 'Scraping page:', str(pageCount)
                r = self.session.get((inbox_url+str(pageCount)), proxies=self.proxies)
                soup = BeautifulSoup(r.content, "html.parser")
                #
                # Look for break condition
                #
                trs = soup.find_all("tr")
                if len(trs) <= 1:
                    break
                for tr in trs:
                    #global inquiry count
                    iCount += 1
                    result = []
                    tds = tr.find_all("td")
                    for td in tds:
                        result.append(td.text.strip())
                    if len(result) > 0:
                        inquiries.append(result)
                pageCount += 1
                break
                time.sleep(random.randint(1,5))

            #archived
            print 'Checking archived inquiries...'
            pageCount = 1
            while True:
                print 'Scraping page:', str(pageCount)
                r = self.session.get((archived_url+str(pageCount)), proxies=self.proxies)
                soup = BeautifulSoup(r.content, "html.parser")
                #
                # Look for break condition
                #
                trs = soup.find_all("tr")
                if len(trs) <= 1:
                    break
                for tr in trs:
                    #global inquiry count
                    iCount += 1
                    result = []
                    tds = tr.find_all("td")
                    for td in tds:
                        result.append(td.text.strip())
                    if len(result) > 0:
                        inquiries.append(result)
                pageCount += 1
                time.sleep(random.randint(1,5))
                
            
            
            #deleted
            print 'Checking deleted inquiries...'
            pageCount = 1
            while True:
                print 'Scraping page:', str(pageCount)
                r = self.session.get((deleted_url+str(pageCount)), proxies=self.proxies)
                soup = BeautifulSoup(r.content, "html.parser")
                #
                # Look for break condition
                #
                trs = soup.find_all("tr")
                if len(trs) <= 1:
                    break
                for tr in trs:
                    #global inquiry count
                    iCount += 1
                    result = []
                    tds = tr.find_all("td")
                    for td in tds:
                        result.append(td.text.strip())
                    if len(result) > 0:
                        inquiries.append(result)
                pageCount += 1
                time.sleep(random.randint(1,5))
                
            ##WE NOW HAVE ADS! Clean the data
            
            
            for i in inquiries:
                try:
                    i[5] = i[5].replace(',', '')
                    i[5] = i[5].replace('$', '')
                    i[5] = int(i[5])
                except:
                    pass
                try:
                    i[7] = i[7].split(' ')[1].strip()
                except:
                    pass
            ##Convert the dates to objects
            
            

            for i in inquiries:
                try:
                    m = int(i[7].split('/')[0].lstrip('0'))
                    d = int(i[7].split('/')[1].lstrip('0'))
                    y = int("20" + str(i[7].split('/')[2].strip()))
                except:
                    today = datetime.date.today()
                    m = today.month
                    d = today.day
                    y = today.year
            #all done
            break
        print iCount, 'total inquiries found.'
        return {'user':self.user, 'count':iCount, 'data':inquiryData}

    #LOGIN
    def Login(self, username, password):
        r = self.session.get("https://www.nakedapartments.com/login", proxies=self.proxies)
        soup = BeautifulSoup(r.content, "html.parser")
        _csrf = soup.find("meta", {"name":"csrf-token"})
        csrf = _csrf.get('content')
        login_data = {'user_session[email]' : username,
                      'user_session[password]' : password,
                      'authenticity_token' : csrf,
                      'user_session[remember_me]' : 0,
                      'button' : ''}

        r = self.session.post('https://www.nakedapartments.com/user_session', data=login_data, proxies=self.proxies)
        soup = BeautifulSoup(r.content, "html.parser")
        error = soup.find("div", {"class": "error alert alert-error"})
        if error:
            if error.text == "Sorry, your email and password didn't match.":
                print(error.text)
                return False
        else:
            return True
    #LOGOUT
    def Logout(self,):
        r = self.session.get('http://www.nakedapartments.com/logoff', proxies=self.proxies)

def get_proxy_list():
    resource = boto3.resource('dynamodb',
            aws_access_key_id='AKIAIOZC3MKUZ2CG6VJQ',
            aws_secret_access_key='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',
            region_name='us-east-1')
    proxy_table = resource.Table('advertapi-proxylist')
    #grab proxy list
    response = proxy_table.scan()
    return response['Items']

def next_proxy(proxy_list):
    #return least recently used proxy
    nextProxy = sorted([datetime.datetime.strptime(item['lastused'], "%Y-%m-%d %H:%M:%S.%f") for item in proxy_list])[0]

    resource = boto3.resource('dynamodb',
            aws_access_key_id='AKIAIOZC3MKUZ2CG6VJQ',
            aws_secret_access_key='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',
            region_name='us-east-1')
    proxy_table = resource.Table('advertapi-proxylist')

    #do dynamodb request
    response = proxy_table.scan(
        FilterExpression=Attr('lastused').eq(str(nextProxy))
    )
    p = response['Items'][0]

    proxies = {'http': 'http://{}:{}@{}:{}/'.format(p['username'], p['password'], p['ip'], p['port']),
            'https': 'https://{}:{}@{}:{}/'.format(p['username'], p['password'], p['ip'], p['port'])}

    #update proxylist db
    response = proxy_table.put_item(
       Item={
            'ip': p['ip'],
            'port': p['port'],
            'username': p['username'],
            'password': p['password'],
            'lastused': str(datetime.datetime.utcnow())
        }
    )  
    return proxies



def main(event, context):
    username = event['auth']['username']
    password = event['auth']['password']
    
    #grab the next proxy to use from the db
    print 'Grabbing proxy from DynamoDB: advertapi-proxylist' 
    proxies = next_proxy(get_proxy_list())

    print 'Attempting NakedApts login...'
    na = NakedApts(username, password, proxies)
    if not na.status:
        return None
               
    print 'NakedInquiry is starting'
    iD = na.get_inquiry_data()
    
    na.Logout()

    print 'Returning response & shutting down'

    return iD
    
if __name__ == "__main__":
    pass


    
    

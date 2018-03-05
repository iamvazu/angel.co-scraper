#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:     Scrape angel.co
#
# Author:      Lord VAZU
#      
# Created:     12/09/2017
# Copyright:   (c) Lord VAzu 2017
# Licence:     <V1.0>
#-------------------------------------------------------------------------------



import requests
import re
import sys
from time import sleep
import time
import stem.process
from stem import Signal
from stem.control import Controller
from bs4 import BeautifulSoup
from ra4 import *
from openpyxl import Workbook
wb = Workbook()
ws=wb.active
import random



def switchIP():
    with Controller.from_port(port=9151) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)
        sleep(10)
        print('Switching')

        
proxies = {'http':  'socks5://127.0.0.1:9150','https': 'socks5://127.0.0.1:9150'}

        
#proxy_list=["199.195.142.65:80","208.83.6.18:3128","108.59.10.129:55555","168.63.24.174:8124","74.91.125.170:8118","50.240.46.244:7004","184.155.18.163:3128","23.92.75.112:80"]
from fake_useragent import UserAgent
ua = UserAgent()

#ua.update()


url_list=[]
name_list=[]
tagline_list=[]
desc_list=[]
loc_list=[]
tags_list=[]
numemp_list=[]
founder_list = []
link_list = []
emp_list=[]
inv_list=[]
board_list=[]
past_list=[]
pastinv_list =[]
mainurl = 'https://angel.co/machine-learning'
page = requests.get(mainurl, proxies = proxies)
soup = BeautifulSoup(page.content,'lxml')
compnum  = soup.find(attrs = {'data-open':'false'}).text.replace(',','').replace('Companies','').strip()
compnum = int(compnum)/20
compnum=int(compnum)

####compnum
#compnum = 1
# range (1)
# it should be range(start, compnum)
#so if error ar 9


for a in range(1,compnum+1):
    sleep(20)
    try:
        switchIP()
        print (a)

        url = mainurl+'?page='+str(a)




        page =  requests.get(url,headers={'X-Requested-With':'XMLHttpRequest'})

        soup = BeautifulSoup(page.content,'lxml')
        for i in soup.find_all('a',{'class':'\\"startup-link\\"'}):
            fl=[]
            el=[]
            Ll = []
            Il=[]
            Bl=[]
            Pl=[]
            Pil=[]
            
            if 'title' not in str(i):
                continue
            i=i['href'].replace('"','').replace('\\','')
            #prxy = random.choice(proxy_list)
            #proxies ={'http':prxy}
           # print proxies
            #print ua.random

            

            page  = requests.get(i,proxies=proxies,headers = {'User-Agent':ua.random,'X-Requested-With':'XMLHttpRequest'})
            
            soup = BeautifulSoup(page.content,'lxml')
            print (i)

            name = soup.find('h1').text.strip()
            count=0
            while name == 'AngelList' and count<10:
                switchIP()
                count+=1
                
                page  = requests.get(i,proxies=proxies,headers = {'User-Agent':ua.random,'X-Requested-With':'XMLHttpRequest'})
                soup = BeautifulSoup(page.content,'lxml')
                name = soup.find('h1').text.strip()
                print ('CAPTCHA')

                
            tagline = soup.find('h2').text.strip()
           # print (tagline)
    ##
            try:
                desc = soup.find(attrs={'class':'show windows'}).text.strip()
            except:
                try:
                    desc = soup.find(attrs={'class':'content'}).text.strip()
                except :desc='Nan'
            loc = soup.find(attrs = {'class':'tag'}).text.strip()

            tags = soup.find(attrs={'class':'js-market_tags'}).text.strip()
            numemp = soup.find(attrs={'class':'js-company_size'}).text.strip()
            
    ##

            foundersect = soup.find(attrs={'class':'founders section'})
            try:
                for b in foundersect.find_all(attrs={'class':'profile-link'}):
                    b=b.text.strip()
                    fl.append(b)
            except: fl=['NaN']

    ##        

            employees_section = soup.find(attrs={'data-tips_selector':'employees_section'})
            if employees_section is not None:
                employees_section=employees_section.next_element.next_element.next_element        

            try:
                for b in employees_section.find_all(attrs={'class':'profile-link'}):
                    b=b.text.strip()
                    
                    el.append(b)
            except: el=['NaN']
    ##
            links = soup.find(attrs={'class':'js-links links s-vgRight1 u-hiddenSmOnly'})
            try:
                for b in links.find_all('a'):
                    b = b['href']
                    Ll.append(b)
            except:Ll=['NaN']
    ##
            investors = soup.find(attrs={'data-tips_selector':'right_block body_tags'})
            if investors is not None:
                investors=investors.next_element.next_element.next_element
            try:
                for z in investors.find_all('a'):
                    z=z.text
                    Il.append(z)
            except:Il=['NaN']
                    
    ##
            boardmember= soup.find(attrs={'data-tips_selector':'board_members_section'})
            if  boardmember is not None:
                boardmember=boardmember.next_element.next_element.next_element
            try:
                for z in boardmember.find_all('a'):
                    z=z.text

                    Bl.append(z)
            except:Bl=['NaN']
    ##
            pastemp = soup.find(attrs={'data-tips_selector':'past_employees_section'})
            if pastemp is not None:
                pastemp=pastemp.next_element.next_element.next_element

                

            try:
                for z in pastemp.find_all('a'):
                    z=z.text

                    Pl.append(z)
            except:Pl=['NaN']

    ##        
            pastinv= soup.find(attrs={'class':'past_financing section'})
            if pastinv is not None:
                pastinv=pastinv            
                

            try:
                for z in pastinv.find_all('a'):
                    z=z.text

                    Pil.append(z)
            except:Pil=['NaN']        


            fl = '|'.join(fl)
            el= '|'.join(el)
            Ll= '|'.join(Ll)
            Il='|'.join(Il)
            Bl='|'.join(Bl)
            Pl='|'.join(Pl)
            Pil = '|'.join(Pil)

            
            pastinv_list.append(Pil)
            board_list.append(Bl)
            past_list.append(Pl)
            inv_list.append(Il)
            emp_list.append(el)
            link_list.append(Ll)
            founder_list.append(fl)
            url_list.append(i)
            name_list.append(name)
            tagline_list.append(tagline)
            desc_list.append(desc)
            loc_list.append(loc)
            tags_list.append(tags)
            numemp_list.append(numemp)
            
            del fl
            del el
            del Il
            del Ll
            del Bl
            del Pl
            del Pil

    except KeyboardInterrupt:
        print('Saving File on interrupt')
        break
    except Exception as E:
        print(E)
        break

# this is to save the data in case some error comes up, it will print the error message so we can troubleshoot lateron
# and will print the error url, when that happens and you want to resume,

# change this
title = 'URL NAME TAGLINE DESC TAGS EMPLOYEENUM FOUNDERs LOCATION EMPLOYEES LINKS PASTINVESTOR PASTEMP BOARDMEM INVESTOR'.split(' ')
ws.append(title)

rappend(url_list,1,ws)
rappend(name_list,2,ws)
rappend(tagline_list,3,ws)
rappend(desc_list,4,ws)
rappend(tags_list,5,ws)
rappend(numemp_list,6,ws)
rappend(founder_list,7,ws)
rappend(loc_list,8,ws)
rappend(emp_list,9,ws)
rappend(link_list,10,ws)
rappend(inv_list,14,ws)
rappend(past_list,12,ws)
rappend(board_list,13,ws)
rappend(pastinv_list,11,ws)

tim = str(time.strftime('%H%M'))+'angel.xlsx'
print (tim)
wb.save(tim)
wb.close()




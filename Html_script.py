# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 21:34:41 2019

@author: krish.naik
"""
import os
import time
import requests
import sys


def retrieve_html(): #retrive html
    for year in range(2013,2019):  #go for each and every year,month
        for month in range(1,13):
            if(month<10):
                url='http://en.tutiempo.net/climate/0{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            else:
                url='http://en.tutiempo.net/climate/{}-{}/ws-421820.html'.format(month
                                                                          ,year)
            texts=requests.get(url) #retrive text download
            text_utf=texts.text.encode('utf=8') #enconde due to some char in html tag fix it
            
            if not os.path.exists("Data/Html_Data/{}".format(year)): #if not exist in local environment check folders exist or not
                os.makedirs("Data/Html_Data/{}".format(year)) #make dir if not exist req path
            with open("Data/Html_Data/{}/{}.html".format(year,month),"wb") as output: #if exist we make open in always write byte mode
                output.write(text_utf)  #here writting corresponding text
            
        sys.stdout.flush() #flush everything we creating
        
if __name__=="__main__":
    start_time=time.time()
    retrieve_html() #calling function
    stop_time=time.time()
    print("Time taken {}".format(stop_time-start_time)) #time to execute
        
    

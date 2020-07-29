from Plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016 #extacting from behind code
import requests
import sys
import pandas as pd
from bs4 import BeautifulSoup #html web crapping
import os
import csv

def met_data(month, year): #web scrab each and every file
    
    file_html = open('Data/Html_Data/{}/{}.html'.format(year,month), 'rb') #read
    plain_text = file_html.read() #read and assigning content

    tempD = []
    finalD = []
#soup can extact anything from html page
    soup = BeautifulSoup(plain_text, "lxml") #what we want take it
    for table in soup.findAll('table', {'class': 'medias mensuales numspan'}):  #in this content present and onlt that class
        for tbody in table:
            for tr in tbody: #tr is list of table rows
                a = tr.get_text() #pick text
                tempD.append(a)

    rows = len(tempD) / 15  #15 col(features) ,get no of rows

    for times in range(round(rows)): # iterate each  row
        newtempD = []
        for i in range(15): # iterate each  feature
            newtempD.append(tempD[0]) #pick and append dat
            tempD.pop(0) #after add remove
        finalD.append(newtempD)

    length = len(finalD)

    finalD.pop(length - 1) #rem last record
    finalD.pop(0) #pop 0 th row

    for a in range(len(finalD)): #remove un necessary fetaures
        finalD[a].pop(6)
        finalD[a].pop(13)
        finalD[a].pop(12)
        finalD[a].pop(11)
        finalD[a].pop(10)
        finalD[a].pop(9)
        finalD[a].pop(0)

    return finalD

def data_combine(year, cs):
    for a in pd.read_csv('Data/Real-Data/real_' + str(year) + '.csv', chunksize=cs):
        df = pd.DataFrame(data=a)
        mylist = df.values.tolist()
    return mylist


if __name__ == "__main__":
    if not os.path.exists("Data/Real-Data"): #if not exist make path
        os.makedirs("Data/Real-Data")
    for year in range(2013, 2017):
        final_data = []
        with open('Data/Real-Data/real_' + str(year) + '.csv', 'w') as csvfile: #create csv file
            wr = csv.writer(csvfile, dialect='excel') #write in excel sheet
            wr.writerow(  #write col names
                ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5'])
        for month in range(1, 13): #for month
            temp = met_data(month, year)#call fuunction
            final_data = final_data + temp #append
            
        pm = getattr(sys.modules[__name__], 'avg_data_{}'.format(year))() #dep feature
        #dep feat is avg_data
        if len(pm) == 364:  #if 364 is -
            pm.insert(364, '-')

        for i in range(len(final_data)-1): #append at last feature
            # final[i].insert(0, i + 1)
            final_data[i].insert(8, pm[i])

        with open('Data/Real-Data/real_' + str(year) + '.csv', 'a') as csvfile: #crete new folder
            wr = csv.writer(csvfile, dialect='excel') #write
            for row in final_data:
                flag = 0
                for elem in row:
                    if elem == "" or elem == "-": #drop
                        flag = 1
                if flag != 1: # write only flag=0
                    wr.writerow(row)
                    
    data_2013 = data_combine(2013, 600)  #calling and combine
    data_2014 = data_combine(2014, 600)
    data_2015 = data_combine(2015, 600)
    data_2016 = data_combine(2016, 600)
     
    total=data_2013+data_2014+data_2015+data_2016 #combine all data
    
    with open('Data/Real-Data/Real_Combine.csv', 'w') as csvfile: #cretae and  write data
        wr = csv.writer(csvfile, dialect='excel')
        wr.writerow(
            ['T', 'TM', 'Tm', 'SLP', 'H', 'VV', 'V', 'VM', 'PM 2.5']) #feature names
        wr.writerows(total)
        
        
df=pd.read_csv('Data/Real-Data/Real_Combine.csv')
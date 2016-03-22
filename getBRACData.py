import re
import requests
import sqlite3
import sys
import time

dbConn = sqlite3.connect('BRACData.db')
cur = dbConn.cursor()
cur.execute('DELETE FROM Event')
cur.execute('DELETE FROM EventCategory')

BRAC = requests.Session()
for year in range(2010, 2016):
    url = 'https://www.coloradocycling.org/results/table?disc=road&year='+str(year)+'&eventId=&resultsetId=sum&s=place+ASC&action=getEvents'
    bracRequest = BRAC.get(url, verify=False)
    #print bracRequest.text


    parseEvents = re.compile(r'"value":"(\d+)","text":"(.*?) - (.*?)"}')
    parseCategories = re.compile(r'<tr class[^>]*>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*<td>\s*(.*?)\s*</td>\s*</tr>')
    eventList = parseEvents.findall(bracRequest.text)
    for event in eventList:
        while True:
            try:
                sql = 'DELETE FROM Event WHERE ID = ' + event[0]
                cur.execute(sql)
                sql = 'DELETE FROM EventCategory WHERE EventID = ' + event[0]
                cur.execute(sql)
                sql = 'INSERT INTO Event (ID, EventName, EventDate, EventYear) VALUES( '+event[0]+', \''+re.sub('\'', '', event[2])+'\', \''+re.sub(r"\\\/", '-', event[1])+'\', ' + str(year) + ')'
                print sql
                cur.execute(sql)
                eventURL = 'https://www.coloradocycling.org/results/table?disc=road&year='+str(year)+'&eventId='+event[0]+'&resultsetId=sum&s=place+ASC'
                #print eventURL
                bracRequest = BRAC.get(eventURL, verify=False)
                eventHTML = bracRequest.text
                #print eventHTML
                categoryTable = re.search(r'<table id="t3"[^>]*>(.*?)</table>', eventHTML, re.S).group(1)
                #categoryTable = re.sub('\s*', '', categoryTable)
                #print categoryTable
                categoryList = parseCategories.findall(categoryTable)
                for cat in categoryList:
                    #print "\t"+cat[0]
                    sql = 'INSERT INTO EventCategory (EventID, Category, Starters, Finishers) VALUES( '+event[0]+', \''+re.sub('\'', '', cat[0])+'\', ' + cat[1] + ', ' + cat[2] + ')'
                    print "\t"+sql
                    cur.execute(sql)
                break   #break out of the while true loop
            except: 
                print 'Failed on ' + event[2] + '. Retrying...'
                time.sleep(5)
            
        #break
        time.sleep(5)
    
dbConn.commit()
dbConn.close()
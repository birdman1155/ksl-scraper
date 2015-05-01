#!/usr/bin/python


import argparse
import re
from multiprocessing.pool import ThreadPool as Pool
import requests
import bs4
import sqlite3 as lite
from email.mime.text import MIMEText
from os import system
import os
import smtplib


root_url = 'http://www.ksl.com/'
index_url = root_url + 'index.php?nid=231&sid=74268&cat=613&search=iphone+5s&zip=Enter+Zip+Code&distance=&min_price=&max_price=&type=&category=345&subcat=&sold=&city=&addisplay=&sort=1&userid=&markettype=sale&adsstate=&nocache=1&o_facetSelected=&o_facetKey=&o_facetVal=&viewSelect=list&viewNumResults=12&sort=1'

response = requests.get(index_url)
soup = bs4.BeautifulSoup(response.text)

def get_phone_title():
    return [span.get_text() for span in soup.select('div.listings div.adBox div.detailBox span.adTitle')]


def get_phone_price():
    #removes the cents span element. Such a pain...
    [span.extract() for span in soup.select('div.listings div.adBox div.detailBox div.priceBox a span span')]
    return [span.get_text() for span in soup.select('div.listings div.adBox div.detailBox div.priceBox a span')]

def get_phone_link():
    return [a.attrs.get('href') for a in soup.select('div.listings div.adBox div.detailBox span.adTitle a')]


con = lite.connect('~/Desktop/ksl-scraper/iPhones.db')

with con:

    cur = con.cursor()

    count = 0
    #reversed order places the newest add on top instead of on the bottom (FIFO)

    title = get_phone_title()[count]
    link = root_url + get_phone_link()[count]
    price = get_phone_price()[count]

    while (count == 0):
        #print title + price + "\n" + link
        
        #increment to end the while loop
        count += 1
    
        #cur.execute("INSERT INTO iPhones VALUES(?, ?, ?);", (title, price, link))
        
        
        # if error then then create the table... need to do this later.
        cur.execute("SELECT * FROM iPhones LIMIT 1;")

        rows = cur.fetchall()
        for row in rows:
            oldTitle = row[0]
            oldPrice = row[1]
            oldLink = row[2]
            
                
                #cur.execute("INSERT INTO iPhones VALUES(?, ?, ?);", (title, price, link))

            #print oldTitle + oldPrice + "\n" + oldLink + "vfdsaf"
            
            
            if (link != oldLink):
                #cur.execute("DROP TABLE IF EXISTS iPhones;")
                cur.execute("DELETE FROM iPhones;")
                cur.execute("INSERT INTO iPhones VALUES(?, ?, ?);", (title, price, link))




                gmail_user = "USEREMAIL"
                gmail_pwd = "PASSWORD"
                FROM = 'USEREMAIL'
                TO = ['USEREMAIL'] #must be a list
                SUBJECT = price + title
                TEXT = link
                
                # Prepare actual message
                message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
                    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
                try:
                    #server = smtplib.SMTP(SERVER)
                    server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                    server.ehlo()
                    server.starttls()
                    server.login(gmail_user, gmail_pwd)
                    server.sendmail(FROM, TO, message)
                    #server.quit()
                    server.close()
                    system('print "email sent!"')
                except:
                    system('print "failed to send email!"')
    
            else:
                system('print "no new listings...sorry!"')



    #for i in reversed(get_phone_title()):
        #print i + get_phone_price()[count] + "\n" + root_url + get_phone_link()[count]
        #link = root_url + get_phone_link()[count]
        #price = get_phone_price()[count]

        #if (count < link):
            #cur.execute("DROP TABLE IF EXISTS iPhones;")
            #cur.execute("CREATE TABLE IF NOT EXISTS iPhones(Title TEXT, Price INT, Link TEXT);")
            #cur.execute("INSERT INTO iPhones VALUES(?, ?, ?);", (i, price, link))
    
        #count += 1
    
    con.commit()








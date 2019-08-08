from bs4 import BeautifulSoup as bs
from selenium import webdriver
import urllib2
import oauth2
import string
from urllib import pathname2url
import os
import webbrowser
from time import sleep
from datetime import date

#pass url to import raw html via chrome
def getHTML(url):
    driver=webdriver.Chrome('chromedriver.exe')
    driver.get(url)
    html=driver.page_source
    driver.close()
    return html

def getActorDetails():
    source=getHTML("http://m.imdb.com/feature/bornondate")
    soup = bs(source, 'html.parser')
    listImage=[]
    listName=[]
    listDetail=[]
    listBestWork=[]
    finalList=[]
    allActors=soup.findAll('h3', class_="lister-item-header")
    for i in allActors:
        name=i.find('a').string
        name=name.strip()
        name.encode('utf-8')
        listName.append(name)

    allActorsImage=soup.findAll('div', class_="lister-item-image")
    for i in allActorsImage:
        img=i.find("img")['src']
        img.encode('utf-8')
        listImage.append(img)
        
    allActorsDetails=soup.findAll('div',class_="lister-item-content")
    for i in allActorsDetails:
        detail=i.find('p',class_="text-muted text-small")
        bw=detail.contents[3]
        bw=bw.string
        bw=bw.strip()
        bw.encode('utf-8')
        detail=detail.contents[0]        
        listBestWork.append(bw)
        listDetail.append(detail[26:].encode('utf-8'))
        
    l=len(listName)
    for i in range(0,l):
        indv=[listName[i],listImage[i],listDetail[i],listBestWork[i]]
        finalList.append(indv)
    return finalList

def main():

    print """

--------------------------------------------------------------------------------------------------------------
Web Scraping in progress
--------------------------------------------------------------------------------------------------------------"""
    sleep(3)
    actorlist=getActorDetails()
    res=open("result.html","w")
    res.write("<h2>Details of Celebrities whose birthday is on "+(str)(date.today())+"</h2>") 
    res.write("<table><tr><th>Name</th><th>Image</th><th>Profession</th><th>Best Work</th></tr>")
    for actor in actorlist:
        res.write("<tr>")
        for col in actor:
            if col==actor[1]:
                res.write("<td style='text-align:center'><img src='"+col.encode('utf-8')+"' style='width:100px'></td>")
            else:
                res.write("<td style='text-align:center'>"+col.encode('utf-8')+"</td>")
        res.write("</tr>")
    res.write("</table>")
    url = 'file:{}'.format(pathname2url(os.path.abspath('result.html')))
    choice= raw_input("Enter Y to view")
    if choice=="y" or choice=="Y" :
        webbrowser.open(url)
main()

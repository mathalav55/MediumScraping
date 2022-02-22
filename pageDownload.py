#download page
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
from urllib.request import urlretrieve
import urllib.request
import cssutils
import logging
import re


#function to remove JS
def removeRearWing(fileContent):
  temp = re.sub("<script src=\".*\"></script>", "", fileContent)
  return temp
#function to remove SideBars
def removeSidepods(soup):
  for div in soup.find_all("div", {'class':'bl'}): 
    div.decompose()
  return soup
#function to remove Related Topics
def removeFloor(soup):
  if(soup.find('div',class_='l ot nm')):
    soup.find('div',class_='l ot nm').decompose()
  return soup

#function to download web page
def downloadPage(pageUrl):
  print ("Connecting to server")
  cssutils.log.setLevel(logging.CRITICAL)
  directory = ''
  opener = urllib.request.build_opener()
  #defining headers as some servers mandiate it
  opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                          ('Connection', 'keep-alive')
                      ]
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(pageurl).read()
  print ("Connection Success!")
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          f = open( 'index.html', 'w' )
          soup = removeSidepods(soup)
          soup = removeFloor(soup)
          text = removeRearWing(str(soup))
          f.write(text)
          f.close()
          print ('Script Executed successfully!')
  except Exception as e:
      print ("Exception occurred = ",e)


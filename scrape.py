#download page
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from urllib.request import urlretrieve
import urllib.request
import cssutils
import logging
from pageDownload import downloadPage

def tagDownload(link):
  cssutils.log.setLevel(logging.CRITICAL)
  opener = urllib.request.build_opener()
  #defining headers as some servers mandiate it
  opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                          ('Connection', 'keep-alive')
                      ]
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(link).read()
  print ("Connection Success!")
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          postLinks = []
          #post link class - button button--smaller button--chromeless u-baseColor--buttonNormal
          for post in soup.find_all("a", {"class": "button button--smaller button--chromeless u-baseColor--buttonNormal"}):
            postLinks.append(str(post['href']))
          for link in postLinks:
            downloadPage(link)
  except Exception as e:
      print ("Exception occurred = ",e)



#function to get url list
def scrape(baseUrl):
  print ("Connecting to server")
  cssutils.log.setLevel(logging.CRITICAL)
  opener = urllib.request.build_opener()
  #defining headers as some servers mandiate it
  opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                          ('Connection', 'keep-alive')
                      ]
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(baseUrl).read()
  print ("Connection Success!")
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          tagLinks = []
          
          #get list of soup links - link class - js-navItemLink
          for tag in soup.find_all("a", {"class": "js-navItemLink"}):
            tagLinks.append(str(tag['href']))
          #run loop for each tag link
          for link in tagLinks:
            tagDownload(link)
          print ('Script Executed successfully!')
  except Exception as e:
      print ("Exception occurred = ",e)
#download page
from bs4 import BeautifulSoup
import os
from urllib.request import urlretrieve
from urllib.request import urlretrieve
import urllib.request
import cssutils
import logging
import re
import traceback
headers = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                          ('Connection', 'keep-alive')
                      ]
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
def downloadPage(pageUrl,folder="test",title=""):
  # print ("Connecting to server")
  cssutils.log.setLevel(logging.CRITICAL)
  directory = folder + '/'
  if( not os.path.isdir(directory)):
    os.makedirs(directory)
  opener = urllib.request.build_opener()
  #defining headers as some servers mandiate it
  opener.addheaders = headers
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(pageUrl).read()
  # print ("Connection Success!")
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          fName = ''

          # setting file name
          if len(title) > 0:
            fName = title
          else:      
            fName = soup.title.text
          f = open( directory + fName + '.html', 'w' )
    
          # adding link for next page
          nextLinkDiv = soup.find_all('div' , class_="next_chapter")
          if len(nextLinkDiv) > 0:
            nextLink = nextLinkDiv[0].find('a')
            nextLink['href'] = './' + str(int(title) + 1) + '.html'
            nextLink['target'] = '_self'
          #writing data to file
          #adding internal links
          innerLinks = soup.find_all('a')
          if len(innerLinks) > 0 :
            for link in innerLinks:
              if 'href' in link :
                if link['href'].find('#') >= 0:
                  link['href'] = '#' + link['href'].split('#')[1]
          
          f.write(str(soup))
          f.close()
          
          print ( 'Page ' + str(int(fName)+1) + ' Downloaded successfully!')
  except Exception as e:
      print ("Exception occurred while downloading " + fName + " Exception = ",e)
      traceback.print_exc()

# downloadPage('https://launchschool.com/books/command_line/read/introduction',title="0")
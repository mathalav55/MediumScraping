from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from pageDownload import downloadPage
import urllib.request
import cssutils
import logging
import os
#launch school scraping
rootDirectory = './LaunchBooks'

#url for books https://launchschool.com/books/

#get boooks list and run loop for each book
#steps for loop 
#1.create a directory for book name - master directory "Launch School" - sub - books
#2.for each page in the book create a html file
#3.Remove sidebar for each page - add a function in the page download
#4.Link the "next" to local page
headers = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'),
                          ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                          ('Connection', 'keep-alive')
                      ]
#download book
def downloadBook(bookUrl,title):
  cssutils.log.setLevel(logging.CRITICAL)
  opener = urllib.request.build_opener()
  bookUrl = bookUrl + '/read/introduction'
  directory = rootDirectory + '/' + title
  if( not os.path.isdir(directory)):
    os.makedirs(directory)
  #defining headers as some servers mandiate it
  opener.addheaders = headers
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(bookUrl).read()
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          div = soup.find('div',{'class' : 'next_chapter'})
          nextPage = bookUrl
          pageList = []
          pageList.append(nextPage)
          #run until there is next page
          while(div):            
            #get url for next page
            nextPage = 'https://launchschool.com' +  div.find('a')['href']
            pageList.append(nextPage)
            #read next page
            html_doc = urllib.request.urlopen(nextPage).read()
            #make soup
            soup = BeautifulSoup(html_doc, 'html.parser')
            #get link div
            div = soup.find('div',{'class' : 'next_chapter'})
          
          for i in range(0,len(pageList)):
            downloadPage(pageList[i],directory,str(i))
  except Exception as e:
      print ("Exception occurred = ",e)

    
#getting list of books
def downloadBooks():
  booksUrl = 'https://launchschool.com/books/'
  #folder to store all books
  if( not os.path.isdir(rootDirectory)):
    os.makedirs(rootDirectory)
  cssutils.log.setLevel(logging.CRITICAL)
  opener = urllib.request.build_opener()
  #defining headers as some servers mandiate it
  opener.addheaders = headers
  urllib.request.install_opener(opener)
  html_doc = urllib.request.urlopen(booksUrl).read()
  try :
          soup = BeautifulSoup(html_doc, 'html.parser')
          #get links for each book
          #identifier - 'books' outer div find 'a'
          booksDiv = soup.find("div",{"class" : 'books'})
          bookTags = booksDiv.find_all("a")
          bookTitles = booksDiv.find_all('span', { "class" : 'book-title'})
          for i in range(0,len(bookTags)):
            link = 'https://launchschool.com' + bookTags[i]['href']
            downloadBook(link,bookTitles[i].text)
         
  except Exception as e:
      print ("Exception occurred = ",e)


downloadBooks()

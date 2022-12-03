import requests
import string
from bs4 import BeautifulSoup

def getLinks(url_link):
  request = requests.get(url_link)
  Soup = BeautifulSoup(request.text, 'html.parser')

  links = []

  body = Soup.find_all('a')
  for link in body:
      if(len(links)) > 50: break

      # removing none links and # links
      if(str(link.get('href')).startswith('None') or str(link.get('href')).startswith('#')): continue
      # removing image links
      if(str(link.get('href')).endswith('.svg') or str(link.get('href')).endswith('.JPG')): continue
      # removing templates
      if 'Template' in str(link.get('href')): continue

      links.append('https://en.wikipedia.org/' + str(link.get('href')))

  return links
from queue import Queue
bfsq = Queue()

url_link = 'https://en.wikipedia.org/wiki/Science_fiction_film'

bfsq.put(url_link)

literally_all_links = []

while bfsq.empty() is not True:
  if len(literally_all_links) > 25: break 
  link = bfsq.get()
  literally_all_links.append(link)
  links = getLinks(link)
  for i in links:
    bfsq.put(i)
import json
heading_tags = ["h1", "h2", "h3"]

docs = []

for link in literally_all_links:
    headings = []
    subheadings = []
    paras = []

    request = requests.get(link)
    Soup = BeautifulSoup(request.text, 'html.parser')

    for tags in Soup.find_all('h1'): # replace 'h1' with heading_tags to get all headings instead of main title or vice versa :)
      # removing [edit] in end
      headings.append(tags.text.strip().replace('[edit]', ''))
    for tags in Soup.find_all('h2'): # replace 'h1' with heading_tags to get all headings instead of main title or vice versa :)
      # removing [edit] in end
      subheadings.append(tags.text.strip().replace('[edit]', ''))
    for para in Soup.find_all('p'): # replace 'h1' with heading_tags to get all headings instead of main title or vice versa :)
      paras.append(para.text.replace('\n', ''))

    doc = {}
    doc['headings'] = headings
    doc['subheadings'] = subheadings
    doc['paras'] = paras

    docs.append(doc)
dataset = json.dumps(docs,indent = 3)
with open('scrapped2.json','w') as json_file:
	json.dump(dataset,json_file)

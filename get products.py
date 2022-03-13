import os
from urllib.request import Request, urlopen
from urllib.error import URLError
import requests, wget, re
from time import sleep
from conf import *
from pathlib import Path

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


# you can also import SoftwareEngine, HardwareType, SoftwareType, Popularity from random_user_agent.params
# you can also set number of user agents required by providing `limit` as parameter

software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   

user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

# Get list of user agents.
user_agents = user_agent_rotator.get_user_agents()

# Get Random User Agent String.
user_agent = user_agent_rotator.get_random_user_agent()
#print(user_agent)

def handle_req(url, data=None, download=False):
   req = Request(url, headers={'User-Agent':user_agent_rotator.get_random_user_agent(),
                              'accept':'text/html;q=0.8,application/signed-exchange;v=b3;q=0.9',
                              'accept-language':'en-US,en;q=0.9'})
   try:
      response = urlopen(req)
   except URLError as e:
      if hasattr(e, 'reason'):
         print('We failed to reach a server.')
         print('Reason: ', e.reason)
      elif hasattr(e, 'code'):
         print('The server couldn\'t fulfill the request')
         print('Error code:', e.code)
   else:
      try:
         if response.headers.get_content_charset() == 'utf-8':
            webpage_as_string = response.read().decode(response.headers.get_content_charset(), "ignore")
         else:
            webpage_as_string = response.read().decode(response.headers.get_content_charset(), "ignore")
      except UnicodeEncodeError as e:
         print(e)
         webpage_as_string = response.read()
      #print(webpage_as_string)
      #print(response.headers.get_content_charset())
      
      if download == True:
         filename = url.split('//')[1].split('/')[0]
         with open(filename+'.txt', 'wb') as f:
            f.write(webpage_as_string.encode('ascii', 'ignore'))

      return webpage_as_string
   return None


def get_files_direct_from_webpage(url_input, search_str='.mp3'):

   base_url = '/'.join(url_input.split('/')[0:3])
   webpage_str = handle_req(url_input, download=True)
   found_indexes = [m.start() for m in re.finditer(search_str, webpage_str)]

   print("URL Input: ", url_input)
   for i in found_indexes:
      webslice = webpage_str[i-75:i+100]
      #print(webslice.split("'")[1])

      filename_start = webslice.find('src')
      if filename_start == -1:
         continue

      filename = webslice[filename_start:].split('src=')[1][1:] + search_str
      if "'" in filename:
         filename = filename.split("'")[0]
      #print(filename)

      if 'bensound-music/' in filename:
         url = base_url + filename 
         fout_name = filename.split('bensound-music/')[1]
      elif 'https://static.pexels.com/lib/videos/free-videos.mp4' in filename:
         continue
      else:
         url = filename
         fout_name = filename.split('external/')[1]
         if "?" in fout_name:
            fout_name = fout_name.split('?')[0]
      
      print("     Downloading: ", url)
      r = requests.get(url)
      with open(fout_name, 'wb') as f:
         f.write(r.content)
      sleep(3)


def get_pictures_from_alixpress(url_input):
   img_url_list = []

   print("URL Input: ", url_input)
   filename_base = url_in.split('/')[4].split('.')[0]
   print("File base name: ", filename_base)
   
   base_url = '/'.join(url_input.split('/')[0:3])
   print("Base Url: %s" %base_url)
   
   webpage_str = handle_req(url_input, download=True)

   found_indexes = [m.start() for m in re.finditer('"skuPropertyImagePath"', webpage_str)]

   if len(found_indexes) != 0:
      #print(found_indexes)
      for i in found_indexes:
         webslice = webpage_str[i+24:i+2048] #max url length
         img_url = webslice[:webslice.find('_640x640.jpg"')]
         #print(img_url)
         img_url_list.append(img_url)

   else:
      found_indexes = [m.start() for m in re.finditer('"imagePathList"', webpage_str)]
      #print(found_indexes)
      for i in found_indexes:
         webslice = webpage_str[i+16:i+2048] #max url length
         #print(webslice)
         img_url_list = eval(webslice[:webslice.find(']')+1])
         #print(img_url_list)



   for i in range(1, len(img_url_list)+1):
      print("     Downloading: ", img_url_list[i-1])
      r = requests.get(img_url_list[i-1])

      #make new folder for item name

      foldername = img_url_list[i-1].split("/")[5].split(".jpg")[0] 
      meta_tags = ",".join(foldername.split("-"))
      #foldername = "".join([c for c in foldername if c.isalpha() or c.isdigit() or c==' ']).rstrip() #makes any string filesafe
      folderpath = os.path.join(DROPSHIP_DIR, filename_base)
      filename = os.path.join(folderpath,filename_base+'-'+str(i)+'.jpg')
      

      path = Path(folderpath)
      if not os.path.exists(path.parent):
         os.mkdir(path.parent)
         print("Created: %s" %path.parent)

      elif not os.path.exists(folderpath):
         os.mkdir(folderpath)
         print("Created: %s" %folderpath)


      with open(os.path.join(folderpath,'link.txt'),'w') as f:
         f.write(url_input)

      with open(os.path.join(folderpath,'meta-tags.txt'),'w') as f:
         f.write((meta_tags))


      if not os.path.exists(filename):
         with open(filename, 'wb') as f:
            f.write(r.content)
         #sleep(1)


               #url_input = 'https://www.bensound.com/royalty-free-music/corporate-pop'
               #get_files_direct_from_webpage(url_input, search_str='.mp3')
               #get_files_direct_from_webpage(url_input, search_str='.mp4') 
while True:
   url_in = input("URL? :") #handle_req(url_in, download=True)
   #url_in = 'https://www.aliexpress.com/item/32961446795.html'
   get_pictures_from_alixpress(url_in)
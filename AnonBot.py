import os
import sys
from bs4 import BeautifulSoup
import time
from selenium import webdriver


class Bot:
	def __init__(self):
                self.keyword_list = ['@gmail', '@yahoo', 'a'] # Sample words, change it
                
                self.profile = webdriver.FirefoxProfile()
                
                self.profile.set_preference('network.proxy.type', 1)
                self.profile.set_preference('network.proxy.socks', '127.0.0.1') #Tor proxy
                self.profile.set_preference('network.proxy.socks_port', 9050) #Tor control port
                
                self.browser = webdriver.Firefox(self.profile, executable_path='/home/salas/geckodriver') # you need to change executable_path to your geckodriver path
 
	def closeBrowser(self):
		self.browser.close()

	def requestLinks(self):
		self.browser.get("https://pastebin.com/archive")

	def scrapeLinks(self):
		self.links = []
		parser = BeautifulSoup(self.browser.page_source, 'html.parser')
		for i in parser.find('table').findAll('a'):
			if '/archive/' not in i.get('href') and i not in self.links:
				self.links.append(i.get('href'))

	def donwloadPastes(self, counter=0):
		folder = 'session'  # folder to save pastes
		if os.path.exists(folder):
			pass
		else:
			os.mkdir(folder)

		download_list = open('list.txt', 'r+')
		for url in self.links:
			download_list.seek(0)
			if url + '\n' not in download_list:
				self.browser.get("https://pastebin.com/raw" + url)
				time.sleep(2) #time to sleep to avoid ip ban, you can change it

				for keyword in self.keyword_list:
					text = self.browser.find_element_by_tag_name('body').text
					counter = counter + text.count(keyword)  # search if keywords in file

				if counter > 4:
					# descargar()
					with open('{}/{}'.format(folder, '{} {} {}'.format(time.strftime("%d_%b_%Y_%H_%M"), str(counter), url.strip('/'))), 'wb') as file: # if you use windows you have to chage '{}/{} to '{}\{}'
						file.write(text.encode('utf-8'))

					download_list.write(url + '\n')
					print(url, '\033[1;32;40mDOWNLOADED\033[1;37;40m', ' ', counter, 'keywords')
					counter = 0

				else:
					# no to download
					download_list.write(url + '\n')
					print(url, 'NO KEYWORDS')
			else:
				# no to download
				print(url, 'SCRAPED BEFORE')
				time.sleep(1)


scraper = Bot()
scraper.requestLinks()
input('SOLVE THE CAPTCHA AND HIT ENTER')
scraper.scrapeLinks()
scraper.donwloadPastes()

while True:
	print('------------------------------')
	scraper.requestLinks()
	scraper.scrapeLinks()
	scraper.donwloadPastes()



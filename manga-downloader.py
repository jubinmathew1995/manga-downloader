# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# 	manga-downloader.py
#
# 	Created by: Jubin George Mathew
#
# 	A simple web scraping program that helps to download 
# 	collections of manga (comics) from mangapanda site.
# ----------------------------------------------------------

import os	# cls and clear-screen interface
import sys	# basic system api.
import socket	# checking network-conn.
import requests	# requesting webpages.
from bs4 import BeautifulSoup	# scraping 

# Url for checking the network connection.
REMOTE_SERVER = "www.google.com"

# url for requesting the data.
url = 'http://www.mangapanda.com/'

# list of manga comics.
anime_list = ['', 'bleach','naruto', 'nanatsu-no-taizai', 'one-piece', 'hunter-x-hunter']

# pointer to the corresponding anime series.
index = -1


def check_network_conn():
	"""
		Used to check whether the internet connection.
	"""
	try:
		host = socket.gethostbyname(REMOTE_SERVER)
		s = socket.create_connection((host, 80), 2)
		return True
	except socket.error as err:
		pass
	return False


def choose_manga(index):
	"""
		used to choose the manga from the list.
	"""
	while index == -1:
		# any message.
		print("\nSelect the manga to download\n")

		# This is to display the list of manga available to download.
		for i in range(1,len(anime_list)):
			print(str(i)+'. '+anime_list[i])

		# This block is to check weather input given is a integer or not.
		try:
			index = int(input("\nSelect the choice [1-%d]: "%(len(anime_list)-1)))
		except ValueError:
			index = -1

		# for clearing the screen acc to your system platform(unix or windows).
		os.system('cls' if os.name == 'nt' else 'clear')

		# check if the input given is in the appropriate range or not.
		if index<=0 or index>(len(anime_list)-1):
			index = -1
			print("\n***INVALID option. Try Again.***")
	return index


if __name__ == '__main__':

	# check if internet connection is there or not.
	if not check_network_conn():
		print("No internet connection !!!")
		sys.exit()

	# choose which anime manga to download
	index = choose_manga(index)

	# create the mangapanda url for the anime.
	animeURL = url + anime_list[index]

	# used to store the starting and ending chapter number for the 
	# selected manga.
	start_chapter_no = 1
	end_chapter_no = -1

	# used to get the list of all the chapters for the manga.
	page = requests.get(animeURL)
	soup = BeautifulSoup(page.text, 'lxml')
	latestChapter = soup.find("table", {"id": "listing"})
	end_chapter_no = len(latestChapter.find_all("tr"))

	# create the directory for the manga.
	os.mkdir( anime_list[index] )

	# loop over all the chapters.
	for i in range(start_chapter_no, end_chapter_no):
		# create directory for individual each chapter.
		folder_name = anime_list[index] + "/%s-"%anime_list[index] + "{0:0=3d}".format(i) 
		os.mkdir( folder_name )

		# for logging purpose
		print("\nDownloading chapter {0:0=3d}".format(i))

		# os.mkdir(anime_list[index]+'/'+str(i))
		# fetch the chapter starting page for fetching the 
		# page details.
		page = requests.get(animeURL+"/%d"%i)
		soup = BeautifulSoup(page.text, 'lxml')
		end_page_no = len(soup.find('select',{"id":"pageMenu"}).find_all('option'))

		# loop over all the pages in the selected chapter.
		for j in range(1,end_page_no+1):
			# request each page and get the image url.
			page=requests.get(animeURL+"/%d/%d"%(i,j))
			soup=BeautifulSoup(page.text,'lxml')
			img_container = soup.find("div", {"id": "imgholder"})
			lnk = img_container.select("img[src^=http]")[0]["src"]

			# download the appropriate url in the directory.
			file_name = folder_name + '/' + "{0:0=3d}".format(j) 
			with open(file_name,"wb") as f:
				f.write(requests.get(lnk).content)
import requests
import urllib
from bs4 import BeautifulSoup



def init_google(query, numberOfArticles):

	r = requests.get('https://www.google.com/search?q=' + str(query))
	soup = BeautifulSoup(r.text, "html.parser")

	links = []
	for item in soup.find_all('h3', attrs={'class' : 'r'}): #Scrapes Google frontpage
		links.append(item.a['href'][7:]) # [7:] strips the /url?q= prefix
	links = links[0:numberOfArticles]
	return links





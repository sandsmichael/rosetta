
from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment
import urllib.request


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False

    return True



def init(link):
	print('Scraping Text from Article Links: ' + link)
	try:
		html = urllib.request.urlopen(link).read()
		strainer = SoupStrainer('body')
		soup = BeautifulSoup(html, 'lxml',parse_only=strainer)

	# Remove ALL Links
		for a in soup.findAll('a'):
			a.decompose()

	# (MarketWatch)
		for head in soup.findAll('header'):
			head.decompose()
		for foot in soup.findAll('footer'):
			foot.decompose()
		for pub in soup.findAll('p', {'id':'published-timestamp'}):
			pub.decompose()
		for img in soup.findAll('img'):
			img.decompose()
		for fig in soup.findAll('figure'):
			fig.decompose()
	# (NYT)
		for load in soup.findAll('div', {'class':'loader-container'}):
			load.decompose()
	# (CNN)
		for justwatch in soup.findAll('h3', {'class':'cd__headline-title'}):
			justwatch.decompose()
		for mustwatch in soup.findAll('h4', {'class':'video__end-slate__tertiary-title'}):
			mustwatch.decompose()
		for paid in soup.findAll('h2', {'data-analytics':"Paid Partner Content_list-xs_"}):
			paid.decompose()


		texts = soup.findAll(text=True)

		visible_texts = filter(tag_visible, texts)

		xx =  u" ".join(t.strip() for t in visible_texts)
	except:
		xx = 'null:http error 500 - scrapewebtext'
	return xx


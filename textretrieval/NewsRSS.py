'''
Created on Jul 8, 2017

@author: micha
'''

'''
Created on Mar 27, 2017

@author: michael sands
'''
from bs4 import BeautifulSoup
import feedparser
import csv
import re 

maxArticles = 3
#Function to fetch the rss feed and return the parsed RSS
def parseRSS( rss_url ):
    return feedparser.parse( rss_url ) 
    
# Function grabs the rss feed headlines (titles) and returns them as a list
def getTagInfo (rss_url, key, type):
    link = []
    title = []
    summary = []
    titlelist = []
    linklist = []
    sourcelist = []
    summarylist = []
    publishedlist = []
    publisherlist = []
    
    myfeed = parseRSS( rss_url )



    #use feedparser to retrieve data from feed
    try:
        publishedlist.append(myfeed.feed.published)
    except(AttributeError):
        publishedlist.append('x.x.x')




    for newsitem in myfeed['items']:
        title.append(newsitem['title'])
        summary.append(BeautifulSoup(newsitem['summary'], 'html.parser') )#'lxml').text Beautifulsoup.text cleans the html tags from the text
        link.append(newsitem['link'])





    try:
        soup = BeautifulSoup(newsitem['summary'])
        image_url = soup.find('img')['src']
    except(TypeError):
        image_url = ''






    #add retrieved feed data to lists         
    for i in range(maxArticles):
        titlelist.append(title[i])
        linklist.append(link[i])
        summarylist.append(summary[i])

        publisher_index = key.find('_')
        publisher = key[0:publisher_index]
        publisherlist.append(publisher)

        sourcelist.append(key)





    # publisher list



    if type == 'title':
        return titlelist
    if type == 'source':
        return sourcelist
    if type == 'rsssummary':
        return summarylist
    if type == 'publisheddate':
        return publishedlist
    if type == 'publisher':
        return publisherlist
    elif type == 'link':
        return linklist



    
fulltitlelist = []
fulllinklist = []
fullsourcelist = []
fullsumlist = []
fullpublishedlist =[]
fullpublisherlist = []
# List of RSS feeds that we will fetch and combine



def start_rss():


    print('Initializing RSS')
    newsurls = {
        'Fox_Politics':'http://feeds.foxnews.com/foxnews/politics',
        'NewYorkTimes_US_Politics':'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
        'MarketWatch_Breaking_News': 'http://feeds.marketwatch.com/marketwatch/bulletins',
        'CNN_World_News':'http://rss.cnn.com/rss/cnn_world.rss',
        'NewYorkTimes_World_News':'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        'CNN_Top_Stories':'http://rss.cnn.com/rss/cnn_topstories.rss',
        'MarketWatch_Top_Stories':  'http://feeds.marketwatch.com/marketwatch/topstories/',
        'Fox_Latest_Headlines':'http://feeds.foxnews.com/foxnews/latest',

    }



    # Iterate over the urls to retrieve data and append the master arrays with the retrieved data
    for key,url in newsurls.items():
        fulltitlelist.extend( getTagInfo (url, key, 'title'))
        fulllinklist.extend( getTagInfo (url, key, 'link'))
        fullsourcelist.extend( getTagInfo (url, key, 'source'))
        fullsumlist.extend( getTagInfo (url, key, 'rsssummary'))
        fullpublisherlist.extend(getTagInfo(url,key,'publisher'))


    return (fulltitlelist, fulllinklist, fullsourcelist, fullpublisherlist)
    #return a list that alternates title and then link so it can be looped in one statement in
    #the newsrss html file to insert title and link and summary images in seperate column on same row.
    #also get the source of the document











#WRITE TO FILE

    # myfile = open(out_path,'wt')
    # writer = csv.writer(myfile, delimiter=',', quotechar='"')
    # for i in range(len(fulltitlelist)):
    #     try:
    #         writer.writerow([fulltitlelist[i] + '  ' +fulllinklist[i]])
    #         myfile.flush() 
    #     except(UnicodeEncodeError):
    #         writer.writerow('')
    
    # myfile.close() 



#SEARCH HEADLINE FOR KEYWORD
    # headline_overview = [] 
    # length = len(fulltitlelist)
    # for i in range(length):
    #     headline_overview.append(fulltitlelist[i])
 
    # #ticker specefific analysis

    # # def search_headlines(ticker):
    # #     for i in range(len(headline_overview)):   
    # #         if ticker in headline_overview[i]:
    # #             print('yes ', i)
    # #             print(headline_overview[i])      
    # # search_headlines('Tesla')
    # # #SEND KEYWORD IN as ticker
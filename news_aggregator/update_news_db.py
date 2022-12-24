import feedparser
import pandas as pd
import hashlib
import os
import sqlite3 as sqlite


# identifying the current directory.
curr_dir = os.path.dirname(os.path.abspath(__file__))

# news' attributes that we're interested in storing them.
news_attributes = ['published', 'link', 'title', 'summary', 'author']

# setting db related parameters.
# todo: moving this parameters to a config. file.
db_name = 'news_db.sqlite'
news_table_name = 'news_articles'
db_folder = 'data'
db_folder = os.path.join(curr_dir, db_folder)

# create db folder if not exist.
if not os.path.exists(db_folder):
    os.makedirs(db_folder)


# function to generate a unique id fo each news.
def generate_news_id(news_link):
    news_link = news_link.encode('utf-8')
    news_id = hashlib.sha256(news_link).hexdigest()
    return news_id
    
    

def get_feeds_urls():
    feeds_urls = {    'Fox Politics': 'http://feeds.foxnews.com/foxnews/politics'
                    , 'NewYorkTimes US Politics': 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'
                    , 'MarketWatch Breaking News': 'http://feeds.marketwatch.com/marketwatch/bulletins'
                    , 'CNN World News': 'http://rss.cnn.com/rss/cnn_world.rss'
                    , 'NewYorkTimes World News': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml'
                    , 'CNN Top Stories': 'http://rss.cnn.com/rss/cnn_topstories.rss'
                    , 'MarketWatch Top Stories': 'http://feeds.marketwatch.com/marketwatch/topstories/'
                    , 'Fox Latest Headlines': 'http://feeds.foxnews.com/foxnews/latest'
                 }    
    return feeds_urls



# function to fetch news from different feeds.
def get_news(news_attributes):
    # this list containes all fetched news articles.
    news_articles = []
    
    feeds_urls = get_feeds_urls()
    
    # iterating over all feeds urls, processing currently published news and storing them.
    for key, url in feeds_urls.items():
        print('Processing ' + key + ' feed!')
        news_feed = feedparser.parse(url)
        for entry in news_feed['entries']:
            news = []
            for attr in news_attributes:
                try:
                    news.append(entry[attr])
                except(KeyError):
                    # there is no value for this attribute.
                    news.append('')
            
            # generating a unique id for each news piece.
            news_id = generate_news_id(entry['link'])
            # adding the generated id to the news' attributes.
            news = [news_id] + news
            # appending the processed news to the list
            news_articles.append(news)
    
    # coverting the list to dataframe
    cols = ['id_'] + news_attributes
    df = pd.DataFrame(news_articles, columns = cols)
    
    # dropping duplicate news
    df = df[~df.duplicated()]
    
    return df



# get the connection to the db. If db not exist, will be created.
def get_db_conn(db_folder, db_name):
    conn = sqlite.connect(os.path.join(db_folder, db_name), isolation_level = None)
    return conn



# function to create the table for storing news articles. If table exists does nothing.
def create_news_table(news_table_name, news_attributes):
    conn = get_db_conn(db_folder, db_name)
    cur = conn.cursor()    
    q = 'id_ TEXT'
    for attr in news_attributes:
        q = q + ', ' + attr + ' TEXT'
    
    q = ' (' + q + ')'    
    create_table_query = 'CREATE TABLE IF NOT EXISTS ' + news_table_name + q
    cur.execute(create_table_query)
    conn.commit()
    cur.close()
    conn.close()


# function to update db with new news articles.
def update_db():
    create_news_table(news_table_name, news_attributes)
    conn = get_db_conn(db_folder, db_name)    
    news_df = get_news(news_attributes)
    news_df.to_sql(name = news_table_name, con = conn, if_exists = 'append', index = False)
    conn.commit()
    conn.close()


# function to remove duplicate news from news table.
def remove_duplicate_news():
    print('Removing duplicate news...')
    conn = get_db_conn(db_folder, db_name)
    cur = conn.cursor()
    # checking for any duplicated news in news table.
    drop_duplicates_query = 'DELETE FROM ' + news_table_name + ' WHERE rowid NOT IN (SELECT min(rowid) FROM ' + news_table_name + ' GROUP BY id_)'
    cur.execute(drop_duplicates_query)
    cur.execute("VACUUM")
    conn.commit()
    cur.close()
    conn.close()
    


if __name__ == '__main__':
    
    update_db()
    remove_duplicate_news()

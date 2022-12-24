from collections import OrderedDict
from bs4 import BeautifulSoup
import multiprocessing
import pandas as pd
import numpy as np
import gensim
from gensim import utils
from gensim.corpora import Dictionary
from gensim.models import LdaMulticore
from gensim.models.phrases import Phrases, Phraser
from gensim.parsing.preprocessing import strip_punctuation, strip_multiple_whitespaces, strip_numeric
import os, gc, logging

logging.basicConfig(format = '%(asctime)s : %(levelname)s : %(message)s', level = logging.INFO)

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# loading the news dataset. 
# todo: this function is customized for the current dataset
# and needs to be adjusted for the final dataset.
def load_news_data(file):
    print('Loading news dataset.')
    news_df = pd.read_pickle(file).loc[:, ['title', 'article_text']]
    news_df.replace('', np.nan, inplace = True)
    news_df.dropna(inplace = True)
    return news_df



# removing 'html' tags from each document.
def parse_html(doc):
    if doc is not None:
        doc = BeautifulSoup(doc, 'html5lib').text
    return doc



# calculating the length of each article and only keeping those articles with
# a length greater than 'min_article_len'
def trim_news_df(news_df, min_article_len):
    news_df = news_df.copy()
    news_df['article_length'] = news_df['article_text'].apply(lambda x:len(x.split(' ')))
    news_df = news_df[news_df['article_length'] > min_article_len]    
    news_df.replace('', np.nan, inplace = True)
    news_df.dropna(inplace = True)
    news_df.drop(columns = ['article_length'])
    news_df = news_df.reset_index(drop = True)
    return news_df



def load_stop_words(add_capitalized_words = True):
    """
    add_capitalized_words: specifies if another version of stop words with the first
    letter capitalized should be appended to the initial list of stop words.
    """
    stop_words = pd.read_csv('stop_words.csv')
    stop_words = stop_words.loc[:, 'words'].values.tolist()
    
    if add_capitalized_words:
        stop_words_capitalized = [word.capitalize() for word in stop_words]
        stop_words = stop_words + stop_words_capitalized
    
    return stop_words



def remove_stop_words(s):    
    s = utils.to_unicode(s)
    return " ".join(w for w in s.split() if w not in stop_words)



def process_doc(doc, drop_stop_words = True):
    """
    drop_stop_words: specifies if commonly used words should be dropped or not.
    """
    if doc is not None:
#        doc = doc.lower()
        doc = strip_punctuation(doc)
        doc = strip_multiple_whitespaces(doc)
        doc = strip_numeric(doc)
        
        if drop_stop_words:
            doc = remove_stop_words(doc)
        
        doc = gensim.utils.simple_preprocess(doc, min_len = 3, max_len = 30)        
    
    return doc



def generate_corpus(data_frame, drop_stop_words = True):
    """
    data_frame: a data frame in which all the columns have important textual data.
    drop_stop_words: specifies if commonly used words should be dropped or not.
    """
    
    for i, row in data_frame.iterrows():        
        
        # displaying the progress.
        if (i+1) % 1000 == 0:
            print('{}/{} documents have been processed!'.format((i+1), len(data_frame)))
        
        # it's assumed that all the columns of the data frame contain 
        # important textual data. So they will be aggregated in a single string.
        doc = ' '.join(row.tolist())
        if doc is not None:
            doc = process_doc(doc, drop_stop_words)            
            yield doc



# phrase's score calculation based on original word2vec paper.
def phrase_scorer_word2vec(worda_count, wordb_count, bigram_count
                           , len_vocab, min_count, corpus_word_count):
    """
    worda_count: number of occurrences of the first token in the phrase being scored
    wordb_count: number of occurrences of the second token in the phrase being scored
    bigram_count: number of occurrences of the phrase being scored
    len_vocab: the number of unique tokens in corpus
    min_count: ignore all bigrams with the total count lower than this value
    corpus_word_count: the total number of non-unique tokens in corpus

    """
    score = (bigram_count - min_count) / worda_count / wordb_count * len_vocab
    return score



# phrase's score calculation based on raw frequency of each bigram.
def phrase_scorer_raw_freq(worda_count, wordb_count, bigram_count
                           , len_vocab, min_count, corpus_word_count):
    """
    worda_count: number of occurrences of the first token in the phrase being scored.
    wordb_count: number of occurrences of the second token in the phrase being scored.
    bigram_count: number of occurrences of the phrase being scored.
    len_vocab: the number of unique tokens in the corpus.
    min_count: ignore all bigrams with the total count lower than this value.
    corpus_word_count: the total number of non-unique tokens in the corpus.

    """
    score = bigram_count
    return score



# build a model to detect phrases based on collocation counts.
def build_corpus_bigram_model(data_frame, use_common_terms = False
                              , min_count = 20, threshold = 20
                              , scorer = phrase_scorer_word2vec):    
    """
    data_frame: a data frame in which all the columns have important textual data.
    use_common_terms: common terms will be used to allow the phraser model to detect
    expressions like 'bank_of_america' or 'eye_of_the_beholder' as bigrams.
    
    scorer: a function that specifies how potential phrases are scored.
    min_count: ignore all bigrams with the total count lower than this value.
    threshold: accepted phrase if the score of the phrase is greater than threshold. 
    """
    
    # corpus containing processed and tokenized documents.
    corpus = list(generate_corpus(data_frame, drop_stop_words = not use_common_terms))
    
    if use_common_terms:
        common_terms = load_stop_words(add_capitalized_words = False)
        bigram_model = Phrases(corpus
                               , min_count = min_count
                               , threshold = threshold
                               , scoring = scorer
                               , common_terms = common_terms)
    else:
        bigram_model = Phrases(corpus
                               , min_count = min_count
                               , threshold = threshold
                               , scoring = scorer)
    
    # cut down memory consumption of the model   
    bigram_model = Phraser(bigram_model)
    return corpus, bigram_model



def build_dict(corpus, trim = True):
    print('Building the dictionary...')
    dct = Dictionary(corpus)
    
    # Remove words that occur too frequently or too rarely.
    if trim:
        max_word_freq = 0.70
        min_word_count = 20
        dct.filter_extremes(no_below = min_word_count
                            , no_above = max_word_freq
                            , keep_n = 1000000)
    print('The dictionary is built.')
    return dct



def train_lda_model(corpus_bow, total_num_topics):
    lda_model = LdaMulticore(corpus = corpus_bow
                             , num_topics = total_num_topics
                             , id2word = dct
                             , workers = multiprocessing.cpu_count()
                             , chunksize = 50000 # num of docs loaded in memory
                             , passes = 30
                             , batch = False
                             , alpha = 'symmetric' # can be 'symmetric' or 'auto'
                             , eta = None
                             , decay = 0.5
                             , offset = 1.0
                             , eval_every = 10
                             , iterations = 50
                             , gamma_threshold = 0.001
                             , random_state = 1
                             , minimum_probability = 0.01
                             , minimum_phi_value = 0.01
                             , per_word_topics = False
                             )
    return lda_model



def topic_word_map(lda_model, num_words = 15):
    topics_words = lda_model.show_topics(num_topics = lda_model.num_topics, num_words = num_words, formatted = False)
    topics_words = [(tp[0], [wd[0] for wd in tp[1]]) for tp in topics_words]
    topics_words = sorted(topics_words, key = lambda x:x[0], reverse = False)    
    topics_words = pd.DataFrame(topics_words, columns = ['topic', 'words'])
    return topics_words



# predicting the topics of each doc along with the probability of each topic.
def predict_doc_topics(lda_model, doc, doc_num_topics = 3):
    """
    doc_num_topics: number of topics to be predicted for each document.
    """
    lda_vec = lda_model.get_document_topics(doc)
    lda_vec = sorted(lda_vec, key = lambda x:x[1], reverse = True)
    lda_vec = lda_vec[:doc_num_topics]
    topics = list(OrderedDict(lda_vec).keys())
    probs = list(OrderedDict(lda_vec).values())    
    pad = doc_num_topics - len(lda_vec)    
    topics = topics + [-1] * pad
    probs = probs + [0] * pad 
    return list(zip(topics, probs))



# predicting the topics of all the documents in bag of words corpus.
def predict_corpus_topics(lda_model, corpus_bow, doc_num_topics):
    i = 0
    topics_probs = []    
    for doc in corpus_bow:  
        # displaying the progress.
        if (i+1) % 1000 == 0:
            print('{}/{} documents have been processed!'.format((i+1), len(corpus_bow)))
        
        tp_pr = predict_doc_topics(lda_model, doc, doc_num_topics)
        topics_probs.append(tp_pr)
        i = i + 1    
    
    topics_probs_df = pd.DataFrame(topics_probs)    
    cols = ['topic{}'.format(i) for i in range(doc_num_topics)]
    topics_probs_df.columns = cols
    return topics_probs_df



stop_words = load_stop_words()

if __name__ == '__main__':
    
    news_file = 'sampl_news_dataset.pkl'
    news_df = load_news_data(news_file)
    
    print('Parsing html tags of news articles.')
    news_df['article_text'] = news_df['article_text'].apply(parse_html)
    gc.collect()
    
    # removing duplicated news articles.
    print('Trimming news dataset.')
    news_df = news_df[~news_df['article_text'].duplicated()]
    
    # trimming the news dataset and removing articles with word-count length
    # less than 'min_article_len'.
    min_article_len = 150
    news_df = trim_news_df(news_df, min_article_len)    
    
    # generating a tokenized and processed corpus from the news dataset and
    # building a bigram model using the corpus.
    print('Generating the corpus and building the bigram model.')
    corpus, bigram_model = build_corpus_bigram_model(news_df.loc[:, ['title', 'article_text']])
    
    # detecting bigrams in the corpus and joining them.
    corpus = [bigram_model[corpus[i]] for i in range(len(corpus))]
    
    # building the dictionary using the final corpus.
    dct = build_dict(corpus, trim = True)
    
    # converting the corpus of terms to their bag of words representations.
    corpus_bow = [dct.doc2bow(line) for line in corpus]
    
    # building and training the lda model.
    # total number of latent topics to be extracted from the corpus.
    total_num_topics = 80
    lda_model = train_lda_model(corpus_bow, total_num_topics)
    
    # saving the model on the disk.
    model_file = 'lda_model_{}_topics'.format(total_num_topics)
    lda_model.save(model_file)
    
    # generating and saving a csv file that maps each topic to its associated words.
    print('Saving topics words map in csv format on the disk.')
    topics_words_map_df = topic_word_map(lda_model, num_words = 20)
    topics_words_map_df.to_csv('topics_words_map_{}topics.csv'.format(total_num_topics), index = False)
    
    # using the previously trained lda model to predict most probable topics for 
    # each news article in the corpus. The final predictions and their probabilities
    # will be saved on the disk in csv format.
    print('Predicting topics for news articles.')
    # the maximum number of topics we would like to predict for each doc.
    doc_num_topics = 10
    topics_probs_df = predict_corpus_topics(lda_model, corpus_bow, doc_num_topics)
    topics_probs_df['title'] = news_df.loc[:, 'title'].reset_index(drop = True)
    topics_probs_df['article_text'] = news_df.loc[:, 'article_text'].reset_index(drop = True)
    print('Saving the articles\' predicted topics in csv format on the disk.')
    topics_probs_df.to_csv('articles_topics_probs_{}topics.csv'.format(total_num_topics), index = False)






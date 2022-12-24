

from normalization import normalize_corpus
import nltk
from operator import itemgetter


#ngrams

def flatten_corpus(corpus):
    return ' '.join([document.strip() 
                     for document in corpus])
                         
def compute_ngrams(sequence, n):
    return zip(*[sequence[index:] 
                 for index in range(n)])


def get_top_ngrams(corpus, ngram_val=1, limit=5):

    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)

    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(), 
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq) 
                     for text, freq in sorted_ngrams]

    return sorted_ngrams   
    


def init_ngram_keyphrases(ngrams, text):
  import analytic_normalization as aNorm
  norm_text = normalize_corpus(text, lemmatize=False)
  if ngrams == 2:
    bi = get_top_ngrams(corpus=norm_text, ngram_val=2,limit=5)
    bigramlist = []
    for item in bi:
        k,v = item
        word = aNorm.remove_special_characters(k)
        word2 = word.replace("”", "")
        word3 = word2.replace("“", "")
        word4 = word3.replace("’", "")
        word5 = word4.replace("u ", "")
        bigramlist.append(word5.strip())
    # from nltk.collocations import BigramCollocationFinder
    # from nltk.collocations import BigramAssocMeasures
    # finder = BigramCollocationFinder.from_documents([item.split() for item in norm_text])
    # bigram_measures = BigramAssocMeasures()                                                
    # y = finder.nbest(bigram_measures.raw_freq, 5)
    # z = finder.nbest(bigram_measures.pmi, 5)   

    return bigramlist


  elif ngrams == 3:                
    tri = get_top_ngrams(corpus=norm_text, ngram_val=3,limit=10)
    
    from nltk.collocations import TrigramCollocationFinder
    from nltk.collocations import TrigramAssocMeasures

    finder = TrigramCollocationFinder.from_documents([item.split() 
                                                    for item 
                                                    in norm_text])
    trigram_measures = TrigramAssocMeasures()                                                
    y = finder.nbest(trigram_measures.raw_freq, 10)
    z = finder.nbest(trigram_measures.pmi, 10)  

    return tri








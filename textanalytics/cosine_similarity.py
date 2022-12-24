

from analytic_normalization import normalize_corpus
from analytic_utils import build_feature_matrix
import numpy as np

def init_cosine(articlesCorpus, article_link):
    queryTitle = ''
    textCorpus = []

    for k,v in articlesCorpus.items():
        if v[0] == article_link:
                queryTitle = k
        textCorpus.append(v[4])


    toy_corpus = textCorpus
    query_docs = [queryTitle]


    # normalize and extract features from the toy corpus
    norm_corpus = normalize_corpus(toy_corpus, lemmatize=True)
    tfidf_vectorizer, tfidf_features = build_feature_matrix(norm_corpus,
                                                            feature_type='tfidf',
                                                            ngram_range=(1, 1), 
                                                            min_df=0.0, max_df=1.0)
                                                            
    # normalize and extract features from the query corpus
    norm_query_docs =  normalize_corpus(query_docs, lemmatize=True)            
    query_docs_tfidf = tfidf_vectorizer.transform(norm_query_docs)

    cosineDict = {}
    for index, doc in enumerate(query_docs):
        doc_tfidf = query_docs_tfidf[index]
        top_similar_docs = compute_cosine_similarity(doc_tfidf,
                                                 tfidf_features,
                                                 top_n=5)
        for doc_index, sim_score in top_similar_docs:
            score = sim_score
            documentText = toy_corpus[doc_index]
            for k,v in articlesCorpus.items():
                if k not in query_docs:
                    if v[4] == documentText:
                        cosineDict[k] = score
 
    import operator
    cosineDictSorted = sorted(cosineDict.items(), key=operator.itemgetter(1))                                              
    return cosineDictSorted

        






def compute_cosine_similarity(doc_features, corpus_features,top_n=5):
    # get document vectors
    doc_features = doc_features[0]
    # compute similarities
    similarity = np.dot(doc_features, 
                        corpus_features.T)
    similarity = similarity.toarray()[0]
    # get docs with highest similarity scores
    top_docs = similarity.argsort()[::-1][:top_n]
    top_docs_with_score = [(index, round(similarity[index], 3))
                            for index in top_docs]
    return top_docs_with_score

    















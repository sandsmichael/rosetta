from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

def build_feature_matrix(documents, feature_type='frequency'):
    feature_type = feature_type.lower().strip()  

    #This Vectorizers below convert a collection of text into a matrix containing the counts of each token with in the text
    if feature_type == 'binary':
        vectorizer = CountVectorizer(binary=True, min_df=1, ngram_range=(1, 1))
    elif feature_type == 'frequency':
        vectorizer = CountVectorizer(binary=False, min_df=1, ngram_range=(1, 1))
    elif feature_type == 'tfidf':
        vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1, 1))
    else:
        raise Exception("Select a feature type of 'binary', 'frequency', or 'tfidf'")

    feature_matrix = vectorizer.fit_transform(documents).astype(float)
    #Use a vectorizer that is established above to create matrix with appropriate values for each term in text
    #Fit transofrm determines the type of data that is returned by sklearn
    
    return vectorizer, feature_matrix


from scipy.sparse.linalg import svds
    
def low_rank_svd(matrix, singular_count=2):
    
    u, s, vt = svds(matrix, k=singular_count)
    return u, s, vt
    
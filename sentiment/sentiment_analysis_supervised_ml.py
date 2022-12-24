
import pandas as pd
import numpy as np
from sentiment_normalization import normalize_corpus
from sentiment_utils import build_feature_matrix

def init_sentiment(trainpath, testpath):
  traindata = pd.read_csv(trainpath)
  newsdata = pd.read_csv(testpath)

  train_data = traindata
  test_data = newsdata

  train_reviews = np.array(train_data['review'])
  train_sentiments = np.array(train_data['sentiment'])

  test_reviews = np.array(test_data['review'])
  test_sentiments = np.array(test_data['sentiment'])



  sample_data = [(test_reviews[index],test_sentiments[index]) for index in range(len(test_sentiments))]

  # normalization
  norm_train_reviews = normalize_corpus(train_reviews,lemmatize=True,only_text_chars=True)
  # feature extraction                                                                            
  vectorizer, train_features = build_feature_matrix(documents=norm_train_reviews, feature_type='tfidf', ngram_range=(1, 1), min_df=0.0, max_df=1.0)                                      
                                  
                                      

  from sklearn.linear_model import SGDClassifier
  import pickle

#BUILD THE Support Vector Machine (SVM) MODEL
  filename = 'C:/Users/sands/Dropbox/Programming/Present/DjangoDirectory/Sigma/data/pickledump.sav'

#INITIAL CREATION OF MODEL DATA
  model = SGDClassifier(loss='hinge', n_iter=500) #Stochastic gradient descent learning
  model.fit(train_features, train_sentiments)
  pickle.dump(model, open(filename, 'wb'))

#LOAD A PREVIOUSLY CREATED MODEL
  # model = pickle.load(open(filename, 'rb'))
  # model.fit(train_features, train_sentiments)



  # normalize reviews                        
  norm_test_reviews = normalize_corpus(test_reviews,lemmatize=True,only_text_chars=True)  
  # extract features                                     
  test_features = vectorizer.transform(norm_test_reviews)         

  sentimentlist = []
  for doc_index in range(len(test_sentiments)):
    # print(test_reviews[doc_index])
    doc_features = test_features[doc_index]
    predicted_sentiment = model.predict(doc_features)[0]
    # print('Predicted Sentiment:', predicted_sentiment)
    sentimentlist.append(predicted_sentiment)


  
  predicted_sentiments = model.predict(test_features)       
  return sentimentlist

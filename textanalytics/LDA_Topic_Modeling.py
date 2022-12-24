import nltk


from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

from nltk.corpus import stopwords 
from nltk.stem.wordnet import WordNetLemmatizer
import string


import sys
import os

import analytic_normalization as norm

def init_topmod(webtext):

	finalTopicList = []
	try:
		specChar = norm.remove_special_characters(webtext)
		stopWords = norm.remove_stopwords(specChar)
		pos = norm.pos_tag_text(stopWords)
		
		alist = []
		accepted_shortwords = ['trump']
		rejected_words = ['things', 'sunday', 'said', 'giving', 'making', 'watched', 'including','bleacher', 'report','sharing', 'edition', 'preference']
		for word,postag in pos:
			if postag == 'n' or postag =='v':
				alist.append(word)
		alist = [word for word in alist if len(word) > 5  or word in accepted_shortwords ]
		alist = [word for word in alist if word not in rejected_words]
		words = ' '.join(alist)
		doc_clean = nltk.word_tokenize(words) 


		topic_list = []
		def display_topics(model, feature_names, no_top_words):
		    for topic_idx, topic in enumerate(model.components_):
		    	for i in topic.argsort()[:no_top_words]:
		    		topic_list.append(feature_names[i])

		# LDA can only use raw term counts for LDA because it is a probabilistic graphical model
		tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2, max_features=15, stop_words='english')
		tf = tf_vectorizer.fit_transform(doc_clean)
		tf_feature_names = tf_vectorizer.get_feature_names()
		no_topics = 200
		lda = LatentDirichletAllocation(n_components=no_topics, max_iter=5, learning_method='online', learning_offset=50.,random_state=0).fit(tf)
		no_top_words = 5
		display_topics(lda, tf_feature_names, no_top_words)


		from collections import Counter
		counts = Counter(topic_list)
		for k,v in counts.items():
			finalTopicList.append(k)

		print(finalTopicList)
	except:
		print('topic modeling error')
	return finalTopicList





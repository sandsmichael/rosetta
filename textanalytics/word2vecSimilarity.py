import nltk
import gensim
import numpy as np
from gensim.models import Phrases



def init_word2vec_newstree(newsDictByArticle, trendingtopics, allbigrams):

	text = []
	for k,v in newsDictByArticle.items():
		temp_text = v[4]
		for item in trendingtopics:
			if " " in item:
				split = item.split(" ")
				output = split[0] + '_' + split[1] #turn all bigrams found in article text into Word_Word format
				temp_text = v[4].replace(item, output) #ngrams cause errors
		text.append(temp_text)

	word_tokenized_text = []
	for item in text:
		sentences = nltk.word_tokenize(item)
		word_tokenized_text.append(sentences)

	#WORD2VEC MODEL
	model = gensim.models.Word2Vec(word_tokenized_text, min_count=12, size =100, workers=4)
	similarityDict = {}
	for i in range(len(trendingtopics)):
		topicx = trendingtopics[i].replace(" ", "_") #ngrams cause errors
		for z in range(len(trendingtopics)):
			try:
				topicy = trendingtopics[z].replace(" ", "_")
				names = str(topicx) + '_' + str(topicy)
				sim = np.round(model.wv.similarity(str(topicx), str(topicy)),2)
				similarityDict[names] = sim
			except:
				a = ''
	import operator
	sorted_full = sorted(similarityDict.items(), key=operator.itemgetter(1))
	print(sorted_full)

	print(allbigrams)
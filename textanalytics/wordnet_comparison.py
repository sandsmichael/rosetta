
import numpy as np 
import nltk
from nltk.corpus import wordnet
synonyms = []
antonyms = []
 
#
#text = ['governments', 'vulnerabilities', 'breaking', 'talking', 'official', 'security', 'administration','allies', 'smartphones', 'increased', 'government', 'gatekeeper', 'noting', 'lewandowski', 'official', 'security', 'administration', 'cunningham', 'source', 'sources', 'address', 'updated', 'officials', 'meetings', 'president', 'access', 'device', 'trump', 'concerns']

def init(text):
	mydict = {}
	for item in text:
		try:
			syns1 = wordnet.synsets(item)
			sysn1_name = syns1[0].name()
			tempitem = item
			text.remove(item)
			keylist = []
			for i in range(len(text)):
				syns2 = wordnet.synsets(text[i])
				sysn2_name = syns2[0].name()

				w = wordnet.synset(sysn1_name)
				ww = wordnet.synset(sysn2_name)
				score = np.round((w.wup_similarity(ww) * 100), 3)

				keylist.append([text[i], score])
				mydict[tempitem] = keylist
		except:
			print('word not found')



	import operator
	sorted_dict = sorted(mydict.items(), key=operator.itemgetter(1), reverse = True)
	return sorted_dict










# syns1 = wordnet.synsets("president")
# sysn1_name = syns1[0].name()

# syns2 = wordnet.synsets("officials")
# sysn2_name = syns2[0].name()
 
# w = wordnet.synset(sysn1_name)
# ww = wordnet.synset(sysn2_name)
# print(np.round((w.wup_similarity(ww) * 100), 3))























#Print synonyms and antonyms

# for syn in wordnet.synsets(w1):
#     for l in syn.lemmas():
#         synonyms.append(l.name())
#         if l.antonyms():
#             antonyms.append(l.antonyms()[0].name())
# print(set(synonyms))
# print(set(antonyms))
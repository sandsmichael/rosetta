import os
import sys
pathsfile =  os.path.dirname(os.path.abspath('src/Pathsfile.py'))
sys.path.insert(0, pathsfile)
import Pathsfile as pf 
sys.path.insert(0, pf.path_SigmaSource)



import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import pandas as pd

from normalization import parse_document




def init_ner(text):
    sentences = parse_document(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]


    # nltk NER
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    ne_chunked_sents = [nltk.ne_chunk(tagged) for tagged in tagged_sentences]
    named_entities = []
    for ne_tagged_sentence in ne_chunked_sents:
        for tagged_tree in ne_tagged_sentence:
            if hasattr(tagged_tree, 'label'):
                    entity_name = ' '.join(c[0] for c in tagged_tree.leaves())
                    entity_type = tagged_tree.label()
                    named_entities.append((entity_name, entity_type))
    
          
    named_entities = list(set(named_entities))
    # entity_frame = pd.DataFrame(named_entities, 
    #                             columns=['Entity Name', 'Entity Type'])

    nerDict = {}
    for item in named_entities:
        k,v = item
        nerDict[k] = v
    return nerDict
















# def init_ner(title):
#     wordlist = title

#     tagged_results = []
#     results = []
#     parsed_ners = []


#     tagged = nltk.pos_tag(nltk.word_tokenize(wordlist))
#     tagged_results.append(tagged)
    
#     no_of_nouns = len([word for word, pos in tagged if pos in [ "NNP"] ])#"NN"
    
#     ners_chunked = nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(wordlist)), binary=False)
#     list_ners = [chunk for chunk in ners_chunked if hasattr(chunk,'label')]

#     for item in list_ners:
#         item = str(item)
#         count = item.count('/')
#         if count == 1: #if there are more than 1 '/' in tree string then there are multiple words i.e. Michael/NNP Sands/NNP
#             start_index = item.find(' ') 
#             end_index = item.find('/')
#             parsed_item = item[start_index:end_index]
#             parsed_ners.append(parsed_item)
#         else:
#             start_index1 = item.find(' ') 
#             end_index1 = item.find('/')
#             parsed_item1 = item[start_index1:end_index1]
#             start_index2 = item.rfind(' ') 
#             end_index2 = item.rfind('/')
#             parsed_item2 = item[start_index2:end_index2]
#             output = parsed_item1  + parsed_item2
#             parsed_ners.append(output)


#     nersList = list(set(parsed_ners))

#     return nersList




from normalization import normalize_corpus, parse_document
from summarization.utils import build_feature_matrix, low_rank_svd
import numpy as np

import networkx




def textrank_text_summarizer(sentences, norm_sentences, num_sentences,feature_type='frequency'):

    vec, dt_matrix = build_feature_matrix(norm_sentences, feature_type='tfidf')
    #This is using Term Frequency Inverse Document Frequency to create a matrix of all tokens in the document text with their associated value
    #vec is the type of vectorizer used by sklearn (Using tfidf above)
    #dt_matrix is the output of our text being run through that vectorizer, yielding a matrix containing all of the tokens in the text with their value

    similarity_matrix = (dt_matrix * dt_matrix.T) #?? Multiple the matrix by its tranposed self
	#can use cosine similarity here instead

    similarity_graph = networkx.from_scipy_sparse_matrix(similarity_matrix)  #??Creates a new graph from an adjacent scipy matrix 
    scores = networkx.pagerank(similarity_graph) 
    #Use pagerank algo to score all of the sentences based upon the values they recieved
    #scores returns a Dictionary of {sentence# : score}
   
    ranked_sentences = sorted(((score, index) for index, score in scores.items()), reverse=True) #Sort the dictionary in order from High to Low scoring sentences
    top_sentence_indices = [ranked_sentences[index][1] for index in range(num_sentences)] #Returns the sentence numbers of the highest n# scoring sentences in the document
    
    highestrankedsentenceindex = top_sentence_indices[0]
    highestscoredsentence = sentences[highestrankedsentenceindex]

    top_sentence_indices.sort() #Re order the sentence numbers based on 0 first and N# after (i.e. reorder so the sentences are in the same order as they appear in original document)
    

    output = []
    for index in top_sentence_indices:
        output.append(sentences[index])
    #Despite using norm_sentences for all of the analytics above...once we have the highest scoring sentences, loop through the true sentences list and pull out
    #the corresponding text based on the index values of the highest scoring normalized sentences as they represent one in the same.

    summary = " ".join(output)
    return (summary,highestscoredsentence)                    
    


def init(usertext):
  DOCUMENT = usertext

  sentences = parse_document(DOCUMENT)
  norm_sentences = normalize_corpus(sentences,lemmatize=True) 

  print("Total Sentences:", len(norm_sentences))

  output,thesis = textrank_text_summarizer(sentences, norm_sentences, num_sentences=5, feature_type='tfidf')
  return (output,thesis)

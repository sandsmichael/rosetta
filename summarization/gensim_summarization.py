
from normalization import normalize_corpus, parse_document
from summarization.utils import build_feature_matrix, low_rank_svd
import numpy as np




from gensim.summarization import summarize, keywords

def text_summarization_gensim(text, summary_ratio=0.5):
    
    summary = summarize(text, split=True, ratio=summary_ratio)
    for sentence in summary:
        print(sentence)


def init(usertext):
	if usertext == "Form is empty":
		toy_text = """
      There are many, and often contradictory, legends about the most ancient King Midas. 
      In one, Midas was king of Pessinus, a city of Phrygia, who as a child was adopted by King Gordias 
      and Cybele, the goddess whose consort he was, and who (by some accounts) was the goddess-mother of
       Midas himself.[6] Some accounts place the youth of Midas in Macedonian Bermion (See Bryges)[7] In
        Thracian Mygdonia,[8] Herodotus referred to a wild rose garden at the foot of Mount Bermion as 
        "the garden of Midas son of Gordias, where roses grow of themselves, each bearing sixty blossoms 
        and of surpassing fragrance".[9] Herodotus says elsewhere that Phrygians anciently lived in Europe
        where they were known as Bryges,[10] and the existence of the garden implies that Herodotus believed
        that Midas lived prior to a Phrygian migration to Anatolia.According to some accounts, Midas had a 
        son, Lityerses, the demonic reaper of men, but in some variations of the myth he instead had a daughter
        Zoë or "life". According to other accounts he had a son Anchurus. Arrian gives an alternative story of 
        the descent and life of Midas. According to him, Midas was the son of Gordios, a poor peasant, and a 
        Telmissian maiden of the prophetic race. When Midas grew up to be a handsome and valiant man, the 
        Phrygians were harassed by civil discord, and consulting the oracle, they were told that a wagon 
        would bring them a king, who would put an end to their discord. While they were still deliberating, 
        Midas arrived with his father and mother, and stopped near the assembly, wagon and all. They, comparing
        the oracular response with this occurrence, decided that this was the person whom the god told them the
        wagon would bring. They therefore appointed Midas king and he, putting an end to their discord, 
        dedicated his father’s wagon in the citadel as a thank-offering to Zeus the king. In addition to this
        the following saying was current concerning the wagon, that whosoever could loosen the cord of the
        yoke of this wagon, was destined to gain the rule of Asia. This someone was to be Alexander the Great.
        11] In other versions of the legend, it was Midas' father Gordias who arrived humbly in the cart and
        made the Gordian Knot. Herodotus said that a "Midas son of Gordias" made an offering to the Oracle of 
        Delphi of a royal throne "from which he made judgments" that were "well worth seeing", and that this 
        Midas was the only foreigner to make an offering to Delphi before Gyges of Lydia.[12] The historical 
        Midas of the 8th century BC and Gyges are believed to have been contemporaries, so it seems most likely 
        that Herodotus believed that the throne was donated by the earlier, legendary King Midas. However, 
        some historians believe that this throne was donated by the later, historical King Midas.[13] 
      """
	else:
		toy_text = usertext

	docs = parse_document(toy_text)
	text = ' '.join(docs)
	text_summarization_gensim(text, summary_ratio=0.4)


	    
	sentences = parse_document(toy_text)
	norm_sentences = normalize_corpus(sentences,lemmatize=False) 

	total_sentences = len(norm_sentences)
	print('Total Sentences in Document:', total_sentences)  



	num_sentences = 3
	num_topics = 2

	vec, dt_matrix = build_feature_matrix(sentences, 
	                                      feature_type='frequency')

	td_matrix = dt_matrix.transpose()
	td_matrix = td_matrix.multiply(td_matrix > 0)

	u, s, vt = low_rank_svd(td_matrix, singular_count=num_topics)  
	                                         
	sv_threshold = 0.5
	min_sigma_value = max(s) * sv_threshold
	s[s < min_sigma_value] = 0

	salience_scores = np.sqrt(np.dot(np.square(s), np.square(vt)))
	print(np.round(salience_scores, 2))

	top_sentence_indices = salience_scores.argsort()[-num_sentences:][::-1]
	top_sentence_indices.sort()
	print(top_sentence_indices)

	output = []
	for index in top_sentence_indices:
	    #print(sentences[index])
	    output.append(sentences[index])


	return output
	    
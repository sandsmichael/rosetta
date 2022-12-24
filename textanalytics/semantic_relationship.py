print('sem rel')

from nltk.corpus import wordnet as wn
import pandas as pd

def random():
	term = 'politics'
	synsets = wn.synsets(term)

	print('Total Synsets:', len(synsets))

	# synsets for fruit
	for synset in synsets:
	    print('Synset:', synset)
	    print('Part of speech:', synset.lexname())
	    print('Definition:', synset.definition())
	    print('Lemmas:', synset.lemma_names())
	    print('Examples:', synset.examples())
	    print()

	# entailments
	for action in ['walk', 'eat', 'digest']:
	    action_syn = wn.synsets(action, pos='v')[0]
	    print(action_syn, '-- entails -->', action_syn.entailments())
	    
	    
	# homonyms\homographs  
	for synset in wn.synsets('bank'):
	    print(synset.name(),'-',synset.definition())


	# synonyms and antonyms
	term = 'large'
	synsets = wn.synsets(term)
	adj_large = synsets[1]
	adj_large = adj_large.lemmas()[0]
	adj_large_synonym = adj_large.synset()
	adj_large_antonym = adj_large.antonyms()[0].synset()

	print( 'Synonym:', adj_large_synonym.name())
	print( 'Definition:', adj_large_synonym.definition())
	print( 'Antonym:', adj_large_antonym.name())
	print( 'Definition:', adj_large_antonym.definition())
	print()



	term = 'tree'
	synsets = wn.synsets(term)
	tree = synsets[0]

	print('Name:', tree.name())
	print ('Definition:', tree.definition())


	hyponyms = tree.hyponyms()
	print ('Total Hyponyms:', len(hyponyms))
	print ('Sample Hyponyms')
	for hyponym in hyponyms[:10]:
	    print(hyponym.name(), '-', hyponym.definition())
	    print()
	    
	hypernyms = tree.hypernyms()
	print (hypernyms)

	hypernym_paths = tree.hypernym_paths()
	print ('Total Hypernym paths:', len(hypernym_paths))

	print('Hypernym Hierarchy')
	print (' -> '.join(synset.name() for synset in hypernym_paths[0]))

	# holonyms and meronyms

	# member holonyms
	member_holonyms = tree.member_holonyms()    
	print( 'Total Member Holonyms:', len(member_holonyms))
	print( 'Member Holonyms for [tree]:-')
	for holonym in member_holonyms:
	    print (holonym.name(), '-', holonym.definition())
	    print()

	# part meronyms
	part_meronyms = tree.part_meronyms()
	print( 'Total Part Meronyms:', len(part_meronyms))
	print( 'Part Meronyms for [tree]:-')
	for meronym in part_meronyms:
	    print( meronym.name(), '-', meronym.definition())
	    print()

	# substance meronyms
	substance_meronyms = tree.substance_meronyms()    
	print( 'Total Substance Meronyms:', len(substance_meronyms))
	print( 'Substance Meronyms for [tree]:-')
	for meronym in substance_meronyms:
	    print( meronym.name(), '-', meronym.definition())
	    print()




















tree = wn.synset('president.n.01')
lion = wn.synset('teacher.n.01')
tiger = wn.synset('senator.n.01')
cat = wn.synset('tax.n.01')
dog = wn.synset('rocket.n.01')

entities = [tree, lion, tiger, cat, dog]
entity_names = [entity.name().split('.')[0] for entity in entities]
entity_definitions = [entity.definition() for entity in entities]

for entity, definition in zip(entity_names, entity_definitions):
    print (entity, '-', definition)
    print()

common_hypernyms = []
for entity in entities:
    # get pairwise lowest common hypernyms
    common_hypernyms.append([entity.lowest_common_hypernyms(compared_entity)[0]
                                            .name().split('.')[0]
                             for compared_entity in entities])
# build pairwise lower common hypernym matrix
common_hypernym_frame = pd.DataFrame(common_hypernyms,
                                     index=entity_names, 
                                     columns=entity_names)
                                     
print( common_hypernym_frame  )  
print()

similarities = []
for entity in entities:
    # get pairwise similarities
    similarities.append([round(entity.path_similarity(compared_entity), 2)
                         for compared_entity in entities])        
# build pairwise similarity matrix                             
similarity_frame = pd.DataFrame(similarities,
                                index=entity_names, 
                                columns=entity_names)
                                     
print(similarity_frame)

from contractions import CONTRACTION_MAP
import re
import nltk
import string
from nltk.stem import WordNetLemmatizer
from html.parser import HTMLParser
import unicodedata

stopword_list = nltk.corpus.stopwords.words('english')
wnl = WordNetLemmatizer()
html_parser = HTMLParser()

def tokenize_text(text):
    tokens = nltk.word_tokenize(text) 
    tokens = [token.strip() for token in tokens]
    return tokens

def expand_contractions(text, contraction_mapping):
    
    contractions_pattern = re.compile('({})'.format('|'.join(contraction_mapping.keys())), 
                                      flags=re.IGNORECASE|re.DOTALL)
    def expand_match(contraction):
        match = contraction.group(0)
        first_char = match[0]
        expanded_contraction = contraction_mapping.get(match)\
                                if contraction_mapping.get(match)\
                                else contraction_mapping.get(match.lower())                       
        expanded_contraction = first_char+expanded_contraction[1:]
        return expanded_contraction
        
    expanded_text = contractions_pattern.sub(expand_match, text)
    expanded_text = re.sub("'", "", expanded_text)
    return expanded_text
    
    
#from pattern.en import tag
from nltk.corpus import wordnet as wn


# Annotate text tokens with POS tags
def pos_tag_text(text):
    
    def penn_to_wn_tags(pos_tag):
        if pos_tag.startswith('JJ'):
            return wn.ADJ
        elif pos_tag.startswith('VB'):
            return wn.VERB
        elif pos_tag.startswith('NN'):
            return wn.NOUN
        elif pos_tag.startswith('RB'):
            return wn.ADV
        else:
            return None
    
    tokenied_text = nltk.word_tokenize(text)
    tagged_text = nltk.pos_tag(tokenied_text)
    # print(tagged_text)
    tagged_lower_text = [(word.lower(), penn_to_wn_tags(pos_tag))
                         for word, pos_tag in
                         tagged_text]
    return tagged_lower_text
    
# lemmatize text based on POS tags    
def lemmatize_text(text):
    
    pos_tagged_text = pos_tag_text(text)
    lemmatized_tokens = [wnl.lemmatize(word, pos_tag) if pos_tag else word for word, pos_tag in pos_tagged_text]
    lemmatized_text = ' '.join(lemmatized_tokens)
    return lemmatized_text
    

def remove_special_characters(text):
    tokens = tokenize_text(text)
    pattern = re.compile('[{}]'.format(re.escape(string.punctuation)))
    filtered_tokens = filter(None, [pattern.sub(' ', token) for token in tokens])
    filtered_text = ' '.join(filtered_tokens)
    return filtered_text
    
    
def remove_stopwords(text):
    tokens = tokenize_text(text)
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    filtered_text = ' '.join(filtered_tokens)    
    return filtered_text


def unescape_html(parser, text):
    
    return parser.unescape(text)

def normalize_corpus(corpus, lemmatize=True, tokenize=False):
    #corpus is a sent_tokenized list of the entire document
    normalized_corpus = []  
    for text in corpus:
        text = html_parser.unescape(text) #Displays html characters in raw text form i.e. '&' instead of '&amp'
        text = expand_contractions(text, CONTRACTION_MAP) #Expand all contractions
        if lemmatize:
            text = lemmatize_text(text) #Convert words to root form and uniform all derivations of a given word
        else:
            text = text.lower()
        text = remove_special_characters(text) #Remove punctuation and other special chars
        text = remove_stopwords(text) #remove stopwords
        if tokenize:
            text = tokenize_text(text) #Word tokenize the text
            normalized_corpus.append(text)
        else:
            normalized_corpus.append(text)
    
    return normalized_corpus


def parse_document(document):
    document = re.sub('\n', ' ', document) #Remove all line breaks
    if isinstance(document, str): #Check if document is of Type string
        document = document
    elif isinstance(document, unicode): #else encode the document as ascii
        return unicodedata.normalize('NFKD', document).encode('ascii', 'ignore')
    else:
        raise ValueError('Encoding error - The Document is not string or unicode')

    document = document.strip() #Remove whitespace
    sentences = nltk.sent_tokenize(document) #Seperate each Sentence into its own item with in a list
    sentences = [sentence.strip() for sentence in sentences]

    return sentences
    
    
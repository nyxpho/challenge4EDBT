#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module can be used to evaluate text similarity between texts, and in 
particular Wikipedia articles.

It mostly provides two methods:
 - via stemming, which is fast, texts are translated into a list of stems (words
 roots) that can be compared
  - via lemmatization, which is slow, texts are translated into a list of lemma 
which contains enough data to check for synonym and are of better quality than
the stems

"""
import re
import nltk

from nltk.parse.stanford import StanfordParser
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

def download_ressources():
	"""
	Used to download ressources to run the different nltk modules
	"""
	nltk.download('stopwords') # For stopwords
	nltk.download('punkt') # tokenization
	nltk.download('maxent_treebank_pos_tagger') # POS tagger
	nltk.download('wordnet') # Wordnet ...


CLEANING_TEXT_PATTERN = re.compile(
	r'(?:\{\{[^\}]*(\}[^\}]*)*\}\})|'
	r'(?:\AREDIRECT)|'
	r'(?:<ref>([^<]*(<(?!/ref>))?)*</ref>)'#Cannot detect ref inside ref
)

STOPWORDS = nltk.corpus.stopwords.words('english')

# Stemmer functions
porter_stemmer = nltk.stem.snowball.PorterStemmer().stem 
snowball_stemmer = nltk.stem.snowball.EnglishStemmer().stem
lancaster_stemmer = nltk.stem.lancaster.LancasterStemmer().stem

#STANDFORD_PARSER = StanfordParser(
	#'parser/stanford-parser-full-2015-04-20/stanford-parser.jar',
	#'parser/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'
#)

wordnet_lemmatizer = WordNetLemmatizer().lemmatize

def full_tokenize(text):
	"""
	Tokenize, remove stopwords, non alpha and too short
	"""
	global CLEANING_TEXT_PATTERN, STOPWORDS
	clean_text = re.sub(CLEANING_TEXT_PATTERN, '', text)
	return (
		token.lower() for token in nltk.word_tokenize(clean_text)
		if token.isalpha() and token not in STOPWORDS and len(token) > 2
	)


def full_stem(text, stemmer=lancaster_stemmer):
	"""
	Returns the stems (sorted)
	
	By default use the fast, aggresive, lancaster stemmer
	"""
	return sorted(stemmer(token) for token in full_tokenize(text))


#def full_lem(text):
	#"""
	#Use the standford parser to return lems
	#"""
	#return STANDFORD_PARSER.raw_parse_sents(text)

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''

def wordnet(text):
	global wordnet_lemmatizer
	pos = nltk.pos_tag(list(full_tokenize(text)))
	return [wordnet_lemmatizer(word, get_wordnet_pos(tag)) for (word, tag) in pos]


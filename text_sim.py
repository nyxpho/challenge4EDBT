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


STOPWORDS = nltk.corpus.stopwords.words('english')

# Stemmer functions
porter_stemmer = nltk.stem.snowball.PorterStemmer().stem 
snowball_stemmer = nltk.stem.snowball.EnglishStemmer().stem
lancaster_stemmer = nltk.stem.lancaster.LancasterStemmer().stem

STANDFORD_PARSER = StanfordParser(
	'parser/stanford-parser-full-2015-04-20/stanford-parser.jar',
	'parser/stanford-parser-full-2015-04-20/stanford-parser-3.5.2-models.jar'
)

wordnet_lemmatizer = WordNetLemmatizer().lemmatize

def full_tokenize(text):
	"""
	Tokenize, remove stopwords, non alpha and too short
	"""
	global STOPWORDS
	return (
		token.lower() for token in nltk.word_tokenize(text)
		if token.isalpha() and token not in STOPWORDS and len(token) > 2
	)


def full_stem(text, stemmer=lancaster_stemmer):
	"""
	Returns the stems (sorted)
	
	By default use the fast, aggresive, lancaster stemmer
	"""
	return sorted(stemmer(token) for token in full_tokenize(text))


def full_lem(text):
	"""
	Use the standford parser to return lems
	"""
	return STANDFORD_PARSER.raw_parse_sents(text)

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


def min_wk_equal(list1, list2):
	"""
	Compute min(Wk12,Wk21) for the 'equal' similarity on sortable item lists
	"""
	list1_it = list1.__iter__()
	list2_it = list2.__iter__()
	wk12 = 0
	wk21 = 0
	looping_list1 = False
	try:
		el1 = list1_it.next()
		el2 = list2_it.next()
		while True:
			if el1 < el2:
				el1 = list1_it.next()
			elif el2 < el1:
				el2 = list2_it.next()
			else:#el1 == el2
				current_value = el1
				looping_list1 = True
				while el1 == current_value:
					wk12 += 1
					el1 = list1_it.next()
				looping_list1 = False
				
				while el2 == current_value:
					wk21 += 1
					el2 = list2_it.next()
	except StopIteration:
		if looping_list1:
			try:
				while el2 == current_value:
					wk21 += 1
					el2 = list2_it.next()
			except StopIteration: pass
	return min(wk12,wk21)

def smthg_sim_equal(list1, list2):
	"""
	Return our custom something similarity between sorted lists list1 and list2
	using the equal similarity as a base.
	
	List element must be sortable !
	"""
	if len(list1) == 0 or len(list2) == 0: return 0
	
	return min_wk_equal(list1, list2) / float(min(len(list1), len(list2)))


def smthg_sim(sim_func, list1, list2):
	"""
	Return our custom something similarity between lists list1 and list2
	"""
	if len(list1) == 0 or len(list2) == 0: return 0
	
	wk12 = sum(max(sim_func(a,b) for b in list2) for a in list1)
	wk21 = sum(max(sim_func(b,a) for a in list1) for b in list2)
	
	return min(wk12, wk21) / float(min(len(list1), len(list2)))


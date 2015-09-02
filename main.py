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

def interSim(set1, set2):
	return 1 if set1.intersection(set2) else 0


def smthg_sim(sim_func, list1, list2):
	"""
	Return our custom something similarity between lists list1 and list2
	"""
	if len(list1) == 0 or len(list2) == 0: return 0
	
	wk12 = sum(max(sim_func(a,b) for b in list2) for a in list1)
	wk21 = sum(max(sim_func(b,a) for a in list1) for b in list2)
	return min(wk12, wk21) / float(min(len(list1), len(list2)))


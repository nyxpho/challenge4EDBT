#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute context similarity
"""

import sys,os,re,time
from igraph import *

gArtArt = Graph.Read_Ncol("test/artart.txt", names=True, weights="if_present", directed=True)
gArtCat = Graph.Read_Ncol("test/artcat.txt", names=True, weights="if_present", directed=True)
gCatCat = Graph.Read_Ncol("test/catcat.txt", names=True, weights="if_present", directed=True)

def inLinksSim(fArticle, sArticle):
	fArticle = 'a'+str(fArticle)
	sArticle = 'a'+str(sArticle)
	fArticleIn = set(gArtArt.neighbors(fArticle, mode="in"))
	sArticleIn = set(gArtArt.neighbors(sArticle, mode="in"))
	return len(fArticleIn.intersection(sArticleIn))/max(1, min(len(fArticleIn), len(sArticleIn)))

def outLinksSim(fArticle, sArticle):
	fArticle = 'a'+str(fArticle)
	sArticle = 'a'+str(sArticle)
	fArticleOut = set(gArtArt.neighbors(fArticle, mode="out"))
	sArticleOut = set(gArtArt.neighbors(sArticle, mode="out"))
	return len(fArticleOut.intersection(sArticleOut))/max(1, min(len(fArticleOut), len(sArticleOut)))

def catSim1(fArticle, sArticle):
	
    """
	This function returns 2 lists of lists:
	- the first list contains a list of the extended categories of the first article
	- the second list contains a list of the extended categories of the second article
	"""
	
	fArticle = 'a'+str(fArticle)
	sArticle = 'a'+str(sArticle)
	firstACat = articleCat(fArticle)
	secondACat = articleCat(sArticle)
	firstList = []
	for cat in firstACat:
		firstList.append(exploration(cat))
	secondList = []
	for cat in secondACat:
		secondList.append(exploration(cat))
	return (firstList, secondList)


def catSim(fArticle, sArticle):
   fExt = [exploration(cat) for cat in articleCat('a'+str(fArticle))]
   sExt = [exploration(cat) for cat in articleCat('a'+str(sArticle))]
   if not fExt or not sExt:
	   return 0
   fExtUnion = set.union(*fExt)
   sExtUnion = set.union(*sExt)
   wk12 = sum(1 for fext in fExt if fext.intersection(sExtUnion))
   wk21 = sum(1 for sext in sExt if sext.intersection(fExtUnion))
   return (min(wk12, wk21) / float(max(1, min(len(fExt),len(sExt)))))

def articleCat(artName):
	"""
	Return the set of categories an articles is contained in
	"""
	try:
		neighbors = gArtCat.neighbors(gArtCat.vs.find(name=artName), mode="out")
		return {gArtCat.vs[catIndex]["name"] for catIndex in neighbors}
	except ValueError:
		return set()


def exploration(catName):
	"""
	Returns the set of category name that are super category of this one
	"""
	try:
		cat_index_in_CatCat = gCatCat.vs.find(name=catName).index
		bfsIt = gCatCat.bfsiter(cat_index_in_CatCat, mode="out")
		explSet = {int(gCatCat.vs[cat.index]["name"][1:]) for cat in bfsIt}
		explSet.add(int(catName[1:]))
		return explSet
	except ValueError:
		return set()


if __name__ == "__main__":
	#print catSim('a1', 'a2')
	#me = catSim1(1, 2)
	#print smthg_sim(interSim, me['first'], me['second'])
	print outLinksSim(1,2)

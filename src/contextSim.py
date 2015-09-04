#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Compute context similarity
"""

import sys,os,re,time
from igraph import *

gArtArt = Graph.Read_Ncol("artart.txt", names=True, weights="if_present", directed=True)
gArtCat = Graph.Read_Ncol("artcat.txt", names=True, weights="if_present", directed=True)
gCatCat = Graph.Read_Ncol("catcat.txt", names=True, weights="if_present", directed=True)

print "size of artart " + str(len(gArtArt.vs))
print "size of catcat " + str(len(gCatCat.vs))
print "size of artcat " + str(len(gArtCat.vs))

def inLinksSim(fArticle, sArticle):
	if fArticle[0] != 'a':
		fArticle = 'a'+str(fArticle)
	if sArticle[0] != 'a':
		sArticle = 'a'+str(sArticle)
	if fArticle == sArticle:
		return 1.
	try:
		fArticleIn = set(gArtArt.neighbors(fArticle, mode="in"))
		sArticleIn = set(gArtArt.neighbors(sArticle, mode="in"))
		return len(fArticleIn.intersection(sArticleIn))/float(max(1, min(len(fArticleIn), len(sArticleIn))))
	except ValueError:
		return 0.

def outLinksSim(fArticle, sArticle):
	if fArticle[0] != 'a':
		ifArticle = 'a'+str(fArticle)
	if sArticle[0] != 'a':
		sArticle = 'a'+str(sArticle)
	if fArticle == sArticle:
		return 1.
	try:
		fArticleOut = set(gArtArt.neighbors(fArticle, mode="out"))
		sArticleOut = set(gArtArt.neighbors(sArticle, mode="out"))
		return len(fArticleOut.intersection(sArticleOut))/float(max(1, min(len(fArticleOut), len(sArticleOut))))
	except ValueError:
		return 0.

def catSim1(fArticle, sArticle):
	
	"""
	This function returns 2 lists of lists:
	- the first list contains a list of the extended categories of the first article
	- the second list contains a list of the extended categories of the second article
	"""
	if fArticle[0] != 'a':	
		fArticle = 'a'+str(fArticle)
	if sArticle[0] != 'a':
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
	if fArticle == sArticle:
		return 1.
	if fArticle[0] != 'a':
		fArticle = 'a'+str(fArticle)
	if sArticle[0] != 'a':
		sArticle = 'a'+str(sArticle)
	fExt = [exploration(cat) for cat in articleCat(str(fArticle))]
	sExt = [exploration(cat) for cat in articleCat(str(sArticle))]  
	if len(fExt) == 0 or len(sExt) == 0:
		return 0
	fExtUnion = set.union(*fExt)
	sExtUnion = set.union(*sExt)
	print fArticle +" " + sArticle + "\nfirst part "
	wk12 = 0
	for fext in fExt:
		inters = fext.intersection(sExtUnion)
		if len(inters) > 0:
			print inters
			wk12 +=1
	wk21 = 0
	print "\nsecond part"
	for sext in sExt:
		inters = sext.intersection(fExtUnion)
		if len(inters) > 0:
			print inters
			wk21 += 1
	print "\n"
	#wk12 = sum(1 for fext in fExt if fext.intersection(sExtUnion))
	#wk21 = sum(1 for sext in sExt if sext.intersection(fExtUnion))
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
		#print depth
		explSet = {gCatCat.vs[cat.index]["name"] for cat in bfsIt}
		explSet.add(catName)
		return explSet
	except ValueError:
		return set()

def retrieveNames(fArticle, sArticle):
	try:
		fName = gArtArt.vs[fArticle]["name"]
		sName = gArtArt.vs[sArticle]["name"]
		return (fName, sName) 
	except ValueError:
		return (None,None)

def noArticles():
	return gArtArt.vcount()

def contextSim(fArticle, sArticle, cstes)
	sim = cstes[1]*inLinksSim(fArticle, sArticle) +
		cstes[2]*outLinksSim(fArticle, sArticle) +
		(1-cstes[1]-cstes[2])*catSim(fArticle, sArticle)
	print inLinksSim(fArticle, sArticle), outLinksSim(fArticle, sArticle), catSim(fArticle, sArticle)
	print sim
	return sim
	

if __name__ == "__main__":
	#print catSim('a1', 'a2')
	#me = catSim1(1, 2)
	#print smthg_sim(interSim, me['first'], me['second'])
	print catSim('1','2')

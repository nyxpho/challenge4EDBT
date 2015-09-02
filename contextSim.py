import sys,os,re,time
from igraph import *

gArtArt = Graph.Read_Ncol("artart.txt", names=True, weights="if_present", directed=True)
gArtCat = Graph.Read_Ncol("artcat.txt", names=True, weights="if_present", directed=True)
gCatCat = Graph.Read_Ncol("catcat.txt", names=True, weights="if_present", directed=True)

def inLinksSim(fArticle, sArticle):
    fArticleIn = gArtArt.neighbors(fArticle, mode="in")
    sArticleIn = gArtArt.neighbors(sArticle, mode="in")
    return {'first':sorted(fArticleIn), 'second':sorted(sArticleIn)}

def outLinksSim(fArticle, sArticle):
    fArticleOut = gArtArt.neighbors(fArticle, mode="out")
    sArticleOut = gArtArt.neighbors(sArticle, mode="out")
    return {'first':sorted(fArticleOut), 'second':sorted(sArticleOut)}

# start with articles that already have a reference to each other
def catSim(fArticle, sArticle):
    start = time.time()
    firstA = gArtArt.vs[fArticle]["name"]
    secondA = gArtArt.vs[sArticle]["name"]
    try:
        indexFirstA = gArtCat.vs.find(name=firstA)
    except ValueError:
        return {'first':[], 'second':[]}
    try:
        indexSecondA = gArtCat.vs.find(name=secondA)
    except ValueError:
        return {'first':[], 'second':[]}
    firstACat = gArtCat.neighbors(indexFirstA, mode="out")
    secondACat = gArtCat.neighbors(indexSecondA,mode="out")
    firstACatName = set([])
    secondACatName = set([])
    firstACatExt = set([])
    secondACatExt = set([])
    for cat in firstACat:
        firstACatName.add(gArtCat.vs[cat]["name"])
    for cat in secondACat:
        secondACatName.add(gArtCat.vs[cat]["name"])
    for cat in firstACatName:
        try:
            indexCat = gCatCat.vs.find(name=cat)
        except ValueError:
            continue
        firstACatExt.add(indexCat.index)
        bfs = gCatCat.bfs(indexCat.index, mode="out")
        firstACatExt.update(bfs[0][0:len(bfs[1])-1])
    for cat in secondACatName:
        try:
            indexCat = gCatCat.vs.find(name=cat)
        except ValueError:
            continue
        secondACatExt.add(indexCat.index)
        bfs = gCatCat.bfs(indexCat.index, mode="out")
        secondACatExt.update(bfs[0][0:len(bfs[1])-1])
    
    return {'first':sorted(firstACatExt), 'second':sorted(secondACatExt)}


if __name__ == "__main__":
    similarityCat = catSim(long(sys.argv[1]), long(sys.argv[2]))
    print len(similarityCat['first'])
    inSimilarity = inLinksSim(long(sys.argv[1]), long(sys.argv[2]))
    print len(inSimilarity['first'])


import sys
from os import path
from igraph import *

def writeTransformation(inPath, outPath, mode):
    """
    Parses the file in inPath and writes in the required format in outPath
    The parameter mode will determine if 
    aa - we put an 'a' in front of each index
    cc - we put a 'c' in front of each index
    ac - a for first, c for  second
    """
    f = open(inPath)
    line = f.readline()
    line = f.readline()
    rb = open(outPath, "w")
    while line is not None:
        line = line.replace("\"","")
        ids = line.strip().split(",")
        if mode =='aa':
            rb.write('a'+ids[0]+ " " + 'a'+ids[1]+"\n")
        if mode =='ac':
            rb.write('a'+ids[0]+ " " + 'c'+ids[1]+"\n")
        if mode =='cc':
            rb.write('c'+ids[0]+ " " + 'c'+ids[1]+"\n")
        line = f.readline()
    rb.close()

if __name__ == "__main__":
	inDir = sys.argv[1] if len(sys.argv)>1 else '.'
	outDir = sys.argv[2] if len(sys.argv)>2 else inDir
	
	transformation_list = [
		('articles_links', 'artart', 'aa'),
		('article_category', 'artcat','ac'),
		('categories_relations', 'catcat', 'cc')
	]
	
	for (inName, outName, mode) in transformation_list:
		inPath = path.join(inDir,inName+'.csv')
		outPath = path.join(outDir,inName+'.txt')
		writeTransformation(inPath, outPath, mode)

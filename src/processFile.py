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
    rb = open(outPath, "w")
    
    if mode =='aa':
        mode_str= 'a%s a%s\n'
    if mode =='ac':
        mode_str= 'a%s c%s\n'
    if mode =='cc':
        mode_str= 'c%s c%s\n'
    
    line = f.readline() #skip the first line of header
    for line in f:
        ids = line.replace("\"","").strip().split(",")
        if len(ids) == 2:
            rb.write(mode_str %(ids[0], ids[1]))
    
    rb.close()
    f.close()

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

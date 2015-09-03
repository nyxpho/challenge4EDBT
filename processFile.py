import sys,os,re,time
from igraph import *

def write(inPath, outPath, mode):
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
    write(sys.argv[1], sys.argv[2],sys.argv[3])

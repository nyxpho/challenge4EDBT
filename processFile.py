import sys,os,re,time
from igraph import *

def write(inPath,outPath):
    f = open(stringPath)
    line = f.readline()
    line = f.readline()
    rb = open(outPath, "w")
    while line is not None:
        line = line.replace("\"","")
        ids = line.strip().split(",")
        rb.write(ids[0]+ " " + ids[1]+"\n")
        line = f.readline()
    rb.close()

if __name__ == "__main__":
    write(sys.argv[1], sys.argv[2])

#!/usr/bin/python
# Created by 邓竹立 on 2021/2/18.

import os
import time
import sys
import getopt
import zipfile
import shutil


inputfile = ''
outputfile = ''

#func name
global lastfunc
#file name
global lastfile
#line
global lastline
#compressed strings
global compressed
#find symbols
global occurredsymbols
global unzippath
lastfunc = ""
lastfile = ""
lastline = ""
compressed = ""

unzip = False

#get inputfile & outputfile
try:
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
except getopt.GetoptError:
      print ('compressed.py -i <inputfile> -o <outputfile>')
      sys.exit(2)
for opt, arg in opts:
      if opt == '-h':
         print ('compressed.py -i <inputfile> -o <outputfile>')
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg

#unzip func
def un_zip(file_name):
 zip_file = zipfile.ZipFile(file_name)
 global unzippath
 unzippath = file_name + "_files"
 if os.path.isdir(file_name + "_files"):
  pass
 else:
  os.mkdir(file_name + "_files")
 for names in zip_file.namelist():
  zip_file.extract(names,file_name + "_files/")
 zip_file.close()

#unzip inputfile if need
if inputfile.endswith('.zip'):
    un_zip(inputfile)
    unzip = True
    name = os.path.basename(inputfile)
    name = name.replace(".zip", "")
    inputfile = inputfile + '_files/' + name

#write compressed flag
with open(outputfile, 'w+') as file:
    file.write("Symbol: compressed\n")
occurredsymbols = False

#find symbols
def occurred_symbols(line):
    global compressed
    compressed = compressed + line + '\n'
    global occurredsymbols
    if line.startswith('Symbol table:'):
        occurredsymbols = True

#compresse symbols
def compresse_func(line):

    global lastfunc
    global lastfile
    global lastline
    global compressed

    strlist = line.split('\t')
    length = len(strlist)
    
    if length < 3:
        return
    #begin addtrss
    str0 = strlist[0]
    #end address
    str1 = strlist[1]
    #symbol name ,such as funcname
    str2 = strlist[2]
    #file name
    str3 = ""
    #line
    str4 = ""
    #unknown
    str5 = ""

    if length > 4:
        str3 = strlist[3]
        str5 = strlist[4]
        fileinfo = str3.split(':')
        if len(fileinfo) > 1:
            str3 = fileinfo[0]
            str4 = fileinfo[1]
    elif length > 3:
        str3 = strlist[3]
        fileinfo = str3.split(':')
        if len(fileinfo) > 1:
            str3 = fileinfo[0]
            str4 = fileinfo[1]
    
    if lastfile != str3:
        lastfile = str3
        compressed = compressed + 'f:' + lastfile + '\n'
    
    if lastfunc != str2:
        lastfunc = str2
        compressed = compressed + 'fn:' + lastfunc + '\n'
    
    if lastline != str4:
        lastline = str4
        compressed = compressed + 'l:' + lastline + '\n'
    if str5 != "":
        a = int(str1,16)
        b = int(str0,16)
        size = '{:x}'.format(a-b)
        compressed = compressed + str0 + ' ' + size + ' ' + str5 + '\n'
    else:
        a = int(str1,16)
        b = int(str0,16)
        size = '{:x}'.format(a-b)
        compressed = compressed + str0 + ' ' + size + '\n'
        
#read bugly.symbol
f = open(inputfile)
line = f.readline()

lines = len(open(inputfile,'r').readlines())

count = 0
while line:
    line = line.strip('\n')
    count = count +1
    
    if occurredsymbols:
        #compresse symbols
        compresse_func(line)
    else:
        #read header info
        occurred_symbols(line)
    
    if count % 1000 == 0:
        progress = int(count * 100 / lines)
        print("\r", end="")
        print("Compressed progress: {}%: ".format(progress), "▋" * (progress // 2), end="")
        sys.stdout.flush()
        with open(outputfile, 'a') as file:
            file.write(compressed)
        compressed = ""
    
    line = f.readline()
f.close()

#wirte left string
print("\r", end="")
print("Compressed progress: {}%: ".format(100), "▋" * (100 // 2), end="")
sys.stdout.flush()

with open(outputfile, 'a') as file:
    file.write(compressed)
compressed = ""

#zip file
print("\nPacking file...")
zippath = outputfile + '.zip'
zip = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
name = os.path.basename(outputfile)
zip.write(outputfile,name)
zip.close()

#remove tmp files
if unzip:
    shutil.rmtree(unzippath)
os.remove(outputfile)

print("Succeed")


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
global lastfunc
global lastfile
global lastline
global decompressed
global occurredsymbols
global iscompressed
global unzippath

lastfunc = ""
lastfile = ""
lastline = ""
decompressed = ""

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


with open(outputfile, 'w+') as file:
    file.write("")
occurredsymbols = False
iscompressed = False

def occurred_symbols(line):
    global iscompressed
    if line.startswith('Symbol: compressed'):
        iscompressed = True
    global decompressed
    decompressed = decompressed + line + '\n'
    global occurredsymbols
    if line.startswith('Symbol table:'):
        occurredsymbols = True

def decompresse_func(line):

    global lastfunc
    global lastfile
    global lastline
    global decompressed
    
    if line.startswith('f:'):
        length = len(line)
        lastfile = ""
        if length > 2:
            lastfile = line[2:length]
    elif line.startswith('fn:'):
        length = len(line)
        lastfunc = ""
        if length > 3:
            lastfunc = line[3:length]

    elif line.startswith('l:'):
        length = len(line)
        lastline = ""
        if length > 2:
            lastline = line[2:length]
    else:
        addressinfo = line.split(' ')
        length = len(addressinfo)
        if length < 2:
            return
        elif length > 2:
            begin = addressinfo[0]
            size = addressinfo[1]
            info = addressinfo[2]
            a = int(begin,16)
            b = int(size,16)
            end = '{:x}'.format(a+b)
            
            decompressed = decompressed + begin + '\t' + end + '\t' + lastfunc
            if len(lastfile) > 0:
                decompressed = decompressed + '\t' + lastfile
                if len(lastline) > 0:
                    decompressed = decompressed + ':' + lastline
            
            decompressed = decompressed + '\t' + info + '\n'
            
        else:
                begin = addressinfo[0]
                size = addressinfo[1]
                a = int(begin,16)
                b = int(size,16)
                end = '{:x}'.format(a+b)
            
                decompressed = decompressed + begin + '\t' + end + '\t' + lastfunc
                if len(lastfile) > 0:
                    decompressed = decompressed + '\t' + lastfile
                    if len(lastline) > 0:
                        decompressed = decompressed + ':' + lastline
                            
                decompressed = decompressed + '\n'

f = open(inputfile)
line = f.readline()

lines = len(open(inputfile,'r').readlines())

count = 0
while line:
    line = line.strip('\n')
    count = count +1
    if occurredsymbols:
        decompresse_func(line)
    else:
        occurred_symbols(line)
        if iscompressed == False:
            decompressed = ""
            print ("not a compressed file!")
            break

    if count % 1000 == 0:
        progress = int(count * 100 / lines)
        print("\r", end="")
        print("Decompressed progress: {}%: ".format(progress), "▋" * (progress // 2), end="")
        sys.stdout.flush()

        with open(outputfile, 'a') as file:
            file.write(decompressed)
        decompressed = ""
    
    line = f.readline()
f.close()
print("\r", end="")
print("Decompressed progress: {}%: ".format(100), "▋" * (100 // 2), end="")
sys.stdout.flush()

with open(outputfile, 'a') as file:
    file.write(decompressed)
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


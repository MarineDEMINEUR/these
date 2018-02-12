#!/usr/bin/env python
#Marine ROGER 09022018
# Programme de batch processing pour ERS RAW data

import getopt, sys, string, re, os, shutil, subprocess, shlex


##################################################################
#Define parameters
##################################################################
#DEM Directory 
DEM = '/home/users/b7067586/Documents/DATA/DEM/ISCE_TDX'
#Orbit Directory (attention ERS1/ERS2)
Orbit1 = '/home/users/b7067586/Documents/DATA/SAR/ERS/Orbit/ERS1' 
Orbit2 = '/home/users/b7067586/Documents/DATA/SAR/ERS/Orbit/ERS2'
#SAR products directory 
ERS = '/home/users/b7067586/Documents/DATA/SAR/ERS/'
outdir = '/home/users/b7067586/Documents/InSAR/ISCE_processing/Batch/ERS'

def main():
  args = parse_arguments()

  print args

  file_content = read_file(args["dates"])
  print file_content
  for date in file_content:
	master = date[0]
	slave = date[1]
	print(master)
	print(slave)
	masterdir = ERS +  master
	slavedir = ERS + slave
	print(slavedir)		
	out = master + '_' + slave
	print(out)
	outdirms = outdir + '/' + out
	print('Processing: date master is ' + master +', slave one is ' + slave)	
	os.mkdir(out)
	shutil.copy('insarApp_create_ERS.py', outdirms)
	os.getcwd()	
	os.chdir(outdirms)
	os.getcwd()	
	print('Start insar_create')
	
	import insarApp_create_ERS
	insarApp_create_ERS.insarApp_create_ERS(masterdir, slavedir, Orbit2, DEM, outdirms)

	#insarApp_create_ERS(masterdir, slavedir, Orbit2, DEM, outdirms)
	#subprocess.call(["python", "insarApp_create_ERS.py", "-m", masterdir, "-s", slavedir, "-orb", Orbit2, "-dem", DEM, "-o", outdirms])
	
	new = 'insarApp_' + out + '.xml'
	os.rename("insarApp.xml", new)
	print('Start of the processing')
	
	outdirend = outdirms + '/' + new
	print(outdirend)
	#subprocess.call(["python", "insarApp.py", outdirend])

	print('Processing of ' + out + 'is complete')
	os.chdir(outdir)

def parse_arguments():
  args = {}
  
  # input arguments
  try:
    opts = getopt.getopt(sys.argv[1:],"h:d", ["help","dates="])
    opts = opts[0]

    for i in range(len(opts)):
      key = re.sub(r"-+", "", opts[i][0])
      if len(opts[i]) > 1:
        args[key] = opts[i][1]
      else:
        args[key] = True
  except Exception as e:
    print e
    usage()

  return args

def read_file(filename):
  content = list(open(filename, 'r'))
  lines=list()
  for i in range(len(content)):
    dates = re.split(r"\s+", content[i].strip('\n'))
    lines.append(dates)

  return lines

def usage():

  print ' -------------------------------------------------------------------------'
  print ' Typical usage:'
  print ' [name].py --dates=/usr/documents/dates.xml'
  print ' '
  print ' --dates  The dates file'
  print ' -------------------------------------------------------------------------'
  sys.exit(' ')

#-------------------------------
if __name__ == "__main__":
  main()

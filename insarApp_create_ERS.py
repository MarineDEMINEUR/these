#!/usr/bin/env python3

#modified for ERS Marine 02022018

import isce
from isceobj.XmlUtil import FastXML as xml
import os, sys, glob
import argparse

def cmdLineParse():
    '''
    Command Line Parser.
    '''
    parser = argparse.ArgumentParser(description='Create ERS input xmlfile for insarApp'
    '''

Example: 

insarApp_create_ERS.py -m masterdir -s slavedir -orb orbdir -dem demdir -o outdir
            
''')
    parser.add_argument('-m','--masterd', type=str, required=True, help='master data folder path', dest='master')
    parser.add_argument('-s','--slaved',type=str, required=True, help='slave data folder path', dest='slave')
    parser.add_argument('-orb','--orb',type=str, required=True, help='orbit file path', dest='orbit')
    parser.add_argument('-dem','--demdir',type=str, required=True, help='dem file path', dest='dem')    
    parser.add_argument('-o','--outdir',type=str, default='./', help='output xml file path', dest='out')
    
   
    inps = parser.parse_args()
    if (not inps.master or not inps.slave or not inps.orbit):
        print('User did not provide master or slave or orbit data path')
        sys.exit(0)

    return inps


def ERS_insarapp_xml_generator(masterdir, slavedir,  orbdir, demdir, outdir='.'):
    '''
    Generation of insarApp.xml for ERS raw data.

    Inputs:
         masterdir = full path to master folder
         slavedir = full path to slave folder
         orbdir = full path to orbit folder
         demdir = full path to dem folder   
         outdir = Directory in which you want insarApp.xml created
    '''
    #####Initialize a component named insar
    insar = xml.Component('insar')

    ####Python dictionaries become components
    ####Master info
    master = {} 
    print masterdir
    masterimg = glob.glob(masterdir + '/DAT_01.001') #list
    masterled = glob.glob(masterdir + '/LEA_01.001')
    masterorb = glob.glob(orbdir)
    master['IMAGEFILE']  =      masterimg[0]      #Can be a string returned by another function
    master['LEADERFILE'] =      masterled[0]      #Can be a string returned by another function
    master['ORBIT_TYPE'] =      'ODR'    
    master['ORBIT_DIRECTORY'] = masterorb[0]
    master['output'] = 'master.raw'    #Can parse file names and use date

    ####Slave info
    slave = {}
    slaveimg = glob.glob(slavedir + '/DAT_01.001')
    slaveled = glob.glob(slavedir + '/LEA_01.001')
    slaveorb = glob.glob(orbdir)
    slave['IMAGEFILE']  =  slaveimg[0]            #Can be a string returned by another function
    slave['LEADERFILE'] =  slaveled[0]            #Can be a string returned by another function
    slave['ORBIT_TYPE'] =  'ODR'    
    slave['ORBIT_DIRECTORY'] = slaveorb[0]
    slave['output'] = 'slave.raw'     #Can parse file names and use date

    #### dem info
  
    insar['dem'] = xml.Catalog(demdir + '/TDM1_DEM.dem.wgs84.xml')

    #####Set sub-component
    ####Nested dictionaries become nested components
    insar['master'] = master
    insar['slave'] = slave
 

    ####Set properties
    insar['sensor name'] = 'ERS'
    insar['range looks'] = 8
    insar['azimuth looks'] = 16
    insar['slc offset method'] = 'ampcor'
    insar['filter strength'] = 0.7
    insar['unwrap'] = 'True'
    insar['do unwrap 2 stage'] = 'True'
    insar['unwrapper name'] = 'snaphu_mcf'
    insar['geocode bounding box'] = [23.5, 24.5, 120.1, 121.2]
    insar['geocode list'] = 'filt_topophase.flat filt_topophase.unw filt_topophase_2stage.unw filt_topophase.unw.conncomp phsig.cor'

   
    ####Components include a writeXML method
    ####Write insarApp.xml in output directory
    insar.writeXML(os.path.join(outdir, 'insarApp.xml'), root='insarApp')

    return

if __name__ == '__main__':
    '''
    Usage example
    insarApp_create_ERS.py -m masterdir -s slavedir -orb orbdir -dem demdir -o outdir
    '''

    if len(sys.argv) == 1:
        dir = '/home/users/b7067586/Documents/InSAR/ISCE_processing/ERS/Batch_processing/'
        masterdir = dir + 'data/masterd/'
        slavedir  = dir + 'data/slaved/'
        orbdir = dir + 'orbit/'
        demdir = dir + 'dem/'
        int_dir   = '/home/users/b7067586/Documents/InSAR/ISCE_processing/ERS/Batch_processing/result/' #outdir
    elif len(sys.argv) > 1:
        inps = cmdLineParse()
        masterdir = inps.master;
        slavedir = inps.slave;
        orbdir = inps.orbit
        demdir = inps.dem;
        int_dir = inps.out;

        ERS_insarapp_xml_generator(os.path.abspath(masterdir), os.path.abspath(slavedir), os.path.abspath(orbdir), os.path.abspath(demdir), outdir= os.path.abspath(int_dir))

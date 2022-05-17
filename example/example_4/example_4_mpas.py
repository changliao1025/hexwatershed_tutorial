#import some basic Python library
import os, sys
from pathlib import Path
from os.path import realpath

#import logging for some log information
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')


#import the hexwatershed python class and function to read the model configuration json file
from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

#set up some model keyword, you can also specify them directly in the json file
#type of mesh 
sMesh_type = 'mpas' 
#assign an index for the case simulation
iCase_index = 1
#the desired spatial resolution in meter, since it is a MPAS variable resolution, this parameter is not effective in this case
dResolution_meter=5000
#add the date stamp to the case simulation
sDate='20220517'

#resolving the path, this will be used to construct the configuration file full path and input/output paths.
sPath = str( Path().resolve() )

#now prepare the data directory
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
sWorkspace_output = str(Path(sWorkspace_data)  /  'output')

#this is full path of the configuration
sFilename_configuration_in = realpath( sPath +  '/example/example_4/pyhexwatershed_susquehanna_mpas.json' )

#check if the configuration file exists or not
if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()

#read the configuration and build an object
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index, sDate_in= sDate, sMesh_type_in= sMesh_type)     

#print out the configuration for review
print(oPyhexwatershed.tojson())

#pPyFlowline is a component for flowline and mesh generation
#if you set this flag as 0, then the model will run as a pure elevation based simulation (no stream burning)
if oPyhexwatershed.pPyFlowline.iFlag_flowline==1:
    oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=39.4620
    oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=-76.0093

#convert user provided shapefile to the geojson, etc.
oPyhexwatershed.setup()

#set the study domain boundary in GCS
oPyhexwatershed.pPyFlowline.dLongitude_left= -79
oPyhexwatershed.pPyFlowline.dLongitude_right= -74.5
oPyhexwatershed.pPyFlowline.dLatitude_bot= 39.20
oPyhexwatershed.pPyFlowline.dLatitude_top= 42.8

#now let's run the pyflowline module
oPyhexwatershed.run_pyflowline()
#save the pyflowline output
oPyhexwatershed.pPyFlowline.export()
#also save the configuration
oPyhexwatershed.export_config_to_json()
#now run the hexwatershed main component 
oPyhexwatershed.run_hexwatershed()
#some postprocess to analyze the result
oPyhexwatershed.analyze()
#export the model output files
oPyhexwatershed.export()
      
#print log information
print('Finished')
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')

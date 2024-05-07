
import os, sys
from pathlib import Path
from os.path import realpath
import argparse
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

sMesh_type = 'hexagon'
iCase_index = 16
dResolution_meter=5000
sDate='20220518'
sPath = str( Path().resolve() )
iFlag_option = 1
sWorkspace_data = realpath( sPath +  '/data/susquehanna' )

sWorkspace_input =  str(Path(sWorkspace_data)  /  'input')

sWorkspace_output=  str(Path(sWorkspace_data)  /  'output')

iFlag_submit = 0


sFilename_configuration_in = realpath( sPath +  '/example/example_1/pyhexwatershed_susquehanna_hexagon.json' )

if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This shapefile does not exist: ', sFilename_configuration_in )
    exit()

oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index, sDate_in= sDate, sMesh_type_in= sMesh_type)  

print(oPyhexwatershed.tojson())

oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=39.4620
oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=-76.0093
oPyhexwatershed.setup()
oPyhexwatershed.pPyFlowline.dLongitude_left= -79
oPyhexwatershed.pPyFlowline.dLongitude_right= -74.5
oPyhexwatershed.pPyFlowline.dLatitude_bot= 39.54 #39.20
oPyhexwatershed.pPyFlowline.dLatitude_top= 42.8
aCell = oPyhexwatershed.run_pyflowline()
aCell_out = oPyhexwatershed.assign_elevation_to_cells()
oPyhexwatershed.pPyFlowline.export()
oPyhexwatershed.export_config_to_json()
oPyhexwatershed.run_hexwatershed()
oPyhexwatershed.analyze()
oPyhexwatershed.export()                 

print('Finished')

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')

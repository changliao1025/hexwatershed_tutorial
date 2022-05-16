
import os, sys
from pathlib import Path
from os.path import realpath
import logging
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation started.')

from pyhexwatershed.classes.pycase import hexwatershedcase
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file


sMesh_type = 'mpas'
iCase_index = 4
dResolution_meter=5000
sDate='20220517'
sPath = str( Path().resolve() )
iFlag_option = 1

sWorkspace_data = realpath( sPath +  '/data/susquehanna' )
sWorkspace_input = str(Path(sWorkspace_data)  /  'input')
sWorkspace_output = str(Path(sWorkspace_data)  /  'output')


sFilename_configuration_in = realpath( sPath +  '/example/example_4/pyhexwatershed_susquehanna_mpas.json' )
        
if os.path.isfile(sFilename_configuration_in):
    print(sFilename_configuration_in)
else:
    print('This configuration file does not exist: ', sFilename_configuration_in )
    exit()
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,\
    iCase_index_in=iCase_index, sDate_in= sDate, sMesh_type_in= sMesh_type)     

print(oPyhexwatershed.tojson())

if oPyhexwatershed.pPyFlowline.iFlag_flowline==1:
    oPyhexwatershed.pPyFlowline.aBasin[0].dLatitude_outlet_degree=39.4620
    oPyhexwatershed.pPyFlowline.aBasin[0].dLongitude_outlet_degree=-76.0093
oPyhexwatershed.setup()
oPyhexwatershed.pPyFlowline.dLongitude_left= -79
oPyhexwatershed.pPyFlowline.dLongitude_right= -74.5
oPyhexwatershed.pPyFlowline.dLatitude_bot= 39.20
oPyhexwatershed.pPyFlowline.dLatitude_top= 42.8
oPyhexwatershed.run_pyflowline()
oPyhexwatershed.pPyFlowline.export()
oPyhexwatershed.export_config_to_json()
oPyhexwatershed.run_hexwatershed()
oPyhexwatershed.analyze()
oPyhexwatershed.export()
      

print('Finished')
logging.basicConfig(format='%(asctime)s %(message)s')
logging.warning('is the time pyhexwatershed simulation finished.')

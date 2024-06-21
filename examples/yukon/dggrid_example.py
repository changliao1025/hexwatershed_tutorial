import os
import sys
import json
from pathlib import Path
import shutil
from os.path import realpath
import importlib.util
from shutil import copy2
from datetime import date
#import geopandas as gpd
import matplotlib.pyplot as plt
#now add the pyflowline into the Python path.

os.environ["PATH"] += os.pathsep + "/qfs/people/liao313/bin/"


from pyhexwatershed.configuration.change_json_key_value import change_json_key_value #this function is used to change the value of a key in a json file
from pyhexwatershed.configuration.read_configuration_file import pyhexwatershed_read_configuration_file #this function is used to read the model configuration file

sPath_parent = Path().resolve()
print(sPath_parent)

sWorkspace_data = os.path.join( sPath_parent ,  'data', 'yukon' )
if not os.path.exists(sWorkspace_data):
    print(sWorkspace_data)
    os.makedirs(sWorkspace_data)

sWorkspace_input =  os.path.join( sWorkspace_data ,  'input')
if not os.path.exists(sWorkspace_input):
    print(sWorkspace_input)
    os.makedirs(sWorkspace_input)

sWorkspace_output = sWorkspace_data + '/output/' #this is where the output will be stored
if not os.path.exists(sWorkspace_output):
    print(sWorkspace_output)
    os.makedirs(sWorkspace_output)

#create a temp folder to download data
iFlag_download_data = 0

if iFlag_download_data == 1:
    sPath_temp = os.path.join( sPath_parent ,  'data', 'tmp' )
    if not os.path.exists(sPath_temp):
        print(sPath_temp)
        os.makedirs(sPath_temp)
    else:
        shutil.rmtree(sPath_temp)

    # specify the repository's URL
    hexwatershed_data_repo = 'https://github.com/changliao1025/hexwatershed_data.git'
    # clone the repository
    os.system(f'git clone {hexwatershed_data_repo} {sPath_temp}')
    sPath_temp_data = os.path.join( sPath_parent ,  'data', 'tmp', 'data','yukon', 'input' )

    #copy all the files under the temp data folder using shutil
    #check if the destination directory exists, if exists, remove it
    if os.path.exists(sWorkspace_input):
        shutil.rmtree(sWorkspace_input)

    shutil.copytree(sPath_temp_data, sWorkspace_input)
    #delte the temp folder
    shutil.rmtree(sPath_temp)

#an example of the configuration file are provided in the input folder
sFilename_configuration_in = realpath( sWorkspace_input +  '/pyhexwatershed_yukon_dggrid.json' )
sFilename_basins_in = realpath( sWorkspace_input +  '/pyflowline_yukon_basins.json' )
if os.path.isfile(sFilename_configuration_in) and os.path.isfile(sFilename_basins_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

print('Finished the data preparation step.')

#step 3
#set up some parameters
sMesh_type = 'dggrid' #the dggrid mesh type supported by hexwatershed
sDggrid_type = 'ISEA3H' #a type of dggrid mesh
iCase_index = 2 #a case index for bookmark
iResolution_index = 11 #dggrid resolution index, see dggrid documentation for details.
iFlag_stream_burning_topology = 1 #see hexwatershed documentation for details
iFlag_use_mesh_dem = 0
iFlag_elevation_profile = 0 #reserved for future use

today = date.today()
iYear = today.year
iMonth = today.month
iDay = today.day
print("Today's date:", iYear, iMonth, iDay)
sDate = str(iYear) + str(iMonth).zfill(2) + str(iDay).zfill(2) #the date is also a bookmark to label a simulation

from pyflowline.mesh.dggrid.create_dggrid_mesh import dggrid_find_resolution_by_index
dResolution = dggrid_find_resolution_by_index(sDggrid_type, iResolution_index)
print(dResolution) #unit is meter

#we want to copy the example configuration file to the output directory
sFilename_configuration_copy= os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_copy.json' )
copy2(sFilename_configuration_in, sFilename_configuration_copy)

#copy the basin configuration file to the output directory as well
sFilename_configuration_basins_copy = os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_basins_copy.json' )
copy2(sFilename_basins_in, sFilename_configuration_basins_copy)

#now switch to the copied configuration file for modification
sFilename_configuration = sFilename_configuration_copy
sFilename_basins = sFilename_configuration_basins_copy

change_json_key_value(sFilename_configuration, 'sWorkspace_output', sWorkspace_output) #output folder
change_json_key_value(sFilename_configuration, 'sFilename_basins', sFilename_basins) #basin configuration file

#change the boundary file
sFilename_mesh_boundary = realpath(os.path.join(sWorkspace_input, 'boundary.geojson'))
change_json_key_value(sFilename_configuration, 'sFilename_mesh_boundary', sFilename_mesh_boundary)
#change the dem file
sFilename_dem = realpath(os.path.join(sWorkspace_input, 'dem.tif'))
change_json_key_value(sFilename_configuration, 'sFilename_dem', sFilename_dem)
#the read function accepts several keyword arguments that can be used to change the default parameters.
#the normal keyword arguments are:
#iCase_index_in: this is an ID to identify the simulation case
#sMesh_type_in: this specifies the mesh type ('mpas' in this example)
#sDate_in: this specifies the date of the simulation, the final output folder will have a pattern such as 'pyflowline20230901001', where pyflowline is model, 20230901 is the date, and 001 is the case index.

oPyhexwatershed = pyhexwatershed_read_configuration_file(sFilename_configuration,
                    iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                    iFlag_use_mesh_dem_in=iFlag_use_mesh_dem,
                    iFlag_elevation_profile_in=iFlag_elevation_profile,
                    iResolution_index_in = iResolution_index,
                    sDggrid_type_in=sDggrid_type,
                    sDate_in= sDate, sMesh_type_in = sMesh_type)

#we also need to set the output location for the only basin
dLongitude_outlet_degree= -164.47594
dLatitude_outlet_degree= 63.04269
oPyhexwatershed.pPyFlowline.aBasin[0].dThreshold_small_river = dResolution * 5
oPyhexwatershed.pPyFlowline.aBasin[0].dAccumulation_threshold = 0.01
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('dLongitude_outlet_degree', dLongitude_outlet_degree, iFlag_basin_in= 1)
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('dLatitude_outlet_degree', dLatitude_outlet_degree, iFlag_basin_in= 1)
#we want to change the flowline file, which is a geojson file
sFilename_flowline = realpath(os.path.join(sWorkspace_input, 'dggrid11/river_networks.geojson') )
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('sFilename_flowline_filter', sFilename_flowline, iFlag_basin_in= 1)
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('iFlag_debug', 0, iFlag_basin_in= 1)

oPyhexwatershed.iFlag_user_provided_binary = 1
oPyhexwatershed.pPyFlowline.iFlag_user_provided_binary = 0

oPyhexwatershed.pyhexwatershed_setup()
#run step 1
aCell_origin = oPyhexwatershed.pyhexwatershed_run_pyflowline()
oPyhexwatershed.pyhexwatershed_assign_elevation_to_cells(dMissing_value_in=-9999)
aCell_new = oPyhexwatershed.pyhexwatershed_update_outlet(aCell_origin)
oPyhexwatershed.pPyFlowline.pyflowline_export()
oPyhexwatershed.pyhexwatershed_export_config_to_json()
oPyhexwatershed.pyhexwatershed_run_hexwatershed()
oPyhexwatershed.pyhexwatershed_export()
#oPyhexwatershed.plot( sVariable_in = 'elevation',dData_min_in=0, iFlag_colorbar_in=1)
#oPyhexwatershed.plot( sVariable_in = 'flow_direction')
#oPyhexwatershed.plot( sVariable_in = 'drainage_area',dData_min_in=0 , iFlag_colorbar_in=1)
#oPyhexwatershed.plot( sVariable_in = 'travel_distance',dData_min_in=0, iFlag_colorbar_in=1)
sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'subbasin.png')
oPyhexwatershed.plot( sVariable_in = 'subbasin',dData_min_in=0, iFlag_colorbar_in=1, sFilename_output_in = sFilename)
sFilename = os.path.join(  oPyhexwatershed.sWorkspace_output_hexwatershed, 'hillslope.png')
oPyhexwatershed.plot( sVariable_in = 'hillslope',dData_min_in=0, iFlag_colorbar_in=1, sFilename_output_in = sFilename)
print('Finished the simulation.')



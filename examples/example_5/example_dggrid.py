import os
import sys
import json
from pathlib import Path
import shutil
from os.path import realpath
import importlib.util
from shutil import copy2
#now add the pyflowline into the Python path.

sPath_parent = str(Path().resolve()) 
print(sPath_parent)



#only for debug purpose
sPath_hexwatershed  = '/Users/liao313/workspace/python/pyhexwatershed'
sys.path.append(sPath_hexwatershed)
sPath_pyflowline  = '/Users/liao313/workspace/python/pyflowline'
sys.path.append(sPath_pyflowline)
sPath_pyearth  = '/Users/liao313/workspace/python/pyearth'
sys.path.append(sPath_pyearth)
print(sys.path)



#step 3
#load the read configuration function
from pyhexwatershed.change_json_key_value import change_json_key_value
from pyhexwatershed.pyhexwatershed_read_model_configuration_file import pyhexwatershed_read_model_configuration_file

print(sPath_parent)
sWorkspace_data = os.path.join( sPath_parent ,  'data', 'yukon' )
print(sWorkspace_data)
sWorkspace_input =  os.path.join( sWorkspace_data ,  'input')

sPath_bin = os.path.join( sPath_parent ,  'bin' )
os.environ["PATH"] += os.pathsep + sPath_bin

#create a temp folder to download data
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

# check if the destination directory exists
if os.path.exists(sWorkspace_input):
    # if it does, remove it
    shutil.rmtree(sWorkspace_input)
shutil.copytree(sPath_temp_data, sWorkspace_input,)



sFilename_configuration_in = realpath( sWorkspace_input +  '/pyhexwatershed_yukon_dggrid.json' )
sFilename_basins_in = realpath( sWorkspace_input +  '/pyflowline_yukon_basins.json' )
if os.path.isfile(sFilename_configuration_in):
    pass
else:
    print('This configuration does not exist: ', sFilename_configuration_in )

#set up some parameters
sMesh_type = 'dggrid' #the dggrid mesh type supported by hexwatershed
sDggrid_type = 'ISEA3H' #a type of dggrid mesh
iCase_index = 1 #a case index for bookmark
iResolution_index = 10 #dggrid resolution index, see dggrid documentation for details.
iFlag_stream_burning_topology = 1 #see hexwatershed documentation for details, also see the publication list.
iFlag_use_mesh_dem = 0
iFlag_elevation_profile = 0

#get today's year, month and day
from datetime import date
today = date.today()
iYear = today.year
iMonth = today.month
iDay = today.day
print("Today's date:", iYear, iMonth, iDay)
sDate = str(iYear) + str(iMonth).zfill(2) + str(iDay).zfill(2) #the date is also a bookmark to label a simulation
sWorkspace_output = sWorkspace_data + '/output/' #this is where the output will be stored

from pyflowline.mesh.dggrid.create_dggrid_mesh import dggrid_find_resolution_by_index
dResolution = dggrid_find_resolution_by_index(sDggrid_type, iResolution_index)
print(dResolution)  

#create a temporal hexwatershed object, later on we will modify several parameters
print(sFilename_configuration_in)
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration_in,
                    iCase_index_in=iCase_index,iFlag_stream_burning_topology_in=iFlag_stream_burning_topology,
                    iFlag_use_mesh_dem_in=0,
                    iFlag_elevation_profile_in=0,
                    iResolution_index_in = iResolution_index, 
                    sDggrid_type_in=sDggrid_type,
                    sDate_in = sDate, sMesh_type_in= sMesh_type, 
                    sWorkspace_output_in = sWorkspace_output)  

#first, we want to change the output directory, even if the json file might be correct, we change it anyway
sWorkspace_output_old = oPyhexwatershed.sWorkspace_output
#we will copy the example configuration files first, so we won't modify the original files
sFilename_configuration_copy= os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_copy.json' )
#copy the main configuration file to the output directory
copy2(sFilename_configuration_in, sFilename_configuration_copy)
#copy the basin configuration file to the output directory as well

sFilename_configuration_basins_copy = os.path.join( sWorkspace_output, 'pyhexwatershed_configuration_basins_copy.json' )    
copy2(sFilename_basins_in, sFilename_configuration_basins_copy)

#now we can modify these two configuration files without worrying about the original files
sFilename_configuration = sFilename_configuration_copy
sFilename_basins = sFilename_configuration_basins_copy
change_json_key_value(sFilename_configuration, 'sWorkspace_output', sWorkspace_output) #output folder
change_json_key_value(sFilename_configuration, 'sFilename_basins', sFilename_basins) #basin configuration file

#we want to change the boundary file, which is a geojson file
sFilename_mesh_boundary = realpath(os.path.join(sWorkspace_input, 'boundary.geojson')) #boundary to clip mesh
change_json_key_value(sFilename_configuration, 'sFilename_mesh_boundary', sFilename_mesh_boundary) 

sFilename_dem = realpath(os.path.join(sWorkspace_input, 'dem.tif')) #boundary to clip mesh
change_json_key_value(sFilename_configuration, 'sFilename_dem', sFilename_dem) 
#the read function accepts several keyword arguments that can be used to change the default parameters.
#the normal keyword arguments are:
#iCase_index_in: this is an ID to identify the simulation case
#sMesh_type_in: this specifies the mesh type ('mpas' in this example)
#sDate_in: this specifies the date of the simulation, the final output folder will have a pattern such as 'pyflowline20230901001', where pyflowline is model, 20230901 is the date, and 001 is the case index.
oPyhexwatershed = None
oPyhexwatershed = pyhexwatershed_read_model_configuration_file(sFilename_configuration,
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
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('dLongitude_outlet_degree', dLongitude_outlet_degree, iFlag_basin_in= 1)
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('dLatitude_outlet_degree', dLatitude_outlet_degree, iFlag_basin_in= 1)
#we want to change the flowline file, which is a geojson file
sFilename_flowline = realpath(os.path.join(sWorkspace_input, 'dggrid10/river_networks.geojson') )
oPyhexwatershed.pPyFlowline.pyflowline_change_model_parameter('sFilename_flowline_filter', sFilename_flowline, iFlag_basin_in= 1)

oPyhexwatershed.iFlag_user_provided_binary = 0 
oPyhexwatershed.pPyFlowline.iFlag_user_provided_binary = 0

oPyhexwatershed.pyhexwatershed_setup()
#run step 1
aCell_origin = oPyhexwatershed.pyhexwatershed_run_pyflowline()


oPyhexwatershed.pyhexwatershed_assign_elevation_to_cells()
aCell_new = oPyhexwatershed.pyhexwatershed_update_outlet(aCell_origin)
oPyhexwatershed.pPyFlowline.pyflowline_export()
oPyhexwatershed.pyhexwatershed_export_config_to_json()
oPyhexwatershed.pyhexwatershed_run_hexwatershed()
oPyhexwatershed.pyhexwatershed_analyze()
oPyhexwatershed.pyhexwatershed_export()

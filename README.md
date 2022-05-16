# Introduction

This a short course for the  <a href="https://www.hexwatershed.org/">`HexWatershed`</a> model.

For more details, please refer to the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

HexWatershed: a mesh independent flow direction model for hydrologic models.

Spatial discretization is the cornerstone of all spatially-distributed numerical simulations including watershed hydrology. Traditional square grid spatial discretization has several limitations:

1. It cannot represent adjacency uniformly;

2. It leads to the “island effect” and the diagonal travel path issue in D8 scheme;

3. It cannot provide a spherical coverage without significant spatial distortion;

4. It cannot be coupled with other unstructured mesh-based models such as the oceanic models.

Therefore, we developed a watershed delineation model (HexWatershed) based on the hexagon mesh spatial discretization.

We further improve HexWatershed to fully unstructured mesh-based to support variable-resolution meshes such as the MPAS mesh.

# Requirements

You need internet connection and several tools to run the examples in the tutorial.

To download the model and the tutorial repository, you need:

- git 

The whole `HexWatershed` package includes both the C++ backend and Python frontend. 
To compile and install the C++ backend, you need:

- C++ compiler, i.e., g++ 8.1.0 and above
- cmake 3.10 and above

To install the Python frontend, you need:

- conda 4.10 and above (anaconda or miniconda)

You need addition tools (e.g., QGIS) to visualize some of the model results.
Depending on your system, these tools can be obtained from these resources:

|       | MacOS |  Ubuntu | HPC |
| ---- | ----------- | -----------| -----------|
|git | |sudo apt install git-all| |
|Homebrew      | https://brew.sh/ | | |
|g++    | brew install gcc | sudo apt-get install g++ | module load gcc|
|cmake| brew install cmake| https://cmake.org/download/| module load cmake|
|conda| https://docs.conda.io/en/latest/miniconda.html | https://docs.conda.io/en/latest/miniconda.html | module load anaconda3 |
|VS Code| https://code.visualstudio.com/ |https://code.visualstudio.com/ |https://code.visualstudio.com/ |

# Step-by-step instruction

1. Download additional data files using an internet browser (Chrome recommended)

Download the `dem1.tif` and `lnd_cull_mesh.nc` files from the following url:

https://rcdemo.pnnl.gov/workshop/

2. Install the HexWatershed backend C++ component

- `git clone https://github.com/changliao1025/hexwatershed.git`

- `cd hexwatershed/build`

- If you are on MacOS, it is recommended to use the <a href="https://brew.sh/">`Homebrew`</a> to setup the g++ and cmake. 

   `cmake CMakeLists.txt -DCMAKE_CXX_COMPILER=g++-11`  
   
   Your homebrew installed g++ may have different versions, check it using `brew info gcc`.
   If your g++ is not in the system path, you may need to update/fix using `brew install gcc`.

   If you are on Linux, and the correct g++ is already in the system path

   `cmake CMakeLists.txt`

- `make install`

3. Install the HexWatershed frontend Python package 
   
   Create/activate a conda environment and install Python packages

- `conda config --set channel_priority strict`

- `conda create --name hexwatershed python=3.8`

- `conda activate hexwatershed`

- `conda install -c conda-forge gdal=3.2`

   you can test whether `gdal` is working using `from osgeo import gdal` in a Python session

- `conda install -c conda-forge hexwatershed`

Because the `GDAL` library is used by this project and the `proj` library is often not configured correctly automatically. 
On Linux or Mac, you can set it up using the `.bash_profile` such as:

Anaconda:

`export PROJ_LIB=/people/user/.conda/envs/hexwatershed/share/proj`

Miniconda:

`export PROJ_LIB=/opt/miniconda3/envs/hexwatershed/share/proj`

4. Download this tutorial

`git clone https://github.com/changliao1025/hexwatershed_tutorial.git`

You need to copy the compiled hexwatershed binary file into the `bin` folder. 

You need to copy the downloaded data files into the `input` folder.

5. Run the examples within the `example` folder

- You need to edit the template `configuration` json file to match with your data set paths.

- Depending where you downloaded the data and the example, different configurations are required.

6. Output files are stored within both `pyflowline` (conceptual river network) and `hexwatershed` (flow direction, etc.) folders. 
   
- Visualize the output `geojson` files using `QGIS`. 
  
- The `hexwatershed.json` file contains all the flow routing parameters.

# Miscellaneous

1. Why a hybrid Python and C++ approach?
   
   Answer: HexWatershed can be run at both regional and global scale, so performance is a factor. Data I/O is much easier in Python so users won't have to build `NetCDF` or `GDAL` from the source code.

2. What if my model doesn't produce the correct or expected answer?
   
   Answer: There are several hidden assumptions within the workflow. For example, if you provide the DEM and river network for two different regions, the program won't be able to tell you that. A visual inspection of your data is important.
   
   Optionally, you can turn on the `iFlag_debug` option in the configuration file to output the `intermediate files`.

3. Most common issues:

   - `conda` cannot create environment, turn off the VPN or bypass it.
   
   - `GDAL` not found, consider using the `conda-forge` channel or use an earlier version such as 3.2.

   - `proj` related issue https://github.com/OSGeo/gdal/issues/1546, make sure you correctly set up the `PROJ_LIB`

# Learn more

1. <a href="https://github.com/dengwirda/jigsaw">`JIGSAW`</a> is the mesh generator that is used to generator the variable resolution meshes.

2. Other meshes such as <a href="https://github.com/sahrk/DGGRID">`DGGrid`</a> will be supported.

3. The depression filling algorithm is modified based the <a href="https://github.com/r-barnes/richdem">`RichDEM`</a> priority-flood depression filling method.

# References

* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702

* Liao. C. (2022). Pyflowline: a mesh independent river network generator for hydrologic models. Zenodo. https://doi.org/10.5281/zenodo.6407299

* Liao. C. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.1). Zenodo. https://doi.org/10.5281/zenodo.6425881
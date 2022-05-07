# Introduction

This a short course for the HexWatershed model.

For more details, please refer to the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

# Requirements

You need internet connection and several tools to run the examples in the tutorial.

- conda 4.10 and above (anaconda or miniconda)
- cmake 3.10 and above
- c++ compiler 8.1.0 and above
- QGIS (optional)

You need addition tools (e.g., QGIS) to visualize some of the model results.

# Step-by-step instruction

1. Download additional data files using a internet brower (Chrome recommended)

Download the dem1.tif and lnd_cull_mesh.nc files from

https://rcdemo.pnnl.gov/workshop/

2. Install the HexWatershed C++ component

- `git clone https://github.com/changliao1025/hexwatershed.git`

- `cd hexwatershed/build`

- If you are using brew on MacOS:

   `cmake CMakeLists.txt -DCMAKE_CXX_COMPILER=g++-10`

  If you are on Linux, and the correct g++ is already in the system path

   `cmake CMakeLists.txt`

- `make install`

3. Create/activate a conda environment and install Python packages

- `conda config --set channel_priority strict`

- `conda create --name hexwatershed_tutorial python=3.8`

- `conda activate hexwatershed_tutorial`

- `conda install -c conda-forge gdal`

- `conda install -c conda-forge pyflowline`

- `pip install hexwatershed`

Because the `GDAL` library is used by this project and the `proj` library is often not configured correctly automatically. 
On Linux or Mac, you can set it up like this, `.bash_profile` as an example:

Anaconda:

`export PROJ_LIB=/people/user/.conda/envs/hexwatershed_tutorial/share/proj`

Miniconda:

`export PROJ_LIB=/opt/miniconda3/envs/hexwatershed_tutorial/share/proj`

4. Download this tutorial

`git clone https://github.com/changliao1025/hexwatershed_tutorial.git`

You need to copy the compiled hexwatershed binary file into the `bin` folder. 

You need to copy the downloaded data files into the `input` folder.

1. Run the examples within the `example` folder

- You need to edit the template configuration file to match with your data set paths.

- Depending where you downloaded the data and the example, different configurations are required.

# Miscellaneous

1. Why a hybrid Python and C++ approach?
   
   Answer: HexWatershed can be run at both regional and global scale, so performance is a factor. Data I/O is much easier in Python so users won't have to build NetCDF or GDAL from the source code.

2. What if my model doesn't produce the correct or expected answer?
   Answer: There are several hidden assumptions within the workflow. For example, if you provide the DEM and river network for two different regions, the program won't be able to tell you that. A visual inspection of your data in important.
   
   Optionally, you can turn on the `iFlag_debug` option in the configuration file to output the `intermediate files`.

3. Most common issues:
   
   - `GDAL` not found, consider using the `conda-forge` channel 

   - `proj` related issue https://github.com/OSGeo/gdal/issues/1546, make sure you correctly set up the `PROJ_LIB`


# References

* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702

* Liao. C. (2022). Pyflowline: a mesh independent river network generator for hydrologic models. Zenodo. https://doi.org/10.5281/zenodo.6407299

* Liao. C. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.1). Zenodo. https://doi.org/10.5281/zenodo.6425881
# Introduction

This is a short course for the  <a href="https://www.hexwatershed.org/">`HexWatershed`</a> model.

HexWatershed: a mesh independent flow direction model for hydrologic models.

Spatial discretization is the cornerstone of all spatially-distributed numerical simulations including watershed hydrology. Traditional square grid spatial discretization has several limitations:

1. It cannot represent adjacency uniformly;

2. It leads to the “island effect” and the diagonal travel path issue in D8 scheme;

3. It cannot provide a spherical coverage without significant spatial distortion;

4. It cannot be coupled with other unstructured mesh-based models such as the oceanic models.

Therefore, we developed a watershed delineation model (HexWatershed) based on the hexagon mesh spatial discretization.

We further improve HexWatershed to fully unstructured mesh-based to support variable-resolution meshes such as the `MPAS` mesh.

For more details, please refer to the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

# Requirements

You need internet connection and several tools to run the examples in the tutorial.

To download the model and the tutorial repository, you need:

- conda 4.10 and above (anaconda or miniconda)

You need addition tools (e.g., QGIS) to visualize some of the model results.

# Step-by-step instruction


1. Install the HexWatershed Python package 
   
   Create/activate a conda environment and install Python packages

- `conda create --name hexwatershed python=3.8`

- `conda activate hexwatershed`

- `conda install -c conda-forge hexwatershed`

Because the `GDAL` library is used by this project and the `proj` library is often not configured correctly automatically. 
On Linux or Mac, you can set it up using the `.bash_profile` such as:

Anaconda:

`export PROJ_LIB=/people/user/.conda/envs/hexwatershed/share/proj`

Miniconda:

`export PROJ_LIB=/opt/miniconda3/envs/hexwatershed/share/proj`

2. Download this tutorial

`git clone https://github.com/changliao1025/hexwatershed_tutorial.git`

3. Run the examples within the `example` folder

- You need to edit the template `configuration` json file to match with your data set paths.

- Depending where you downloaded the data and the example, different configurations are required.

4. Output files are stored within both `pyflowline` (conceptual river network) and `hexwatershed` (flow direction, etc.) folders. 
   
- Visualize the output `geojson` files using `QGIS`. 
  
- The `hexwatershed.json` file contains all the flow routing parameters.

# Behind the scene

In general, `HexWatershed` run the following the algorithms step-by-step.

1. Flowline simplication
2. Mesh generation
3. Topology reconstruction
4. Elevation resampling
5. Stream burning
6. Depression filling
7. Slope calculation
8. Flow direction
9. Flow accumulation
10. River networks
11. Export outputs

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

3. The depression filling algorithm is modified based on the <a href="https://github.com/r-barnes/richdem">`RichDEM`</a> priority-flood depression filling method.

4. HexWatershed can be run at both regional and global scale, see this Youtube clip for example: <a href="https://youtu.be/Y_NkLCazxMU">`Global scale HexWatershed simulation`</a>

# References

* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702

* Liao. C. (2022). Pyflowline: a mesh independent river network generator for hydrologic models. Zenodo. https://doi.org/10.5281/zenodo.6407299

* Liao. C. (2022). HexWatershed: a mesh independent flow direction model for hydrologic models (0.1.1). Zenodo. https://doi.org/10.5281/zenodo.6425881
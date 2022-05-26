# Introduction

This is a short course for the  <a href="https://www.hexwatershed.org/">`HexWatershed`</a> model.

HexWatershed: a mesh independent flow direction model for hydrologic models.

For full details of the model, please refer to our papers and the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

# Requirements

You need internet connection to install the  through the Python Pip or Conda (recommended) system.

You can use the Visual Studio Code to run the Python examples.

You can use QGIS to visualize some of the model results.

# Step-by-step instruction


1. Install the HexWatershed Python package through Conda

- `conda create --name hexwatershed python=3.8`

- `conda activate hexwatershed`

- `conda install -c conda-forge hexwatershed`

2. Download this tutorial

   `git clone https://github.com/changliao1025/hexwatershed_tutorial.git`

3. Run the examples within the `example` folder

- Edit the template `configuration` json file to match with your data set paths.

4. View and visualize model output files.
   
- View normal json file using any text editor such as VS Code.

- Visualize `geojson` files using `QGIS`. 
  

# FAQ

1. Why my `conda` cannot create environment?
   
   Turn off the VPN or bypass it.

2. Why import `GDAL` failed?
   
   Consider using the `conda-forge` channel.

3. `proj` related issue https://github.com/OSGeo/gdal/issues/1546, 
   
   Make sure you correctly set up the `PROJ_LIB`

   Because the `GDAL` library is used by this project and the `proj` library is often not configured correctly automatically. 
   On Linux or Mac, you can set it up using the `.bash_profile` such as:

   Anaconda:

   `export PROJ_LIB=/people/user/.conda/envs/hexwatershed/share/proj`

   Miniconda:

   `export PROJ_LIB=/opt/miniconda3/envs/hexwatershed/share/proj`

4. What if my model doesn't produce the correct or expected answer?
   
   Answer: There are several hidden assumptions within the workflow. For example, if you provide the DEM and river network for two different regions, the program won't be able to tell you that. A visual inspection of your data is important.
   
   Optionally, you can turn on the `iFlag_debug` option in the configuration file to output the `intermediate files`.

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
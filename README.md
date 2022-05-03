# Introduction
This a short course for the HexWatershed model.
For more details, please refer to the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

# Requirements

You need internet connection and several tools to run the examples in the tutorial.

- conda 
- cmake
- c++ compiler
- QGIS (optional)

You need addition tools (e.g., QGIS) to visulize some of the model results.

# Step-by-step instruction


1. Download additional data files using a internet brower (Chrome recommended)

Download the dem1.tif and lnd_cull_mesh.nc files from

https://rcdemo.pnnl.gov/workshop/

2. Install the HexWatershed C++ component

- `git clone https://github.com/changliao1025/hexwatershed.git`

- `cd hexwatershed/build`

- `cmake CMakeLists.txt  -DCMAKE_CXX_COMPILER=g++-10`

- `make install`

3. Create/activate a conda environment and install Python packages

- `conda create --name hexwatershed_tutorial python=3.8`

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

5. Run the examples within the `example` folder

- You need to edit the template configuration file to match with your data set.

- Depending where you downloaded the data and the example, different configurations are required.


# References

* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702
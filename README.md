# Introduction
This a short course for the HexWatershed model.
For more details, please refer to the HexWatershed documentation (https://hexwatershed.readthedocs.io/).

# Requirements

You need internet connection and several tools to run the examples in the tutorial.

- conda 
- cmake
- c++ compiler

You need addition tools to visulize some of the model results.

# Step-by-step instruction

1. Create and activate a conda environment for this tutorial

`conda create --name hexwatershed_tutorial python=3.8`

2. Install depedency packages

`conda install -c conda-forge pyflowline`
`pip install hexwatershed`

3. Clone this repository

`git clone https://github.com/changliao1025/hexwatershed_tutorial.git`

4. Download additional data files using a internet brower (Chrome recommended)

Download the dem1.tif and lnd_cull_mesh.nc files from

https://rcdemo.pnnl.gov/workshop/

5. 


# Suggested reading

# References

* Liao, Chang, Tian Zhou, Donghui Xu, Richard Barnes, Gautam Bisht, Hong-Yi Li, Zeli Tan, et al. (02/2022AD) 2022. “Advances In Hexagon Mesh-Based Flow Direction Modeling”. Advances In Water Resources 160. Elsevier BV: 104099. 
https://doi.org/10.1016/j.advwatres.2021.104099.

* Liao, C., Tesfa, T., Duan, Z., & Leung, L. R. (2020). Watershed delineation on a hexagonal mesh grid. Environmental Modelling & Software, 128, 104702. https://doi.org/10.1016/j.envsoft.2020.104702
# top-quark-mass-reconstruction
Physics data analysis project reconstructing the top quark mass from simulated LHC collision events using Python.
# Top Quark Mass Reconstruction

## Overview

This project reconstructs the mass of the top quark from simulated Large Hadron Collider (LHC) collision data using Python. The analysis uses invariant mass calculations to identify W boson candidates and reconstruct top quark decay products.

## Features

- Invariant mass reconstruction from four-momentum data
- W boson candidate identification
- Top quark mass reconstruction
- Histogram analysis of reconstructed masses
- Gaussian fitting using SciPy
- Data visualisation with Matplotlib

## Technologies

- Python
- NumPy
- Pandas
- Matplotlib
- SciPy

## Physics

The invariant mass is calculated using:

m² = E² − pₓ² − pᵧ² − pz²

Jet pairs are combined to reconstruct W bosons and then combined with b-jets to reconstruct top quark candidates.

## Author

Carolina Escalante  
BSc Physics with Astrophysics  
Queen Mary University of London

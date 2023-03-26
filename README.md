# Welcome on sismo-memo repository !

This GitHub repository has been created in the frame of my master thesis in Master in Environmental Science and Management, Focus : Environmental Science at the Université Libre de Bruxelles. 
The thesis studies the interactions at the interface between the bed-water-ice of the Vatnajökull ice-cap situated in Iceland based on seismic data. The study and the repository is mainly subdivided into 3 approaches in seismology : Seismic-wave velocity changes, Horizontal-to-vertical spectral ratio and glacial hydrological tremor.

## Seismic velocity change (DV/V) :

The data are provided by the permanent stations of the Icelandic Meteorological Office (IMO). The velocity variations of seismic-wave are continuously studied during 4 years between the 1^$st$ January 2018 and the 1^$st$ Januare 2022 and computed in xx different frequency ranges with MSNoise 1.6 ; a Python package realised by Lecocq et al (2017) at the Royal Observatory of Belgium (ROB). For this part, any jupyter notebooks are related to the processing or the computation of DV/V but they are used to make plots or determine the sensitive kernels of Rayleigh or Love waves.

### Jupyter Notebooks :

InterferoMsNoise.ipynb : used to make DV/V plots between each station pairs.
03_SW_Sensitivity_kernel.ipynb : determine the sensitivity kernels of Rayleigh and Love wave based on a Vs and Vp model. Not available for now.

## Horizontal-to-vertical spectral ratio :

### Jupyter Notebooks :

Ice-thickness.ipynb : used to compute the hvsr of each station based on the hvsrpy 1.0.0 Python package of Vanatassel 20xx. This notebook used also a simple model to retrieved the ice thickness of each sensors.
Ice_polar.ipynb : creates rotate plots from hvsrpy 1.0.0 Python package and Geopsy (Wathelet et al. 2017) and finds the azimuth of the maximum HV Amplitude.

## Glacial hydrological tremor :

### Jupyter Notebooks :

hydro-glacier.ipynb : analyses the relationship between the power spectral density and the water discharge.

## Others :

### Jupyter Notebooks :

gnss-temp.ipynb : extracts the GPS location and temperature of the 3 components SmartSolo from the DigiSolo.LOG.
netCDF-reader.ipynb : extracts the temperature, snow melt and precipitation from reanalyzed ERA-5 NetCDF file of Copernicus. 

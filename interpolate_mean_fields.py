"""
Interpolate the non-uniformly spaced data from the zonally and temporally averaged coupled model
onto the uniform grid of the CANAL. Save the interpolated fields as txt files

"""

import numpy                  as np
import scipy.interpolate      as interp
import xarray                 as xr

# Load the datasets with the zonally and temporally averaged data
umean = xr.open_dataset(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/umean_u-bx950_Jul_Aug.nc')
tmean = xr.open_dataset(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/tmean_u-bx950_Jul_Aug.nc')

rn_domszz = 1000; rn_dy = 20 # from namelist_cfg (read data from FORTRAN?)
rn_domszy = 3300; rn_dz = 20 # from namelist_cfg (read data from FORTRAN?)

# Specify the uniform grid in the CANAL
depth_canal = np.linspace(rn_domszz, 0, int(rn_domszz/rn_dz))
lat_canal   = np.linspace(-rn_domszy/(2*111), rn_domszy/(2*111), int(rn_domszy/rn_dy))

# Interpolate the non-uniform data onto the uniform grid
umean_canal = umean.uo.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})
tmean_canal = tmean.thetao.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})

# Convert to numpy arrays, flatten, and then save the data
np.savetxt(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/U_TIW.txt',umean_canal.values.flatten())
np.savetxt(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/T_TIW.txt',tmean_canal.values.flatten())

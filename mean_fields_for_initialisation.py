"""
Save the mean fields for initilisation of the CANAL

"""

import glob
import xarray as xr

# List the files from the coupled model
U_infile = glob.glob("/gws/nopw/j04/oxford_es/jrees/u-bx950/onm/EqPac*_grid_U.nc")[120:-1]
T_infile = glob.glob("/gws/nopw/j04/oxford_es/jrees/u-bx950/onm/EqPac*_grid_T.nc")[120:-1]

# Open the datasets
U_dataset = xr.open_mfdataset(U_infile)
T_dataset = xr.open_mfdataset(T_infile)        
    
# Rename the dimensions
U_dataset = U_dataset.rename({'time_counter':'time','depthu':'depth'})
T_dataset = T_dataset.rename({'time_counter':'time','deptht':'depth'})

# Extract the region 15S-15N, 110-160W, 0-1100m
xW25 = 80;  xE25 = 282; yS25 = 21; yN25 = 144; depthT25 = 0; depthB25 = 1100

uoce = U_dataset.uo.sel(x=slice(xW25,xE25),y=slice(yS25,yN25),depth=slice(depthT25,depthB25))
toce = T_dataset.thetao.sel(x=slice(xW25,xE25),y=slice(yS25,yN25),depth=slice(depthT25,depthB25))  

# Group the data by month and average zonally and temporally
umean = uoce.groupby('time.month').mean(dim='time').mean(dim='x')
tmean = toce.groupby('time.month').mean(dim='time').mean(dim='x')

# Select the data from July-August and average temporally
umean  = umean.isel(month=slice(5, 7)).mean(dim='month')
tmean  = tmean.isel(month=slice(5, 7)).mean(dim='month')

# For interpolation, it is easier to relabel the dimensions as follows
umean = xr.DataArray(umean, coords={'depth': depth, 'latitude': latitude}, dims=['depth', 'latitude'])
tmean = xr.DataArray(tmean, coords={'depth': depth, 'latitude': latitude}, dims=['depth', 'latitude'])

rn_domszz = 1000; rn_dy = 20 # from namelist_cfg (read data from FORTRAN?)
rn_domszy = 3300; rn_dz = 20 # from namelist_cfg (read data from FORTRAN?)

# Specify the uniform grid in the CANAL
depth_canal = np.linspace(0, rn_domszz, int(rn_domszz/rn_dz))
lat_canal   = np.linspace(-rn_domszy/(2*111), rn_domszy/(2*111), int(rn_domszy/rn_dy))

# Interpolate the non-uniform data onto the uniform grid
umean_canal = umean.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})
tmean_canal = tmean.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})

# Convert to numpy arrays, flatten, and then save the data
np.savetxt(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/U_TIW.txt',umean_canal.values.flatten())
np.savetxt(f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/T_TIW.txt',tmean_canal.values.flatten())

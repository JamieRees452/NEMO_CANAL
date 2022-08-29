"""
Calculate and save the zonally and temporally averaged data from the
coupled atmosphere-ocean integration

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

# Save the zonally and temporally averaged data in netCDF format
umean.to_netcdf(path=f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/umean_u-bx950_Jul_Aug.nc')
tmean.to_netcdf(path=f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL/mean_fields/tmean_u-bx950_Jul_Aug.nc')

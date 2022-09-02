"""
Save the mean fields for initilisation of the CANAL
"""

import glob
import numpy             as np
import scipy.interpolate as interp
import xarray            as xr

MY_CANAL_directory = f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL'
my_group_workspace = f'/gws/nopw/j04/oxford_es/jrees'

latitude = np.loadtxt(f'{MY_CANAL_directory}/mean_fields/latitude_nonuniform.txt')
depth    = np.loadtxt(f'{MY_CANAL_directory}/mean_fields/depth_nonuniform.txt')

# -------------------------------------------------------------------------------------------------------
# Zonally and temporally averaged mean fields from the coupled model 
# -------------------------------------------------------------------------------------------------------

U_infile = glob.glob(f'{my_group_workspace}/u-bx950/onm/EqPac*_grid_U.nc')
T_infile = glob.glob(f'{my_group_workspace}/u-bx950/onm/EqPac*_grid_T.nc')
        
U_dataset = xr.open_mfdataset(U_infile).rename({'time_counter':'time','depthu':'depth'})
T_dataset = xr.open_mfdataset(T_infile).rename({'time_counter':'time','deptht':'depth'})

uoce = U_dataset.uo.sel(x=slice(xW25,xE25),y=slice(yS25,yN25),depth=slice(depthT25,depthB25))
toce = T_dataset.thetao.sel(x=slice(xW25,xE25),y=slice(yS25,yN25),depth=slice(depthT25,depthB25)) 

umean = uoce.groupby('time.month').mean(dim='time').mean(dim='x')
tmean = toce.groupby('time.month').mean(dim='time').mean(dim='x')

umean  = umean.isel(month=slice(5, 7)).mean(dim='month')
tmean  = tmean.isel(month=slice(5, 7)).mean(dim='month')

# -------------------------------------------------------------------------------------------------------
# From text files
# -------------------------------------------------------------------------------------------------------

# If loading the text data
#umean = np.loadtxt(f'{MY_CANAL_directory}/mean_fields/umean.txt'); umean = np.reshape(umean, (47, 123))
#tmean = np.loadtxt(f'{MY_CANAL_directory}/mean_fields/tmean.txt'); tmean = np.reshape(tmean, (47, 123))

# For interpolation, it is easier to relabel the dimensions as follows
umean_new = xr.DataArray(umean, coords={'depth': depth, 'latitude': latitude}, dims=['depth', 'latitude'])
tmean_new = xr.DataArray(tmean, coords={'depth': depth, 'latitude': latitude}, dims=['depth', 'latitude'])

# ------------------------------------------------------------------------------------------------------------
# Interpolate onto the CANAL grid
# ------------------------------------------------------------------------------------------------------------
rn_domszx = 5560; rn_dx = 20; x_points = int(rn_domszx/rn_dx) + 1
rn_domszy = 3340; rn_dy = 20; y_points = int(rn_domszy/rn_dy) + 1
rn_domszz = 1000; rn_dz = 20; z_points = int(rn_domszz/rn_dz) + 1

lon_canal   = np.linspace(0, rn_domszx, x_points)
lat_canal   = np.linspace(-rn_domszy/2, rn_domszy/2, y_points)
depth_canal = np.linspace(0, rn_domszz, z_points)

# Interpolate onto the uniform CANAL grid
umean_canal = umean_new.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})
tmean_canal = tmean_new.interp(latitude=lat_canal, depth=depth_canal, kwargs={"fill_value": "extrapolate"})

# -----------------------------------------------------------------------------------------------------------
# Broadcast into longitude
# -----------------------------------------------------------------------------------------------------------

# We initialise using 3D netCDF data hence we need longitude (use np.ones to keep lat-depth fields zonally invariant)
lon = xr.DataArray(np.ones(x_points), [("longitude", lon_canal)])

# Broadcast arrays to repeat (similar to np.tile)
umean_canal = lon*umean_canal 
tmean_canal = lon*tmean_canal 

umean_canal = umean_canal.transpose("depth", "latitude", "longitude")
tmean_canal = tmean_canal.transpose("depth", "latitude", "longitude")

vmean_canal = xr.zeros_like(umean_canal)
smean_canal = 35*xr.ones_like(tmean_canal)

umean_canal = xr.DataArray(umean_canal, name='zonal_velocity')
vmean_canal = xr.DataArray(vmean_canal, name='meridional_velocity')
tmean_canal = xr.DataArray(tmean_canal, name='temperature')
smean_canal = xr.DataArray(smean_canal, name='salinity')

# -----------------------------------------------------------------------------------------------------------
# Save to netCDF
# -----------------------------------------------------------------------------------------------------------

# Save data to netCDF
umean_canal.to_netcdf(f'{MY_CANAL_directory}/EXP00/umean_canal.nc')
umean_canal.to_netcdf(f'{MY_CANAL_directory}/EXP00/vmean_canal.nc')
tmean_canal.to_netcdf(f'{MY_CANAL_directory}/EXP00/tmean_canal.nc')
smean_canal.to_netcdf(f'{MY_CANAL_directory}/EXP00/smean_canal.nc')

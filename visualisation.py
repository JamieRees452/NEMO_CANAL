"""
Visualisation of the outputs for the CANAL
"""

import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import glob

MY_CANAL_directory = f'/home/users/jme22rs/NEMO/NEMO_CANAL/NEMO/tests/MY_CANAL'

U_dataset = xr.open_mfdataset(f'{MY_CANAL_directory}/EXP00/CANAL_grid_U.nc').rename({'time_counter':'time'})
V_dataset = xr.open_mfdataset(f'{MY_CANAL_directory}/EXP00/CANAL_grid_V.nc').rename({'time_counter':'time'})
W_dataset = xr.open_mfdataset(f'{MY_CANAL_directory}/EXP00/CANAL_grid_W.nc').rename({'time_counter':'time'})
T_dataset = xr.open_mfdataset(f'{MY_CANAL_directory}/EXP00/CANAL_grid_T.nc').rename({'time_counter':'time'})

uoce = U_dataset.uoce
voce = V_dataset.voce
woce = W_dataset.woce
toce = T_dataset.toce
soce = T_dataset.soce

fig, axes=plt.subplots(figsize=(6,3),dpi=300)

uoce.isel(time=0,depthu=1).plot.contourf(yincrease=False,levels=20,ax=axes,add_colorbar=False,cmap='RdBu_r')

plt.xlabel(f'',fontsize=14)
plt.ylabel(f'',fontsize=14)
plt.title(f't={0}',loc='center')

plt.tight_layout()
plt.show()
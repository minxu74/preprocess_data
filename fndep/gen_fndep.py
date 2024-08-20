#!/usr/bin/env python

import xarray as xr
import os
import numpy as np
import netCDF4 as nc4


scen = 'ssp126'



if scen == 'ssp370':
   ds_drynhx = xr.open_dataset("drynhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-209912.nc")
   ds_drynoy = xr.open_dataset("drynoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-209912.nc")
   ds_wetnhx = xr.open_dataset("wetnhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-209912.nc")
   ds_wetnoy = xr.open_dataset("wetnoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-209912.nc")
elif scen == 'ssp534':

   ds_drynhx = xr.open_dataset("drynhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-210012.nc")
   ds_drynoy = xr.open_dataset("drynoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-210012.nc")
   ds_wetnhx = xr.open_dataset("wetnhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-210012.nc")
   ds_wetnoy = xr.open_dataset("wetnoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-"+scen+"-1-0_gn_201501-210012.nc")

elif scen == 'ssp126':
   ds_drynhx = xr.open_dataset("drynhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp126-1-0_gn_201501-209912.nc")
   ds_drynoy = xr.open_dataset("drynoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp126-1-0_gn_201501-209912.nc")
   ds_wetnhx = xr.open_dataset("wetnhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp126-1-0_gn_201501-209912.nc")
   ds_wetnoy = xr.open_dataset("wetnoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp126-2-0_gn_201501-209912.nc")


print (ds_drynhx.time.dt.days_in_month)

#my = (ds_drynhx.drynhx * 86400. * ds_drynhx.time.dt.days_in_month).groupby('time.year').sum('time') 
#ot = (ds_drynhx.drynhx * 86400. * ds_drynhx.time.dt.days_in_month).resample(time="AS").sum(dim="time")
#np.testing.assert_allclose(my.values, ot.values)

# kg m-2 s-1  - > g(N)/m2/yr

# kg m-2 s-1 kg m-2 yr-1
# 0 - 2015 - 84 -2099
drynhx = (ds_drynhx.drynhx * 86400. * ds_drynhx.time.dt.days_in_month).groupby('time.year').sum('time') 
wetnhx = (ds_wetnhx.wetnhx * 86400. * ds_wetnhx.time.dt.days_in_month).groupby('time.year').sum('time') 
NDEP_NHx_year = drynhx + wetnhx

drynoy = (ds_drynoy.drynoy * 86400. * ds_drynoy.time.dt.days_in_month).groupby('time.year').sum('time') 
wetnoy = (ds_wetnoy.wetnoy * 86400. * ds_wetnoy.time.dt.days_in_month).groupby('time.year').sum('time') 
NDEP_NOy_year = drynoy + wetnoy

NDEP_year = NDEP_NHx_year + NDEP_NOy_year

#drynhx.variables['drynhx'] 

#print (NDEP_year.isel(time=0).sum(dim=("lat", "lon"))

#cdate="c220610"
cdate="c220708"
os.system("cp -f fndep_elm_cbgc_exp_simyr1849-2101_1.9x2.5_c190103.nc fndep_elm_cbgc_exp_simyr1849-2101_1.9x2.5_ncar_ccmi_"+scen+"_"+cdate+".nc")
fndep = nc4.Dataset("fndep_elm_cbgc_exp_simyr1849-2101_1.9x2.5_ncar_ccmi_"+scen+"_"+cdate+".nc", "r+")


#kg m-2 yr-1 g m-2 yr-1

# 0 - 1849, 252 -2101, 166-2015, 251-2100

# 2015-2099
fndep.variables['NDEP_NHx_year'][166:251,:,:] = NDEP_NHx_year.values[0:85,:,:] * 1000.
# 2100-2101
fndep.variables['NDEP_NHx_year'][251    ,:,:] = NDEP_NHx_year.values[84  ,:,:] * 1000.
fndep.variables['NDEP_NHx_year'][252    ,:,:] = NDEP_NHx_year.values[84  ,:,:] * 1000.

fndep.variables['NDEP_NOy_year'][166:251,:,:] = NDEP_NOy_year.values[0:85,:,:] * 1000.
fndep.variables['NDEP_NOy_year'][251    ,:,:] = NDEP_NOy_year.values[84  ,:,:] * 1000.
fndep.variables['NDEP_NOy_year'][252    ,:,:] = NDEP_NOy_year.values[84  ,:,:] * 1000.

fndep.variables['NDEP_year'    ][166:251,:,:] = NDEP_year.values    [0:85,:,:] * 1000.
fndep.variables['NDEP_year'    ][251    ,:,:] = NDEP_year.values    [84  ,:,:] * 1000.
fndep.variables['NDEP_year'    ][252    ,:,:] = NDEP_year.values    [84  ,:,:] * 1000.

#-netcdf fndep_elm_cbgc_exp_simyr1849-2101_1.9x2.5_c190103 {
#-dimensions:
#-        lat = 96 ;
#-        lon = 144 ;
#-        time = 253 ;
#-variables:
#-        float NDEP_NHx_year(time, lat, lon) ;
#-                NDEP_NHx_year:long_name = "NHx deposition" ;
#-                NDEP_NHx_year:units = "g(N)/m2/yr" ;
#-        float NDEP_NOy_year(time, lat, lon) ;
#-                NDEP_NOy_year:long_name = "NOy deposition" ;
#-                NDEP_NOy_year:units = "g(N)/m2/yr" ;
#-        float NDEP_year(time, lat, lon) ;
#-                NDEP_year:long_name = "Sum of NOy and NHx deposition" ;
#-                NDEP_year:units = "g(N)/m2/yr" ;
#-        double time(time) ;
#-                time:long_name = "time" ;
#-                time:calendar = "noleap" ;
#-                time:units = "days since 0000-01-01 00:00" ;
#-        int YEAR(time) ;
#-                YEAR:long_name = "year" ;
#-                YEAR:units = "Year AD" ;
#-        double lat(lat) ;
#-                lat:long_name = "latitude" ;
#-                lat:units = "degrees_north" ;
#-        double lon(lon) ;
#-                lon:long_name = "longitude" ;
#-                lon:units = "degrees_east" ;
#-                :source1 = "drynhx_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc" ;
#-                :source2 = "wetnhx_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc" ;
#-                :source3 = "drynoy_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc" ;
#-                :source4 = "wetnoy_input4MIPs_surfaceFluxes_CMIP_NCAR-CCMI-2-0_gn_185001-201412.nc" ;
#-                :source5 = "drynhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp585-1-0_gn_201501-209912.nc" ;
#-                :source6 = "wetnhx_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp585-1-0_gn_201501-209912.nc" ;
#-                :source7 = "drynoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp585-1-0_gn_201501-209912.nc" ;
#-                :source8 = "wetnoy_input4MIPs_surfaceFluxes_ScenarioMIP_NCAR-CCMI-ssp585-2-0_gn_201501-209912.nc" ;
#-                :history = "Jan 03 2019 created" ;
#-                :comment = "1849 repeat 1850 data + 1850-2014 historical data + 2015-2099 ssp5-85 data + 2100,2101 repeat 2099 data" ;




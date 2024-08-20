#!/usr/bin/env bash

# Min Xu; ORNL; 2021/10/05


module load nco


rubisco_cmip6_ssp=/global/project/projectdirs/m2467/prj_minxu/rubisco_cmip6_ssp

# info from GHG_CMIP_SSP585-1-2-1_Annual_Global_2015-2500_c20190310.n
#-input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-cfc11eq-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc
#-input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-cfc12-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc
#-input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-nitrous-oxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc
#-input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-methane-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc
#-input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc

#ncrcat Data_for_E3SM/temp3b.nc Data_for_E3SM/temp_last_time.nc Data_for_E3SM/temp_last_time.nc Data_for_E3SM/temp4.nc
#ncks --mk_rec_dmn time --no_abc Data_for_E3SM//temp3.nc Data_for_E3SM//temp3b.nc

#ncrename -v mole_fraction_of_cfc11eq_in_air,f11 Data_for_E3SM//temp3.nc
#ncrename -v mole_fraction_of_cfc12_in_air,f12 Data_for_E3SM//temp3.nc
#ncrename -v mole_fraction_of_nitrous_oxide_in_air,N2O Data_for_E3SM/temp3.nc
#ncrename -v mole_fraction_of_methane_in_air,CH4 Data_for_E3SM//temp3.nc
#ncrename -v mole_fraction_of_carbon_dioxide_in_air,CO2 Data_for_E3SM//temp3.nc
#ncks -O -x -v sector,sector_bnds Data_for_E3SM//temp2.nc Data_for_E3SM/temp3.nc
#ncwa -O --average sector Data_for_E3SM/temp1.nc Data_for_E3SM//temp2.nc

#ncks -A --no_abc -d sector,0,0 input4MIPS_data/SSP5_8.5_v1.2.1/mole-fraction-of-cfc11eq-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc Data_for_E3SM//temp1.nc
#ncks -A --no_abc -d sector,0,0 input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-cfc12-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc Data_for_E3SM//temp1.nc
#ncks -A --no_abc -d sector,0,0 input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-nitrous-oxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc Data_for_E3SM/temp1.nc
#ncks -A --no_abc -d sector,0,0 input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-methane-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc Data_for_E3SM/temp1.nc
#ncks -A --no_abc -d sector,0,0 input4MIPS_data/SSP5_8.5_v1.2.1//mole-fraction-of-carbon-dioxide-in-air_input4MIPs_GHGConcentrations_ScenarioMIP_UoM-REMIND-MAGPIE-ssp585-1-2-1_gr1-GMNHSH_2015-2500.nc Data_for_E3SM/temp1.nc

# CO2, CH4, N2O, f12, f11

gasvarnames=(mole-fraction-of-cfc11eq-in-air mole-fraction-of-cfc12-in-air mole-fraction-of-nitrous-oxide-in-air mole-fraction-of-methane-in-air mole-fraction-of-carbon-dioxide-in-air)

gasvarne3sm=(f11 f12 N2O CH4 CO2)


scen='ssp534'
i=0
for var in "${gasvarnames[@]}"; do
    fvar=`/bin/ls ./ggas/$var*$scen*`
    ncks -A --no_abc -d sector,0,0 $fvar temp1.nc
    i=$((i+1))
done
# remove the sector dimension
ncwa -O --average sector temp1.nc temp2.nc
ncks -O -x -v sector,sector_bnds temp2.nc temp3.nc


# change names
i=0
for var in "${gasvarnames[@]}"; do
    
  
    echo ${var//-/_}
    echo ncrename -v ${var//-/_},${gasvarnes3m[$i]} temp3.nc
    ncrename -v ${var//-/_},${gasvarne3sm[$i]} temp3.nc 
    i=$((i+1))
done

# make time to be record dimension
ncks --mk_rec_dmn time --no_abc temp3.nc temp3a.nc
ncap2 -s 'date=array(20150701,10000,$time); adj=array(0.0,0.0,$time)' temp3a.nc temp3b.nc

ncatted -a long_name,date,c,c,'current date as yyyymmdd' temp3b.nc
ncatted -a long_name,adj,c,c,'f11 scaling factor =>  f11_adjusted = f11 * (1 + adj).' temp3b.nc


cdate=`date +"%y%m%d"`
#GHG_CMIP_SSP585-1-2-1_Annual_Global_2015-2500_c20190310.nc
#                string date:long_name = "current date as yyyymmdd" ;
#        float adj(time) ;
#                string adj:long_name = "f11 scaling factor =>  f11_adjusted = f11 * (1 + adj)." ;

/bin/mv -f temp3b.nc $rubisco_cmip6_ssp/GHG_CMIP6_${scen^^}-1-2-1_Annual_Global_2015-2500_$cdate.nc

/bin/rm -f temp1.nc temp2.nc temp3.nc temp3a.nc


#chlorine loading

#Cly = 3*CFC11 + 2*CFC12 + 3*CFC113 + 2*CFC114 + CFC115 + HCFC22 + 2*HCFC141b + HCFC142b + halon1211 +
# CH3Cl + 4*CCl4 + 3*CH3CCl3

clspecies=(CFC11 CFC12 CFC113 CFC114 CFC115 HCFC22 HCFC141b HCFC142b halon1211 CH3Cl CCl4 CH3CCl3)
clweights=(  3     2     3      2      1      1       2         1        1       1     4     3)


arrVar=()
for var in "${clspecies[@]}"; do
    if [[ $var == 'CCl4' ]]; then
        clfile=`/bin/ls ggas/*carbon-tetrachloride-in-air*${scen}*.nc`
    else
        if [[ $var == 'CH3Cl' ]]; then
            clfile=`/bin/ls ggas/*methyl-chloride-in-air*${scen}*.nc`
        else
            clfile=`/bin/ls ggas/*${var,,}-in-air*${scen}*.nc`
        fi
    fi
    bfile=${clfile##*/}
    tvar=(${bfile//_/ })
    nvar=${tvar[0]}
    arrVar+=(${nvar//-/_}) 
    ncks -A --no_abc -d sector,0,0 $clfile temp1.nc
done


echo "${arrVar[*]}"


eqstring="cyl=0.0"
i=0
for var in "${arrVar[@]}"; do
    eqstring+="+$var*${clweights[$i]}"
    i=$((i+1))
done

echo $eqstring


# remove the sector dimension
ncwa -O --average sector temp1.nc temp2.nc
ncks -O -x -v sector,sector_bnds temp2.nc temp3.nc

set -x



ncap2 -s "$eqstring" temp3.nc temp3b.nc


/bin/rm -f temp1.nc temp2.nc temp3.nc

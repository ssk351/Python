############################################
###Script to write the NETCDF data into ASCII format
### Data format col-1 DATE (yyyy-mm-dd), col-2 LATITUDE(Degrees)
### col-3 LONGIUDE, and col-4 PARAMETER(Rainfall)
############################################
import netCDF4 as nc
import numpy as np

def netcdf_to_ascii(nc_file, parameter, ascii_file):
    # Open the NetCDF file
    ds = nc.Dataset(nc_file, 'r')

    # Read the dimensions and variables
    time = ds.variables['TIME'][:]
    lat = ds.variables['LATITUDE'][:]
    lon = ds.variables['LONGITUDE'][:]
    param = ds.variables[parameter][:]

    # Convert time to days assuming units are 'days since ...'
    time_units = ds.variables['TIME'].units
    days = nc.num2date(time, units=time_units)

    # Open the ASCII file for writing
    with open(ascii_file, 'w') as f:
        # Write the header
        f.write("days,latitude,longitude,{}\n".format(parameter))

        # Write the data
        for t_idx, t in enumerate(days):
            for lat_idx, latitude in enumerate(lat):
                for lon_idx, longitude in enumerate(lon):
                    value = param[t_idx, lat_idx, lon_idx]
                    f.write("{},{},{},{}\n".format(t.strftime('%Y-%m-%d'), latitude, longitude, value))

    # Close the NetCDF file
    ds.close()

# Example usage
nc_file = '/scratch/sahiduli/SSK/OBS/RF/DD/IMDP25/imd_2021.nc'
parameter = 'Rainfall'  # Change this to the actual parameter name in your NetCDF file
ascii_file = 'output.txt'
netcdf_to_ascii(nc_file, parameter, ascii_file)

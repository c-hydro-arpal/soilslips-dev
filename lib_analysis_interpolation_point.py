"""
Library Features:

Name:          lib_analysis_interpolation_point
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20200515'
Version:       '1.0.0'
"""

#######################################################################################
# Logging
import logging
import tempfile
import rasterio
import os

from numpy import zeros, min, max, flipud, savetxt

from lib_utils_system import create_filename_tmp
from lib_utils_process import exec_process
from lib_utils_system import random_string, make_folder

from lib_info_args import logger_name_scenarios as logger_name

# Logging
log_stream = logging.getLogger(logger_name)

# Debug
# import matplotlib.pylab as plt
#######################################################################################


# -------------------------------------------------------------------------------------
# Method to interpolate point data to map
def interp_point2map(data_in_1d, geox_in_1d, geoy_in_1d, geox_out_2d, geoy_out_2d, epsg_code='4326',
                      interp_no_data=-9999.0, interp_radius_x=None, interp_radius_y=None,
                      interp_method='nearest', interp_option=None,
                      folder_tmp=None, var_name_data='values', var_name_geox='x', var_name_geoy='y'):

    # Define layer name (using a random string)
    var_name_layer = random_string()

    # Define temporary folder
    if folder_tmp is None:
        folder_tmp = tempfile.mkdtemp()

    # Check interpolation radius x and y
    if (interp_radius_x is None) or (interp_radius_y is None):
        logging.error(' ===> Interpolation radius x or y are undefined.')
        raise ValueError('Radius must be defined')

    # Define temporary file(s)
    file_name_csv = os.path.join(folder_tmp, var_name_layer + '.csv')
    file_name_vrt = os.path.join(folder_tmp, var_name_layer + '.vrt')
    file_name_tiff = os.path.join(folder_tmp, var_name_layer + '.tiff')

    # Define geographical information
    geox_out_min = min(geox_out_2d)
    geox_out_max = max(geox_out_2d)
    geoy_out_min = min(geoy_out_2d)
    geoy_out_max = max(geoy_out_2d)
    geo_out_cols = geox_out_2d.shape[0]
    geo_out_rows = geoy_out_2d.shape[1]

    # Define dataset for interpolating function
    data_in_ws = zeros(shape=[data_in_1d.shape[0], 3])
    data_in_ws[:, 0] = geox_in_1d
    data_in_ws[:, 1] = geoy_in_1d
    data_in_ws[:, 2] = data_in_1d

    # Create csv file
    make_folder(os.path.split(file_name_csv)[0])
    create_point_csv(file_name_csv, data_in_ws, var_name_data, var_name_geox, var_name_geoy)

    # Create vrt file
    make_folder(os.path.split(file_name_vrt)[0])
    create_point_vrt(file_name_vrt, file_name_csv, var_name_layer, var_name_data, var_name_geox, var_name_geoy)

    # Grid option(s)
    if interp_method == 'nearest':
        if interp_option is None:
            interp_option = ('-a nearest:radius1=' + str(interp_radius_x) + ':radius2=' +
                             str(interp_radius_y) + ':angle=0.0:nodata=' + str(interp_no_data))
    elif interp_method == 'idw':
        if interp_option is None:
            interp_option = ('-a invdist:power=2.0:smoothing=0.0:radius1=' + str(interp_radius_x) + ':radius2=' +
                             str(interp_radius_y) + ':angle=0.0:nodata=' + str(interp_no_data))
    else:
        interp_option = None

    # Execute line command definition (using gdal_grid)
    line_command = ('gdal_grid -zfield "' + var_name_data + '"  -txe ' +
                    str(geox_out_min) + ' ' + str(geox_out_max) + ' -tye ' +
                    str(geoy_out_min) + ' ' + str(geoy_out_max) + ' -a_srs EPSG:' + epsg_code + ' ' +
                    interp_option + ' -outsize ' + str(geo_out_rows) + ' ' + str(geo_out_cols) +
                    ' -of GTiff -ot Float32 -l ' + var_name_layer + ' ' +
                    file_name_vrt + ' ' + file_name_tiff + ' --config GDAL_NUM_THREADS ALL_CPUS')
    '''
    ERRORS LIKE:
    
    ERROR 1: PROJ: proj_create_from_database: SQLite error on SELECT name, coordinate_system_auth_name, 
        coordinate_system_code, geodetic_crs_auth_name, geodetic_crs_code, conversion_auth_name, conversion_code, 
        area_of_use_auth_name, area_of_use_code, text_definition, deprecated FROM projected_crs 
        WHERE auth_name = ? AND code = ?: no such column: area_of_use_auth_name
    ERROR 1: Failed to process SRS definition: EPSG:32643,WGS84/UTM zone 43N
    
    Explanation here:
    https://gis.stackexchange.com/questions/411287/python-gdal-grid-error-in-epsg
    
    In PyCharm add in sh launcher the PATH and LD_LIBRARY_PATH as defined in .bashrc to have the same libraries
    loaded in the environment. Try with os.system(line_command) and then use exec_process if all is working
    '''
    # os.system(line_command)

    # Execute algorithm
    [std_out, std_err, std_exit] = exec_process(command_line=line_command, command_path=folder_tmp)

    # Read data in tiff format and get values
    data_out_obj = rasterio.open(file_name_tiff)
    data_out_3d = data_out_obj.read()

    # Image postprocessing to obtain 2d, south-north, east-west data
    data_out_2d = data_out_3d[0, :, :]
    data_out_2d = flipud(data_out_2d)

    # Delete tmp file(s)
    if os.path.exists(file_name_csv):
        os.remove(file_name_csv)
    if os.path.exists(file_name_vrt):
        os.remove(file_name_vrt)
    if os.path.exists(file_name_tiff):
        os.remove(file_name_tiff)

    return data_out_2d
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to create csv ancillary file
def create_point_csv(file_name_csv, var_data, var_name_data='values', var_name_geox='x', var_name_geoy='y',
                     file_format='%10.4f', file_delimiter=','):

    with open(file_name_csv, 'w') as file_handle:
        file_handle.write(var_name_geox + ',' + var_name_geoy + ',' + var_name_data + '\n')
        savetxt(file_handle, var_data, fmt=file_format, delimiter=file_delimiter, newline='\n')
        file_handle.close()
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to create vrt ancillary file
def create_point_vrt(file_name_vrt, file_name_csv, var_name_layer,
                     var_name_data='values', var_name_geox='x', var_name_geoy='y'):

    with open(file_name_vrt, 'w') as file_handle:
        file_handle.write('<OGRVRTDataSource>\n')
        file_handle.write('    <OGRVRTLayer name="' + var_name_layer + '">\n')
        file_handle.write('        <SrcDataSource>' + file_name_csv + '</SrcDataSource>\n')
        file_handle.write('    <GeometryType>wkbPoint</GeometryType>\n')
        file_handle.write('    <LayerSRS>WGS84</LayerSRS>\n')
        file_handle.write(
            '    <GeometryField encoding="PointFromColumns" x="' +
            var_name_geox + '" y="' + var_name_geoy + '" z="' + var_name_data + '"/>\n')
        file_handle.write('    </OGRVRTLayer>\n')
        file_handle.write('</OGRVRTDataSource>\n')
        file_handle.close()

# -------------------------------------------------------------------------------------

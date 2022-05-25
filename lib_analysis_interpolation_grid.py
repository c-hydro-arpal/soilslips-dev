"""
Library Features:

Name:          lib_analysis_interpolation_grid
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20200515'
Version:       '1.0.0'
"""

#######################################################################################
# Library
import logging
import numpy as np
from scipy.interpolate import griddata

from lib_info_args import logger_name_scenarios as logger_name

# Logging
log_stream = logging.getLogger(logger_name)

# Debug
import matplotlib.pylab as plt
#######################################################################################


# -------------------------------------------------------------------------------------
# Method to interpolate grid index to a reference dataset
def interp_grid2index(lons_in, lats_in, lons_out, lats_out, nodata=-9999, interp_method='nearest'):

    if lons_in.shape.__len__() == 1 and lats_in.shape.__len__() == 1:
        shape_in = lons_in.shape[0] * lats_in.shape[0]
        lons_in_2d, lats_in_2d = np.meshgrid(lons_in, lats_in)
    elif lons_in.shape.__len__() == 2 and lats_in.shape.__len__() == 2:
        shape_in = lons_in.shape[0] * lats_in.shape[1]
        lons_in_2d = lons_in
        lats_in_2d = lats_in
    else:
        log_stream.error(' ===> Geographical datasets input dimensions in bad format')
        raise IOError('Geographical data format not allowed')

    if lons_out.shape.__len__() == 1 and lats_out.shape.__len__() == 1:
        lons_out_2d, lats_out_2d = np.meshgrid(lons_out, lats_out)
    elif lons_out.shape.__len__() == 2 and lats_out.shape.__len__() == 2:
        lons_out_2d = lons_out
        lats_out_2d = lats_out
    else:
        log_stream.error(' ===> Geographical datasets output dimensions in bad format')
        raise IOError('Geographical data format not allowed')

    index_in = np.arange(0, shape_in)
    index_out = griddata((lons_in_2d.ravel(), lats_in_2d.ravel()), index_in,
                         (lons_out_2d.ravel(), lats_out_2d.ravel()), method=interp_method, fill_value=nodata)

    # index_tmp = np.reshape(index_out, [lons_out_2d.shape[0], lats_out_2d.shape[1]])

    # Debug
    # plt.figure()
    # plt.imshow(index_tmp)
    # plt.colorbar()
    # plt.show()

    return index_out

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to interpolate grid data to a reference dataset
def interp_grid2map(lons_in, lats_in, values_in, lons_out, lats_out, nodata=-9999, interp_method='nearest',
                    index_out=None):

    if index_out is None:
        values_tmp = griddata((lons_in.ravel(), lats_in.ravel()), values_in.ravel(),
                              (lons_out.ravel(), lats_out.ravel()), method=interp_method,
                              fill_value=nodata)
        values_out = np.reshape(values_tmp, [lons_out.shape[0], lats_out.shape[1]])
    else:
        values_tmp = values_in.ravel()[index_out]
        values_out = np.reshape(values_tmp, [lons_out.shape[0], lats_out.shape[1]])

    return values_out
# -------------------------------------------------------------------------------------

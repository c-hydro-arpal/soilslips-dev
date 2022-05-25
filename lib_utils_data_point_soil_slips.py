"""
Library Features:

Name:          lib_utils_data_point_soil_slips
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20220320'
Version:       '1.0.0'
"""

#######################################################################################
# Libraries
import logging
import os
import pandas as pd
import numpy as np

from pandas.tseries import offsets

from lib_data_io_shp import read_file_shp

from lib_info_args import logger_name_scenarios as logger_name

# Logging
log_stream = logging.getLogger(logger_name)
#######################################################################################


# -------------------------------------------------------------------------------------
# Read point soil slips
def read_point_file(file_name):

    if os.path.exists(file_name):
        point_dframe, point_collections, point_geoms = read_file_shp(file_name)
    else:
        log_stream.error(' ===> Soil slips database file "' + file_name + '" is not available')
        raise IOError('File not found!')

    return point_dframe

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to join point and grid
def collect_point_data(point_dframe_src, point_group_obj, point_time_format='%Y-%m-%d',
                       point_dframe_alert_area_tag='ZONA_ALLER', point_dframe_time_tag='DATA',
                       point_group_name_tag_src='name', point_group_threshold_tag_src='warning_threshold',
                       point_group_index_tag_src='warning_index', point_group_feature_tag_src=None,
                       point_group_n_tag_dst='event_n', point_group_name_tag_dst=None,
                       point_group_threshold_tag_dst='event_threshold', point_group_index_tag_dst='event_index',
                       point_group_feature_tag_dst='event_feature'):

    points_collections = {}
    for group_key, group_data in point_group_obj.items():

        group_selection = group_data[point_group_name_tag_src]
        group_threshold = group_data[point_group_threshold_tag_src]
        group_index = group_data[point_group_index_tag_src]

        point_selection = point_dframe_src.loc[point_dframe_src[point_dframe_alert_area_tag] == group_selection]
        # geo_point_selection = geo_point_selection.reset_index()
        # geo_point_selection = geo_point_selection.set_index(self.column_db_tag_time)

        time_point_selection = pd.DatetimeIndex(
            point_selection[point_dframe_time_tag].values).unique().sort_values()

        point_list_n, point_list_feature, point_list_threshold, point_list_index = [], [], [], []
        for time_point_step in time_point_selection:
            time_str_step = time_point_step.strftime(point_time_format)

            point_step = point_selection.loc[point_selection[point_dframe_time_tag] == time_str_step]
            point_threshold = find_point_category(point_step.shape[0], group_threshold)
            point_index = find_point_value(point_threshold, group_index)

            point_list_n.append(point_step.shape[0])
            point_list_feature.append(point_step)
            point_list_threshold.append(point_threshold)
            point_list_index.append(point_index)

        point_data = {point_group_n_tag_dst: point_list_n, point_group_threshold_tag_dst: point_list_threshold,
                      point_group_index_tag_dst: point_list_index,
                      point_group_feature_tag_dst: point_list_feature}

        point_dframe_dst = pd.DataFrame(point_data, index=time_point_selection)

        points_collections[group_key] = {}
        points_collections[group_key] = point_dframe_dst

    return points_collections
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to select point data
def select_point_by_time(time_step, point_dframe=None, time_format='%Y-%m-%d 00:00:00'):

    if point_dframe is not None:

        point_dframe_time_from = point_dframe.index[0]
        point_dframe_time_to = point_dframe.index[-1]

        if time_step in list(point_dframe.index):
            point_dframe_by_time = point_dframe.loc[time_step.strftime(time_format)]
        else:
            point_dframe_by_time = None
    else:
        log_stream.warning(' ===> Soil slips dataframe is defined by NoneType')
        point_dframe_by_time, point_dframe_time_from, point_dframe_time_to = None, None, None

    return point_dframe_by_time, point_dframe_time_from, point_dframe_time_to
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to set time range
def set_point_time_range(point_dframe, time_columns='time', time_frequency='D', time_format='%Y-%m-%d'):

    time_db = pd.DatetimeIndex(point_dframe[time_columns].values).unique().sort_values()

    time_start = time_db[0] - offsets.YearBegin()
    time_end = time_db[-1] + offsets.YearEnd()

    time_range = pd.date_range(start=time_start, end=time_end, freq=time_frequency)
    time_range = pd.DatetimeIndex(time_range.format(formatter=lambda x: x.strftime(time_format)))

    return time_range
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to find point value
def find_point_value(category, value):
    if category in list(value.keys()):
        val = value[category]
    else:
        val = np.nan
    return val
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to find point category
def find_point_category(value, category):
    for cat_key, cat_limits in category.items():
        cat_min = cat_limits[0]
        cat_max = cat_limits[1]
        if (cat_min is not None) and (cat_max is not None):
            if (value >= cat_min) and (value <= cat_max):
                break
        elif cat_min and cat_max is None:
            break
    return cat_key
# -------------------------------------------------------------------------------------

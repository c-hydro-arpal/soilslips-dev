"""
Class Features

Name:          driver_data_io_geo_point_soil_slips
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20200515'
Version:       '1.0.0'
"""

######################################################################################
# Library
import logging
import os

from lib_data_io_pickle import read_obj, write_obj
from lib_utils_system import make_folder

from lib_utils_data_point_soil_slips import read_point_file, collect_point_data

from lib_info_args import logger_name_scenarios as logger_name

# Logging
log_stream = logging.getLogger(logger_name)

# Debug
# import matplotlib.pylab as plt
######################################################################################


# -------------------------------------------------------------------------------------
# Class DriverGeo
class DriverGeoPoint:

    # -------------------------------------------------------------------------------------
    # Initialize class
    def __init__(self, src_dict, dst_dict=None,
                 collections_data_group=None,
                 flag_point_data_src='soil_slips', flag_point_data_dst='soil_slips',
                 flag_geo_updating=True):

        self.flag_point_data_src = flag_point_data_src
        self.flag_point_data_dst = flag_point_data_dst

        self.file_name_tag = 'file_name'
        self.folder_name_tag = 'folder_name'

        self.point_db_data_tag = 'database_data'

        self.structure_group_tag_name_src = 'name'
        self.structure_group_tag_threshold_src = 'warning_threshold'
        self.structure_group_tag_index_src = 'warning_index'
        self.structure_group_tag_features_src = None
        self.structure_group_tag_name_dst = None
        self.structure_group_tag_threshold_dst = 'event_threshold'
        self.structure_group_tag_index_dst = 'event_index'
        self.structure_group_tag_features_dst = 'event_features'

        self.column_db_tag_alert_area = 'ZONA_ALLER'
        self.column_db_tag_time = 'DATA'

        self.group_data = collections_data_group

        self.flag_geo_updating = flag_geo_updating

        self.file_name_src = src_dict[self.flag_point_data_src][self.point_db_data_tag][self.file_name_tag]
        self.folder_name_src = src_dict[self.flag_point_data_src][self.point_db_data_tag][self.folder_name_tag]
        self.file_path_src = os.path.join(self.folder_name_src, self.file_name_src)

        self.file_name_dst = dst_dict[self.flag_point_data_dst][self.point_db_data_tag][self.file_name_tag]
        self.folder_name_dst = dst_dict[self.flag_point_data_dst][self.point_db_data_tag][self.folder_name_tag]
        self.file_path_dst = os.path.join(self.folder_name_dst, self.file_name_dst)

        self.time_format = '%Y-%m-%d'

    # -------------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------------
    # Method to organize data
    def organize_data(self):

        # Starting info
        log_stream.info(' ----> Organize soil slips point information ... ')

        group_data = self.group_data

        file_path_src = self.file_path_src
        file_path_dst = self.file_path_dst

        if self.flag_geo_updating:
            if os.path.exists(file_path_dst):
                os.remove(file_path_dst)

        log_stream.info(' -----> Define registry points data ... ')
        if not os.path.exists(file_path_dst):

            obj_point_registry = read_point_file(file_path_src)
            obj_point_collection = collect_point_data(
                obj_point_registry, group_data,
                point_time_format=self.time_format,
                point_dframe_alert_area_tag=self.column_db_tag_alert_area,
                point_dframe_time_tag=self.column_db_tag_time,
                point_group_name_tag_src=self.structure_group_tag_name_src,
                point_group_threshold_tag_src=self.structure_group_tag_threshold_src,
                point_group_index_tag_src=self.structure_group_tag_index_src,
                point_group_feature_tag_src=self.structure_group_tag_name_src,
                point_group_name_tag_dst=self.structure_group_tag_name_dst,
                point_group_threshold_tag_dst=self.structure_group_tag_threshold_dst,
                point_group_index_tag_dst=self.structure_group_tag_index_dst,
                point_group_feature_tag_dst=self.structure_group_tag_name_dst,
            )

            folder_name_dst, file_name_dst = os.path.split(file_path_dst)
            make_folder(folder_name_dst)
            write_obj(file_path_dst, obj_point_collection)

            log_stream.info(' -----> Define registry points data ... DONE')
        else:

            # Read soil slips collections from disk
            obj_point_collection = read_obj(file_path_dst)
            log_stream.info(' -----> Define registry points data ... SKIPPED. Datasets was previously computed.')

        log_stream.info(' ----> Organize soil slips point information ... DONE')

        return obj_point_collection

# -------------------------------------------------------------------------------------

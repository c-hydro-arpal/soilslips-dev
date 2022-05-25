"""
Library Features:

Name:          lib_utils_time
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20220320'
Version:       '1.0.0'
"""

# -------------------------------------------------------------------------------------
# Libraries
import logging
import re
import pandas as pd

from datetime import date

from lib_info_args import logger_name_scenarios
from lib_info_args import logger_name_predictors
from lib_utils_logging import LogDecorator

from lib_utils_system import get_dict_nested_value

# Logging
log_stream = logging.getLogger()
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to decorate the logger_name of the time fx
@LogDecorator(logger_name=logger_name_scenarios)
def set_time_scenarios(**kwargs):
    return set_time(**kwargs)


@LogDecorator(logger_name=logger_name_predictors)
def set_time_predictors(**kwargs):
    return set_time(**kwargs)
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to set time run
def set_time(time_run_args=None, time_run_file=None, time_format='%Y-%m-%d %H:$M',
             time_run_file_start=None, time_run_file_end=None,
             time_period=1, time_frequency='H', time_rounding='H', time_reverse=True):

    log_stream.info(' ----> Set time period ... ')
    if (time_run_file_start is None) and (time_run_file_end is None):

        log_stream.info(' -----> Time info defined by "time_run" argument ... ')

        if time_run_args is not None:
            time_run = time_run_args
            log_stream.info(' ------> Time ' + time_run + ' set by argument')
        elif (time_run_args is None) and (time_run_file is not None):
            time_run = time_run_file
            logging.info(' ------> Time ' + time_run + ' set by user')
        elif (time_run_args is None) and (time_run_file is None):
            time_now = date.today()
            time_run = time_now.strftime(time_format)
            log_stream.info(' ------> Time ' + time_run + ' set by system')
        else:
            log_stream.info(' ----> Set time period ... FAILED')
            log_stream.error(' ===> Argument "time_run" is not correctly set')
            raise IOError('Time type or format is wrong')

        time_tmp = pd.Timestamp(time_run)
        time_run = time_tmp.floor(time_rounding)

        if time_period > 0:
            time_range = pd.date_range(end=time_run, periods=time_period, freq=time_frequency)
        else:
            log_stream.warning(' ===> TimePeriod must be greater then 0. TimePeriod is set automatically to 1')
            time_range = pd.DatetimeIndex([time_now], freq=time_frequency)

        logging.info(' -----> Time info defined by "time_run" argument ... DONE')

    elif (time_run_file_start is not None) and (time_run_file_end is not None):

        log_stream.info(' -----> Time info defined by "time_start" and "time_end" arguments ... ')

        time_run_file_start = pd.Timestamp(time_run_file_start)
        time_run_file_start = time_run_file_start.floor(time_rounding)
        time_run_file_end = pd.Timestamp(time_run_file_end)
        time_run_file_end = time_run_file_end.floor(time_rounding)

        if time_run_file_start > time_run_file_end:
            log_stream.error(' ===> Variable "time_start" is greater than "time_end". Check your settings file.')
            raise RuntimeError('Time_Range is not correctly defined.')

        time_now = date.today()
        time_run = time_now.strftime(time_format)
        time_run = pd.Timestamp(time_run)
        time_run = time_run.floor(time_rounding)
        time_range = pd.date_range(start=time_run_file_start, end=time_run_file_end, freq=time_frequency)

        log_stream.info(' -----> Time info defined by "time_start" and "time_end" arguments ... DONE')

    else:
        log_stream.info(' ----> Set time period ... FAILED')
        log_stream.error(' ===> Arguments "time_start" and/or "time_end" is/are not correctly set')
        raise IOError('Time type or format is wrong')

    if time_reverse:
        time_range = time_range[::-1]

    log_stream.info(' ----> Set time period ... DONE')

    return [time_run, time_range]

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to verify time window
def verify_time_window(time_reference, time_period, time_step=1):

    if not isinstance(time_period, pd.DatetimeIndex):
        time_period = pd.DatetimeIndex(time_period)

    if time_reference in time_period:
        idx_start = time_period.get_loc(time_reference)
    else:
        idx_start = None

    idx_end = None
    if idx_start is not None:
        idx_end = idx_start + time_step - 1

    flag_temporal_window = False
    if (idx_start is not None) and (idx_end is not None):
        if time_period.shape[0] > idx_end:
            flag_temporal_window = True

    if not flag_temporal_window:
        log_stream.warning(' ===> Temporal window do not include all the needed step for computing variable')
        log_stream.warning(' ===> Due to this issue of the time period, the variable will be not plotted.')

    return flag_temporal_window

# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to split time window
def split_time_window(time_window):
    time_period = re.findall(r'\d+', time_window)
    if time_period.__len__() > 0:
        time_period = int(time_period[0])
    else:
        time_period = 1
    time_frequency = re.findall("[a-zA-Z]+", time_window)[0]

    return time_period, time_frequency
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to find time maximum delta
def find_time_maximum_delta(time_delta_list):
    delta_string_max = None
    delta_seconds_max = 0
    for delta_string_step in time_delta_list:
        delta_seconds_step = pd.to_timedelta(delta_string_step).total_seconds()
        if delta_seconds_step > delta_seconds_max:
            delta_seconds_max = delta_seconds_step
            delta_string_max = delta_string_step

    return delta_string_max
# -------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------
# Method to search time features
def search_time_features(data_structure, data_key='rain_datasets', data_search_type='max'):

    search_period_selected, search_frequency_selected, search_type_selected = None, None, None
    if (data_key is not None) and (isinstance(data_key, str)):
        search_period_list, search_type_list = [], []
        for group_name, group_fields in data_structure.items():
            period_tmp = get_dict_nested_value(group_fields, [data_key, "search_period"])
            type_tmp = get_dict_nested_value(group_fields, [data_key, "search_type"])
            search_period_list.extend(period_tmp)
            search_type_list.extend(type_tmp)
        search_period_list = list(set(search_period_list))
        search_type_list = list(set(search_type_list))

        if data_search_type == 'max':
            search_delta_selected = find_time_maximum_delta(search_period_list)
            search_period_selected, search_frequency_selected = split_time_window(search_delta_selected)
            if search_type_list.__len__() > 1:
                log_stream.error(' ===> Obj "search_type_list" is not unique.')
                raise NotImplementedError('Case not implemented yet')
            else:
                search_type_selected = search_type_list[0]
        else:
            log_stream.error(' ===> Search type "' + data_search_type + '" is not supported')
            raise NotImplementedError('Case not implemented yet')
    else:
        log_stream.warning(' ===> Search time features are defined by NoneType ')

    return search_period_selected, search_frequency_selected, search_type_selected
# -------------------------------------------------------------------------------------

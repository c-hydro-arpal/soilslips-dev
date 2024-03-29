"""
Library Features:

Name:          lib_data_io_tiff
Author(s):     Fabio Delogu (fabio.delogu@cimafoundation.org)
Date:          '20240116'
Version:       '1.0.0'
"""

# ----------------------------------------------------------------------------------------------------------------------
# libraries
import logging
import rasterio
import gdal
import osr

from rasterio.transform import Affine
from osgeo import ogr, gdal, gdalconst

from lib_data_io_shp import convert_shp_2_tiff
from lib_info_args import proj_wkt as proj_default_wkt
from lib_info_args import logger_name

# logging
logging.getLogger('rasterio').setLevel(logging.WARNING)
log_stream = logging.getLogger(logger_name)

# Debug
# import matplotlib.pylab as plt
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to write file tiff
def write_file_tiff(file_name, file_data, file_wide, file_high, file_geotrans, file_proj,
                    file_metadata=None, file_format=gdalconst.GDT_Float32):

    if not isinstance(file_data, list):
        file_data = [file_data]

    if file_metadata is None:
        file_metadata = {'description_field': 'data'}
    if not isinstance(file_metadata, list):
        file_metadata = [file_metadata] * file_data.__len__()

    if isinstance(file_geotrans, Affine):
        file_geotrans = file_geotrans.to_gdal()

    file_n = file_data.__len__()
    dset_handle = gdal.GetDriverByName('GTiff').Create(file_name, file_wide, file_high, file_n, file_format,
                                                       options=['COMPRESS=DEFLATE'])
    dset_handle.SetGeoTransform(file_geotrans)
    dset_handle.SetProjection(file_proj)

    for file_id, (file_data_step, file_metadata_step) in enumerate(zip(file_data, file_metadata)):
        dset_handle.GetRasterBand(file_id + 1).WriteArray(file_data_step)
        dset_handle.GetRasterBand(file_id + 1).SetMetadata(file_metadata_step)
    del dset_handle
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Method to read file tiff
def read_file_tiff(file_name):

    file_handle = rasterio.open(file_name)
    file_proj = file_handle.crs.wkt
    file_geotrans = file_handle.transform

    file_tags = file_handle.tags()
    file_bands = file_handle.count
    file_metadata = file_handle.profile

    if file_bands == 1:
        file_data = file_handle.read(1)
    elif file_bands > 1:
        file_data = []
        for band_id in range(0, file_bands):
            file_data_tmp = file_handle.read(band_id + 1)
            file_data.append(file_data_tmp)
    else:
        log_stream.error(' ===> File multi-band are not supported')
        raise NotImplementedError('File multi-band not implemented yet')

    return file_data, file_proj, file_geotrans
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# Convert data to tiff
def convert_polygons_2_tiff(shape_polygon, shape_file, raster_file, template_file=None,
                            pixel_size=0.001, burn_value=1, epsg=4326):

    template_handle = rasterio.open(template_file)
    metadata = template_handle.meta.copy()
    metadata.update(compress='lzw')

    driver = ogr.GetDriverByName('Esri Shapefile')
    ds = driver.CreateDataSource(shape_file)

    if shape_polygon.type == 'MultiPolygon':
        layer = ds.CreateLayer('', None, ogr.wkbMultiPolygon)
    elif shape_polygon.type == 'Polygon':
        layer = ds.CreateLayer('', None, ogr.wkbPolygon)
    else:
        raise IOError('Shape type not implemented yet')
    defn = layer.GetLayerDefn()
    feat = ogr.Feature(defn)

    # Make a geometry, from Shapely object
    geom = ogr.CreateGeometryFromWkb(shape_polygon.wkb)
    feat.SetGeometry(geom)

    layer.CreateFeature(feat)
    feat = geom = None  # destroy these

    # Save and close everything
    ds = layer = feat = geom = None

    convert_shp_2_tiff(shape_file, raster_file,
                       pixel_size=pixel_size, burn_value=burn_value, epsg=epsg)

# ----------------------------------------------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
from osgeo import ogr
from osgeo import gdal
import shutil
try:
    shutil.rmtree('spx.gdb')
except:
    pass

gdal.SetConfigOption('FGDB_BULK_LOAD', 'YES')


# The spx for the first layer is a00000009.spx
#                 second         a0000000a.spx
#                 third          a0000000b.spx
# ...


ds = ogr.GetDriverByName('FileGDB').CreateDataSource('spx.gdb')
lyr = ds.CreateLayer('points', geom_type = ogr.wkbPoint)
for j in range(181):
    for i in range(361):
        feat = ogr.Feature(lyr.GetLayerDefn())
        geom = ogr.CreateGeometryFromWkt('POINT(%d %d)' % (i - 180, j - 90))
        feat.SetGeometry(geom)
        lyr.CreateFeature(feat)

lyr = ds.CreateLayer('points2', geom_type = ogr.wkbPoint)
for j in range(181):
    for i in range(361):
        feat = ogr.Feature(lyr.GetLayerDefn())
        geom = ogr.CreateGeometryFromWkt('POINT(%f %f)' % ((i - 180) / 10., (j - 90) / 10.))
        feat.SetGeometry(geom)
        lyr.CreateFeature(feat)

lyr = ds.CreateLayer('points3', geom_type = ogr.wkbPoint)
for j in range(20):
    for i in range(31):
        feat = ogr.Feature(lyr.GetLayerDefn())
        geom = ogr.CreateGeometryFromWkt('POINT(%d %d)' % (1 << i, 1 << i))
        feat.SetGeometry(geom)
        lyr.CreateFeature(feat)

def create_polygon(lyr,x,y,x2,y2):
    feat = ogr.Feature(lyr.GetLayerDefn())
    geom = ogr.CreateGeometryFromWkt('POLYGON((%f %f,%f %f,%f %f,%f %f,%f %f))' % (x,y,x,y2,x2,y2,x2,y,x,y))
    feat.SetGeometry(geom)
    lyr.CreateFeature(feat)

lyr = ds.CreateLayer('polygons', geom_type = ogr.wkbPolygon)
for j in range(180):
    for i in range(360):
        x = i - 180
        y = j - 90
        x2 = x + 1
        y2 = y + 1
        create_polygon(lyr,x,y,x2,y2)

def create_polygon_recurse(lyr,x,y,x2,y2,min_size):
    if x2 - x < min_size or y2 - y < min_size:
        return
    create_polygon(lyr,x,y,x2,y2)
    xmid = (x + x2) / 2.0
    ymid = (y + y2) / 2.0
    create_polygon_recurse(lyr,x,y,xmid,ymid,min_size)
    create_polygon_recurse(lyr,x,ymid,xmid,y2,min_size)
    create_polygon_recurse(lyr,xmid,y,x2,ymid,min_size)
    create_polygon_recurse(lyr,xmid,ymid,x2,y2,min_size)

lyr = ds.CreateLayer('polygons2', geom_type = ogr.wkbPolygon)
create_polygon_recurse(lyr,-1000000,-1000000,1000000,1000000, 10000)

lyr = ds.CreateLayer('polygons3', geom_type = ogr.wkbPolygon)
create_polygon_recurse(lyr,-10000,-10000,10000,10000,100)

lyr = ds.CreateLayer('polygons4', geom_type = ogr.wkbPolygon)
create_polygon_recurse(lyr,-100,-100,100,100,1)

lyr = ds.CreateLayer('polygons5', geom_type = ogr.wkbPolygon)
for i in range(100):
    create_polygon(lyr,-1000000,-1000000,1000000,1000000)
    create_polygon(lyr,-100000,-100000,100000,100000)
    create_polygon(lyr,-10000,-10000,10000,10000)
    create_polygon(lyr,-1000,-1000,1000,1000)
    create_polygon(lyr,-100,-100,100,100)
    create_polygon(lyr,-10,-10,10,10)


ds = None

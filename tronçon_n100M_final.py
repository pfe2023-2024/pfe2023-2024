import arcpy # type: ignore
import geopandas as gpd
from shapely.geometry import MultiLineString, MultiPoint, Point, Polygon, LineString
import pandas as pd
import numpy as np

def convert_feature_to_geodataframe(layer_path):
    fr_fields = [field.name for field in arcpy.ListFields(layer_path)]
    fr_fields.append('SHAPE@')
    fr_data = []
    with arcpy.da.SearchCursor(layer_path, fr_fields) as cursor:
        for row in cursor:
            fr = row[-1]
            attributes = {field: value for field, value in zip(fr_fields[:-1], row[:-1])}
            attributes['geometry'] = fr
            fr_data.append(attributes)
    gdf = gpd.GeoDataFrame(fr_data)
    return gdf

###############les fonctions#############################
#filtered function
def filter_dataframe(Accidents_routiers, field1=None, field2=None, cond1=None, cond2=None, cond3=None):
    if field1 is None:
        filtered_data = Accidents_routiers[Accidents_routiers[field2] >= cond2]
    elif field1 is not None and field2 is not None:
        filtered_data = Accidents_routiers[Accidents_routiers[field1] != cond1]
        filtered_data = filtered_data[filtered_data[field2] >= cond2]
        filtered_data = filtered_data[filtered_data[field2] <= cond3]
    else:
        pass
    return filtered_data

#projected function
def project_points_on_lines(accidents, routes):
    shply_line = routes.geometry.unary_union
    for i in range(len(accidents)):
        shply_line.interpolate(shply_line.project(accidents.geometry[i])).wkt
    result = accidents.copy()
    result['geometry'] = result.apply(lambda row: shply_line.interpolate(shply_line.project(row.geometry)), axis=1)
    return result

#buffer function
def create_buffer(accidents_projected, buffer_distance, BUFFER_ID=None, ID=None):
    if BUFFER_ID is None and ID is None:
        df_buffer = accidents_projected.geometry.buffer(buffer_distance)
        buffered_df = gpd.GeoDataFrame(geometry=df_buffer, crs=accidents_projected.crs)
    else:
        df_buffer = accidents_projected.geometry.buffer(buffer_distance)
        buffered_df = gpd.GeoDataFrame(geometry=df_buffer, crs=accidents_projected.crs)
        buffered_df[BUFFER_ID] = accidents_projected[ID]
    return buffered_df

def find_intersections(gdf1, gdf2):
    intersection_result = gpd.sjoin(gdf2, gdf1, how="inner", op="intersects")
    return intersection_result

#dissolve function
def dissolve_by_id(gdf):
    dissolved = gdf.dissolve(by='BUFFER_ID', aggfunc={"BUFFER_ID": "count"})
    dissolved = dissolved.rename(columns={'BUFFER_ID': 'count'})
    return dissolved

#feature_to_point function
def convert_to_points(gdf):
    points = gdf.copy()
    points.geometry = points.geometry.centroid
    return points

#clipped function
def clip_features(input_feats, clip_feats, xy_tolerance=None):
    clipped = gpd.clip(input_feats, clip_feats, xy_tolerance)
    for cln in clipped.columns:
        print(clipped.dtypes[cln])
        if clipped.dtypes[cln] == tuple:
            clipped[cln] = clipped[cln].astype(str)
        print(clipped.dtypes[cln])
    return clipped.explode(index_parts=True)

#function Point_noir_Mileu
def create_midpoints(lines):
    points_gdf = lines.interpolate(distance=0.5, normalized=True)
    return points_gdf


# Charger les données
#layer input
accident_layer = arcpy.GetParameterAsText(0)
route_layer = arcpy.GetParameterAsText(1)
out_layer = arcpy.GetParameterAsText(2)
#field & condition input
p1 = arcpy.GetParameterAsText(3)
p2 = arcpy.GetParameterAsText(4)
c1 = arcpy.GetParameterAsText(5)
c2 = arcpy.GetParameterAsText(6)
c3 = arcpy.GetParameterAsText(7)
p3 = arcpy.GetParameterAsText(8)

#feature to gdf
Accidents_routiers = convert_feature_to_geodataframe(accident_layer)
routes = convert_feature_to_geodataframe(route_layer)
# appel functions
selected_accidents = filter_dataframe(Accidents_routiers, field1=p1, field2=p2, cond1=c1, cond2=c2, cond3=c3)
projected_accidents = project_points_on_lines(Accidents_routiers, routes)
buffer_zones = create_buffer(projected_accidents, 50, 'BUFFER_ID', p3)
intersections = find_intersections(buffer_zones, projected_accidents)
dissolved = dissolve_by_id(intersections)
selected_dissolved = filter_dataframe(dissolved, field1=None, field2='count', cond1=None, cond2=3)
points_with_3_or_more_accidents = convert_to_points(selected_dissolved)
buffer_zones_2 = create_buffer(points_with_3_or_more_accidents, 50, BUFFER_ID=None, ID=None)
clipped_routes = clip_features(routes, buffer_zones_2, xy_tolerance=None)
midpoints = create_midpoints(clipped_routes)

arcpy.AddMessage(clipped_routes)
arcpy.AddMessage(midpoints)

clipped_routes.to_file(out_layer)
#midpoints.to_file("result.gpkg", layer='PMN')
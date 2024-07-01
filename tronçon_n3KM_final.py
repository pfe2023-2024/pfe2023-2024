import arcpy # type: ignore
import geopandas as gpd
from shapely.geometry import Point, LineString 
from shapely.ops import split , snap , linemerge


###############les fonction#############################


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
# filtrer les données
def filter_data(dataframe, field1=None, field2=None, condition1=None, condition2=None, condition3=None):
    if field1 is None:
        filtered_data = dataframe[dataframe[field2] >= condition2]
    elif field1 is not None and field2 is not None:
        filtered_data = dataframe[dataframe[field1] != condition1]
        filtered_data = filtered_data[filtered_data[field2] >= condition2]
        filtered_data = filtered_data[filtered_data[field2] <= condition3]
    else:
        pass
    return filtered_data

# projeter les points
def project_points_onto_line(points, lines):
    unified_line = lines.geometry.unary_union
    result = points.copy()
    result['geometry'] = result.apply(lambda row: unified_line.interpolate(unified_line.project(row.geometry)), axis=1)
    return result

# ajouter XY
def add_xy_coordinates(dataframe):
    dataframe = dataframe.copy()
    dataframe['X'] = dataframe.geometry.x
    dataframe['Y'] = dataframe.geometry.y
    return dataframe

# fussioner a partir X Y
def dissolve_and_count_points(dataframe, x_col='X', y_col='Y'):
    # Count the number of points at each location
    count_df = dataframe.groupby([x_col, y_col]).size().reset_index(name='count')
    
    # Dissolve the dataframe
    dissolved = dataframe.dissolve(by=[x_col, y_col], aggfunc='first').reset_index()
    
    # Merge the count with the dissolved data
    dissolved = dissolved.merge(count_df, on=[x_col, y_col])
    
    return dissolved
# split line at point
def find_insert_position(line, point):
    min_distance = float('inf')
    insert_position = 0
    coords = list(line.coords)
    
    for i in range(len(coords) - 1):
        segment = LineString([coords[i], coords[i + 1]])
        distance = segment.distance(point)
        
        if distance < min_distance:
            min_distance = distance
            insert_position = i + 1
            
    return insert_position

def insert_point_at_line(line_gdf, point_gdf, tolerance=0.001):
    new_lines = []
    for geom in line_gdf.geometry:
        if geom.geom_type == 'LineString':
            lines = [geom]
        elif geom.geom_type == 'MultiLineString':
            lines = list(geom.geoms)
        for line in lines:
            for point in point_gdf.geometry:
                if line.buffer(tolerance).intersection(point):
                    coords = list(line.coords)
                    insert_position = find_insert_position(line, point)
                    coords.insert(insert_position, (point.x, point.y))
                    line = LineString(coords)
            new_lines.append(line)
    result = gpd.GeoDataFrame(geometry=new_lines, crs=line_gdf.crs)
    return result
#fonction une
def split_line_at_nearest_points(gdf_line, gdf_points, tolerance=0.001):
    segments = []
    for geom in gdf_line.geometry:
        if geom.geom_type == 'LineString':
            lines = [geom]
        elif geom.geom_type == 'MultiLineString':
            lines = list(geom.geoms) 
        for line in lines:
            for point in gdf_points.geometry:
                if line.buffer(tolerance).intersection(point):
                    split_line = split(line, point)
                    segments.append(split_line.geoms[0])
                    if len(split_line.geoms) > 1:
                        line = split_line.geoms[1]
            segments.append(line)
    result = gpd.GeoDataFrame(geometry=segments, crs=gdf_line.crs)
    return result
#fonction deux
def split_line_by_nearest_points(gdf_line, gdf_points, tolerance):
    line = gdf_line.geometry.unary_union
    coords = gdf_points.geometry.unary_union
    split_line = split(line, snap(coords, line, tolerance))

    segments = [feature for feature in split_line.geoms]

    gdf_segments = gpd.GeoDataFrame(
        list(range(len(segments))), geometry=segments ,crs = gdf_line.crs)
    gdf_segments.columns = ['index', 'geometry']

    return gdf_segments
# ajouter la colonne distance
def calculate_segment_lengths(gdf):
    gdf['length'] = gdf.geometry.length
    return gdf

# clacule les intersections
def calculate_intersection(gdf1, gdf2):
    intersection_result = gpd.sjoin(gdf2, gdf1, how="inner", predicate="intersects")
    intersection_result['join_count'] = intersection_result.groupby(level=0).cumcount() + 1
    intersection_result = intersection_result.reset_index(drop=True)
    return intersection_result

# choisir les petits segment
def select_short_segments(gdf,field):
    short_segments = gdf[(gdf['length'] <= 3000) & (gdf[field] >= 2)]
    return short_segments
#############


# Fonction pour trouver les voisins et dissoudre les lignes
def dissolve_pairs_with_count(gdf):
    dissolved_lines = []
    used_indices = set()
    counts = []
    
    for i, line1 in gdf.iterrows():
        if i in used_indices:
            continue
        neighbors = gdf[~gdf.index.isin(used_indices) & (gdf.geometry.touches(line1.geometry))]
        if not neighbors.empty:
            line2 = neighbors.iloc[0]
            merged_line = linemerge([line1.geometry, line2.geometry])
            dissolved_lines.append(merged_line)
            counts.append(2)  # Deux lignes fusionnées
            used_indices.add(line2.name)
        else:
            dissolved_lines.append(line1.geometry)
            counts.append(1)  # Une seule ligne
        used_indices.add(i)
    
    # Création du nouveau GeoDataFrame avec la colonne de compte
    result_gdf = gpd.GeoDataFrame(geometry=dissolved_lines,crs=gdf.crs)
    result_gdf['count'] = counts
    return result_gdf

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

#feature to gdf
Accidents_routiers = convert_feature_to_geodataframe(accident_layer)
routes = convert_feature_to_geodataframe(route_layer)

# appeler les fonction
filtered_accidents = filter_data(Accidents_routiers, field1=p1, field2=p2, condition1=c1, condition2=c2, condition3=c3)
projected_accidents = project_points_onto_line(filtered_accidents, routes)
projected_acc = add_xy_coordinates(projected_accidents)
projected_acc_diss = dissolve_and_count_points(projected_acc, x_col='X', y_col='Y')
split_route = split_line_by_nearest_points(insert_point_at_line(routes.explode(index_parts=True), projected_acc_diss, tolerance=0.5), projected_acc_diss, tolerance=0.5)
split_route_len = calculate_segment_lengths(split_route)
intersect = calculate_intersection(projected_acc_diss, split_route_len)
selected_segments = select_short_segments(intersect,field='join_count')
dissolve_seg = dissolve_pairs_with_count(selected_segments)
dissolve_seg_len = calculate_segment_lengths(dissolve_seg)
tronçon_noirs3km = select_short_segments(dissolve_seg_len,field='count')
arcpy.AddMessage(tronçon_noirs3km)
tronçon_noirs3km.to_file(out_layer)
arcpy.AddMessage('ok')
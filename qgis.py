from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import (QgsProcessing,
                       QgsProcessingException,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterFeatureSink,
                       QgsFeatureSink,
                       QgsProcessingParameterString,
                       QgsProject,
                       QgsVectorLayer)
from qgis import processing
import geopandas as gpd
from shapely.geometry import Point, LineString, Polygon
class ExampleProcessingAlgorithm(QgsProcessingAlgorithm):
    INPUT_ACCIDENTS = 'INPUT_ACCIDENTS'
    INPUT_ROUTES = 'INPUT_ROUTES'
    OUTPUT = 'OUTPUT'
    
    FIELD1 = 'FIELD1'
    FIELD2 = 'FIELD2'
    CONDITION1 = 'CONDITION1'
    CONDITION2 = 'CONDITION2'
    CONDITION3 = 'CONDITION3'
    BUFFER_ID_FIELD = 'BUFFER_ID_FIELD'
    
    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ExampleProcessingAlgorithm()

    def name(self):
        return 'exampleprocessingalgorithm'

    def displayName(self):
        return self.tr('Example Processing Algorithm')

    def group(self):
        return self.tr('Example scripts')

    def groupId(self):
        return 'examplescripts'

    def shortHelpString(self):
        return self.tr("Example algorithm short description")

    def initAlgorithm(self, config=None):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_ACCIDENTS,
                self.tr('Input Accidents Layer'),
                [QgsProcessing.TypeVectorPoint]
            )
        )
        
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.INPUT_ROUTES,
                self.tr('Input Routes Layer'),
                [QgsProcessing.TypeVectorLine]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Output Layer')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.FIELD1,
                self.tr('Field 1')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.FIELD2,
                self.tr('Field 2')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.CONDITION1,
                self.tr('Condition 1')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.CONDITION2,
                self.tr('Condition 2')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.CONDITION3,
                self.tr('Condition 3')
            )
        )
        
        self.addParameter(
            QgsProcessingParameterString(
                self.BUFFER_ID_FIELD,
                self.tr('Buffer ID Field')
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        input_accidents = self.parameterAsSource(parameters, self.INPUT_ACCIDENTS, context)
        input_routes = self.parameterAsSource(parameters, self.INPUT_ROUTES, context)
        
        field1 = self.parameterAsString(parameters, self.FIELD1, context)
        field2 = self.parameterAsString(parameters, self.FIELD2, context)
        condition1 = self.parameterAsString(parameters, self.CONDITION1, context)
        condition2 = self.parameterAsString(parameters, self.CONDITION2, context)
        condition3 = self.parameterAsString(parameters, self.CONDITION3, context)
        buffer_id_field = self.parameterAsString(parameters, self.BUFFER_ID_FIELD, context)
        
        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            input_accidents.fields(),
            input_accidents.wkbType(),
            input_accidents.sourceCrs()
        )

        accidents_gdf = self.feature_to_geodataframe(input_accidents)
        routes_gdf = self.feature_to_geodataframe(input_routes)

        filtered_accidents = self.filter_data(accidents_gdf, field1=field1, field2=field2, cond1=condition1, cond2=condition2, cond3=condition3)
        projected_accidents = self.project_points_onto_line(filtered_accidents, routes_gdf)
        buffered_zones = self.create_buffer(projected_accidents, 1500, 'BUFFER_ID', buffer_id_field)
        intersections = self.intersect_geodataframes(buffered_zones, projected_accidents)
        dissolved_intersections = self.dissolve_geometries(intersections, 'BUFFER_ID', 'count_buff')
        filtered_dissolved = self.filter_data(dissolved_intersections, field2='count_buff', cond2=3)
        points_over_3_accidents = self.convert_to_centroids(filtered_dissolved)
        buffered_points = self.create_buffer(points_over_3_accidents, 1500)
        clipped_routes = self.clip_features(routes_gdf, buffered_points)
        final_intersections = self.intersect_geodataframes(filtered_dissolved, clipped_routes, how='left')
        final_dissolved = self.dissolve_geometries(final_intersections, 'name', 'count_r')
        final_filtered = self.filter_data(final_dissolved, field2='count_r', cond2=3)

        for feature in final_filtered.itertuples():
            sink.addFeature(feature)

        return {self.OUTPUT: dest_id}
    
    def feature_to_geodataframe(self, source):
        features = [feat for feat in source.getFeatures()]
        field_names = [field.name() for field in source.fields()]
        data = []
        
        for feat in features:
            geom = feat.geometry().asWkt()
            attrs = feat.attributes()
            row = {field: attrs[idx] for idx, field in enumerate(field_names)}
            row['geometry'] = geom
            data.append(row)
        
        gdf = gpd.GeoDataFrame(data)
        return gdf

    def filter_data(self, gdf, field1=None, field2=None, cond1=None, cond2=None, cond3=None):
        if field1 is None:
            filtered_data = gdf[gdf[field2] >= cond2]
        elif field1 is not None and field2 is not None:
            filtered_data = gdf[gdf[field1] != cond1]
            filtered_data = filtered_data[filtered_data[field2].apply(lambda x: x >= datetime.strptime(cond2, "%Y-%m-%d"))]
            filtered_data = filtered_data[filtered_data[field2].apply(lambda x: x <= datetime.strptime(cond3, "%Y-%m-%d"))]
        else:
            pass
        return filtered_data

    def project_points_onto_line(self, points, lines):
        unified_line = lines.geometry.unary_union
        result = points.copy()
        result['geometry'] = result.apply(lambda row: unified_line.interpolate(unified_line.project(row.geometry)), axis=1)
        return result

    def create_buffer(self, gdf, distance, buffer_id=None, id_field=None):
        buffered_geometries = gdf.geometry.buffer(distance)
        buffered_gdf = gpd.GeoDataFrame(geometry=buffered_geometries, crs=gdf.crs)
        if buffer_id is not None and id_field is not None:
            buffered_gdf[buffer_id] = gdf[id_field]
        return buffered_gdf

    def intersect_geodataframes(self, gdf1, gdf2, how="inner"):
        intersection_result = gpd.sjoin(gdf2, gdf1, how=how, op="intersects")
        return intersection_result

    def dissolve_geometries(self, gdf, by_field, new_field_name):
        dissolved = gdf.dissolve(by=by_field, aggfunc={by_field: 'count'})
        dissolved = dissolved.rename(columns={by_field: new_field_name})
        return dissolved

    def convert_to_centroids(self, gdf):
        centroids = gdf.copy()
        centroids.geometry = centroids.geometry.centroid
        return centroids

    def clip_features(self, input_gdf, clip_gdf, xy_tolerance=None):
        clipped = gpd.clip(input_gdf, clip_gdf, xy_tolerance)
        for column in clipped.columns:
            if clipped.dtypes[column] == tuple:
                clipped[column] = clipped[column].astype(str)
        return clipped.explode(index_parts=True)


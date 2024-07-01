DROP VIEW routes_merge cascade;
-----------------------les fonctions----------------------------------
CREATE OR REPLACE FUNCTION merged()
RETURNS void AS $$
BEGIN
    DROP VIEW IF EXISTS routes_merge;
    CREATE VIEW routes_merge AS
    SELECT ST_LineMerge(ST_Union(geom)) AS merged_line
	FROM route;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION filter_accidents_2021()
RETURNS void AS $$
BEGIN
    DROP VIEW IF EXISTS accidents_2021;
    CREATE VIEW accidents_2021 AS
    SELECT *
    FROM accidents
    WHERE "ACCIDENT_DATE" BETWEEN '2021-01-01' AND '2021-12-31'
    AND "TYPE_ACC_NEW" <> 'حادث مادي';
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION projeter()
RETURNS void AS $$
BEGIN
    DROP VIEW IF EXISTS acc_projeter;
    CREATE VIEW acc_projeter AS
    SELECT accidents_2021.*,
           ST_ClosestPoint(routes_merge.merged_line, accidents_2021.geom) AS closest_point
    FROM accidents_2021
    CROSS JOIN routes_merge;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION buffer()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS acc_projeter_buffer;
    CREATE VIEW acc_projeter_buffer AS
    SELECT ST_Buffer(acc_projeter.closest_point, 50) AS st_buffer
    FROM acc_projeter;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION intersects()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS accidents_inter_buffer;
    CREATE VIEW accidents_inter_buffer AS
    SELECT a.*
    FROM acc_projeter a
	JOIN acc_projeter_buffer b
	ON ST_Intersects(a.closest_point, b.st_buffer);
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION dissolve()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS dissolved_acc;
	CREATE VIEW dissolved_acc AS
	SELECT ID,
		   ST_Union(closest_point)AS dissolved_geom,
           COUNT(*) AS count
	FROM accidents_inter_buffer
	GROUP BY ID;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION filter_accidents_plus3()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS accidents_plus3;
    CREATE VIEW accidents_plus3 AS
    SELECT *
    FROM dissolved_acc
	WHERE dissolved_acc.count >=3;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION feature_to_point()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS FeatureToPoint;
    CREATE VIEW FeatureToPoint AS
    SELECT ST_Centroid(dissolved_geom) AS centroid_geom
    FROM accidents_plus3;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION accidents_buffer()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS buffer50;
    CREATE VIEW buffer50 AS
    SELECT *,
		   ST_Buffer(centroid_geom, 50) AS buffer_geom
    FROM FeatureToPoint;
END;
$$ LANGUAGE plpgsql;
----------------------------------------------------------------------
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION clip()
RETURNS void AS $$
BEGIN
	DROP VIEW IF EXISTS clipped_geom;
    CREATE VIEW clipped_geom AS
    SELECT ST_Intersection(routes_merge.merged_line, buffer50.buffer_geom) AS clipped_geom
	FROM routes_merge, buffer50
	WHERE ST_Intersects(routes_merge.merged_line, buffer50.buffer_geom);
END;
$$ LANGUAGE plpgsql;
-----------------------------------exécution les fonctions-----------------------------------
SELECT merged();
SELECT filter_accidents_2021();
SELECT projeter();
SELECT buffer();
SELECT intersects();
SELECT dissolve();
SELECT filter_accidents_plus3();
SELECT feature_to_point();
SELECT accidents_buffer();
SELECT clip();
----------------------------------------------------------------------
----------------------------------------------------------------------
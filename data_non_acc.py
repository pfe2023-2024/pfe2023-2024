import geopandas as gpd
import pandas as pd
import random
import datetime
from datetime import datetime
from datetime import datetime, timedelta

#read and drop
#df_non_acc = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/data_non_acc/data_non_acc.shp")
#df_com=gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/data_non_acc/com_setif.shp")
#df_non_acc.drop(['Join_Count','TARGET_FID','CID','route','Shape_Leng'], axis=1, inplace=True)
#df_com.drop(['OBJECTID_1','NATURE','AUTRE_NOM','NOM_WILAYA','WILAYA',
             #'ORIGINE','Code','Shape_Leng','Shape_Le_1','Shape_Area'], axis=1, inplace=True)
df_non_acc = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/data_non_acc/data.gpkg")

#fonction de sjoin
def join_geodata(data, commune_data):
    # Convert the non-spatial DataFrame to a GeoDataFrame
    data_geo = gpd.GeoDataFrame(data)
    # Select the relevant columns from the commune_data GeoDataFrame
    commune = commune_data[['COMMUNE', 'geometry']].to_crs(data_geo.crs)
    # Join the two GeoDataFrames using a spatial join
    joined_data = gpd.sjoin(data_geo, commune, how="inner", op="within")
    return joined_data

#fonction add data
def add_new_columns(df):
    df['type_acc'] = None
    df['nbre_dec'] = None
    df['nbre_bless'] = None
    #df['type_route'] = None
    df['etat_route'] = None
    df['meteo'] = None
    df['etat_chauss'] = None
    df['vision'] = None
    df['heure_acc'] = None
    df['cause_acc'] = None
    df['annee_permis'] = None
    df['niveau'] = None
    df['sit_fam'] = None
    df['cat_veh'] = None
    df['annee_veh'] = None
    df['Date_Acci'] = None
    df['Age'] = None
    df['Wilaya'] = None
    #df['geometry'] = None
    df['index_right'] = None
    #df['Commune'] = None
    df['Week_non_week'] = None
    df['date_naissance'] = None
    df['Population'] = None
    df['Area'] = None
    df['density_pop'] = None
    df['marque_veh'] = None
    df['Saison'] = None
    df['Periode_jour'] = None
    
    return df

def set_accident_columns(df):
    df['type_acc'] = 'non_acc'
    df['nbre_dec'] = '0'
    df['nbre_bless'] = '0'
    df['Wilaya'] = 'setif'
    df['cause_acc'] = 'setif'
    return df

def set_random_columns(df):
    # Set 'etat_route' column
    niveau_list = ['PM', 'NP', 'INF', 'MG']
    weights = [0.8, 0.1, 0.7, 0.3]
    for i in range(len(df)):
        df.loc[i, 'etat_route'] = random.choices(niveau_list, weights=weights)[0]

    # Set 'etat_chauss' column
    niveau_list = ['ENC', 'HM', 'GL']
    weights = [0.9, 0.7, 0.3]
    for i in range(len(df)):
        df.loc[i, 'etat_chauss'] = random.choices(niveau_list, weights=weights)[0]

    # Set 'vision' column
    niveau_list = ['B', 'M', 'F']
    weights = [0.8, 0.14, 0.06]
    for i in range(len(df)):
        df.loc[i, 'vision'] = random.choices(niveau_list, weights=weights)[0]

    # Set 'sit_fam' column
    niveau_list = ['MAR', 'CEL', 'SF', 'DIV']
    weights = [0.4, 0.2, 0.3, 0.1]
    for i in range(len(df)):
        df.loc[i, 'sit_fam'] = random.choices(niveau_list, weights=weights)[0]

    # Set 'Periode_jour' column
    niveau_list = ['PS', 'PMA', 'PM']
    weights = [0.57, 0.23, 0.2]
    for i in range(len(df)):
        df.loc[i, 'Periode_jour'] = random.choices(niveau_list, weights=weights)[0]

    # Set 'Saison' column
    niveau_list = ['E', 'P', 'A']
    weights = [0.34, 0.26, 0.4]
    for i in range(len(df)):
        df.loc[i, 'Saison'] = random.choices(niveau_list, weights=weights)[0]

    return df

def set_meteo_column(df):
    list_meteo =['C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'N', 'C', 'C', 'C', 'PL',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'PL', 'N', 'C', 'BR', 'N', 'N', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'LT', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'BR', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'N', 'C',
            'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'PL', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C',
            'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'C', 'N', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'PL',
            'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'SN', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C', 'PL', 'C', 'N', 'PL', 'C', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'PL', 'C', 'C', 'PL', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'N',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C', 'PL', 'BR', 'C', 'C', 'C', 'C', 'BR', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C',
            'C', 'C', 'N', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'SN', 'C', 'C', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'N', 'C', 'N', 'C',
            'C', 'N', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'SN', 'C', 'C', 'C', 'C', 'C', 'C', 'C',
            'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'BR', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'N', 'C', 'C', 'C',
            'C', 'C', 'N', 'C', 'C', 'N', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'PL', 'C', 'C', 'C', 'C','C', 'C', 'PL' ]
    df['meteo'] = list_meteo
    return df

def generate_random_time(num_rows):
    random_times = []
    for _ in range(num_rows):
        random_hour = random.randint(0, 23)
        random_minute = random.randint(0, 59)
        random_datetime = datetime(2023, 1, 1, random_hour, random_minute)  # Créer un objet datetime
        random_times.append(random_datetime.time())  # Extraire la partie heure
    return random_times 

def generate_random_time1(num_rows):
  # Define the time ranges and their probabilities
  time_ranges = {
      (8, 12): 0.22,
      (13, 20): 0.60,
      (20, 23): 0.18
  }

  # Generate a list of random times
  random_times = []
  for _ in range(num_rows):
    # Choose a random time range based on the probabilities
    random_range = random.choices(list(time_ranges.keys()), weights=list(time_ranges.values()))[0]

    # Generate a random time within the chosen range
    hour = random.randint(random_range[0], random_range[1])
    minute = random.randint(0, 59)

    # Create a datetime object and add it to the list
    random_times.append(datetime.time(hour, minute))

  return random_times


def generate_random_dates(df, start_date, end_date):
    random_dates = [start_date + (end_date - start_date) * random.random() for _ in range(df.shape[0])]
    random_dates_str = [date.strftime('%d/%m/%Y') for date in random_dates]
    df['annee_permis'] = random_dates_str
    return df

def set_random_values(df):
    # Définir la colonne 'niveau'
    niveau_list = ['M', 'L', 'P', 'U', 'SN']
    for i in range(len(df)):
        df.loc[i, 'niveau'] = random.choice(niveau_list)
    
    # Définir la colonne 'cat_veh'
    values = ['Leger', 'MOTO', 'Lour', 'Transport', 'NA']
    for i in range(len(df)):
        df.loc[i, 'cat_veh'] = random.choice(values)
    
    # Définir la colonne 'marque_veh'
    car_brands = ['peugeot', 'Renault', 'Berliet', 'Peugeot', 'Sonacom', 'TOYOTA', 'Sonakom', 'hafei', 'Harbin', 'Volkswagen',
                  'Suzuki', 'Isuzu', 'QQ', 'Remorque', 'Hyundai', 'sail', 'Congo', 'Daihatsu', 'expers', 'Toyota', 'Citroen',
                  'opel', 'Kia', 'Tractor', 'Jac', 'Iveco', 'citroen', 'Faw', 'Scania', 'Ford', 'Saksu', 'Mercedus', 'JMC',
                  'velo', 'Mitsubishi', 'Man']
    for i in range(len(df)):
        df.loc[i, 'marque_veh'] = random.choice(car_brands)
    
    return df

def set_annee_veh_column(df):
    annees = [1988, 1984, 2005, 2000, 2010, 2002, 2012, 2012, 1989, 1999, 1967, 2000, 1995, 1986, 2007, 2010,
            1988, 1985, 2001, 1975, 1986, 1979, 2010, 2012, 2011, 2007, 1997, 1982, 2001, 2012, 2010, 2008,
            2007, 1990, 1997, 2012, 2013, 1989, 1977, 1978, 1997, 1990, 2006, 1982, 2008, 2010, 1995, 2012,
            1993, 2012, 2012, 1997, 2012, 1984, 2000, 2011, 2012, 1995, 2012, 2001, 2001, 1989, 1989, 2010,
            2008, 1986, 2012, 2005, 2001, 2003, 2008, 2000, 2000, 2009, 2003, 2007, 2005, 2006, 2012, 2005,
            2003, 1992, 2000, 1997, 1997, 1996, 1993, 2007, 2007, 2013, 1974, 2013, 2005, 2008, 2008, 2004,
            2001, 1989, 1986, 1986, 1986, 2002, 1997, 2011, 2009, 2010, 2004, 2000, 2002, 2003, 2012, 1993,
            2012, 1998, 1993, 2012, 2001, 1998, 2004, 2013, 1999, 1992, 2007, 2011, 1974, 1998, 1993, 1990,
            2009, 2010, 2001, 2012, 2002, 2000, 2000, 1989, 2011, 1999, 1991, 1996, 1998, 1992, 1987, 2004,
            2001, 2004, 1999, 2001, 2004, 2002, 1998, 2011, 1990, 1997, 2013, 1995, 1962, 2003, 2010, 1991,
            2009, 2009, 1983, 2011, 2010, 2008, 2009, 2013, 2004, 2004, 1994, 2002, 2004, 2012, 1987, 2004,
            1999, 2012, 2011, 1997, 1977, 2013, 2009, 1999, 1991, 2009, 2006, 2013, 2012, 1966, 1998, 1998,
            1988, 2012, 2009, 2012, 2011, 1989, 2007, 1984, 2006, 2002, 2012, 2006, 2008, 1984, 2011, 1979,
            2012, 2006, 2004, 1987, 2007, 1997, 2002, 2009, 2012, 2008, 2013, 1994, 2007, 1997, 2011, 2007,
            2011, 1994, 2001, 1999, 2007, 1990, 2005, 2013, 2013, 2013, 2001, 2000, 1989, 2004, 2002, 1990,
            2013, 1988, 2007, 2003, 2012, 2010, 1989, 1981, 2000, 2004, 2008, 2000, 2008, 1999, 2009, 1977,
            2006, 2009, 1993, 2008, 1980, 2007, 1996, 2011, 2010, 2009, 2003, 1965, 1965, 1992, 1977, 2000,
            2011, 2001, 2011, 1991, 2009, 2011, 1988, 2013, 2007, 1999, 2000, 2012, 2006, 2005, 1998, 1991,
            2012, 1978, 2011, 1990, 1989, 2008, 2004, 2001, 2008, 1998, 2011, 2010, 1998, 2012, 1993, 2013,
            2001, 1974, 1991, 1995, 2006, 2013, 2001, 2013, 2013, 2006, 1989, 2010, 1998, 2005, 2006, 2000,
            2009, 2008, 2013, 2009, 2009, 2008, 2007, 2000, 2000, 2009, 2012, 2008, 2012, 2012, 2008, 2012,
            2012, 1999, 2005, 2009, 2012, 2005, 2012, 1996, 2012, 1995, 1970, 1998, 2012, 2009, 2011, 2012,
            1998, 1989, 1989, 1996, 2012, 2001, 2011, 1981, 2012, 1998, 1999, 1970, 2013, 1982, 1990, 2000,
            2012, 1997, 1996, 2003, 2012, 1999, 2002, 2005, 1988, 2002, 2000, 2000, 1996, 2010, 1984, 1989,
            1992, 2002, 2000, 2003, 2011, 2008, 2006, 2013, 1990, 2002, 2012, 2011, 2004, 2012, 1984, 2005,
            2011, 2009, 2008, 2013, 2010, 1987, 1971, 2007, 2000, 2006, 1968, 1983, 1994, 2000, 2001, 2006,
            2012, 2008, 2002, 2013, 2008, 1996, 1993, 2011, 2007, 2011, 2011, 1983, 2013, 2000, 2007, 2012,
            2000, 1989, 1965, 2013, 1983, 1984, 2010, 2012, 2009, 1993, 2007, 2013, 2009, 2006, 2009, 1996,
            1979, 2009, 2006, 1983, 2011, 2006, 1986, 2001, 1983, 2004, 2012, 2013, 2010, 1996, 1986, 2000,
            2013, 1998, 2003, 2000, 2003, 1999, 2001, 2011, 2005, 1986, 2000, 2001, 2004, 2011, 2011, 2013,
            1991, 1999, 2012, 2012, 2012, 2012, 1991, 2010, 2005, 2002, 2001, 1988, 2005, 2013, 2011, 2010,
            1983, 2000, 2012, 2001, 2012, 2012, 2006, 2012, 2011, 1986, 2000, 2012, 2012, 1989, 2012, 1981,
            2000, 2001, 2008, 1993, 2013, 2013, 2005, 2009, 1976, 2000, 2011, 2010, 2008, 2013, 2000, 2007,
            2007, 2011, 2001, 2012, 2012, 1992, 1993, 1994, 2011, 2013, 1994, 1990, 1999, 1995, 2012, 1999,
            2012, 2009, 1889, 2012, 1996, 2003, 1989, 1994, 1995, 2004, 1999, 2011, 1985, 2013, 2010, 1988,
            1997, 2008, 2006, 2006, 1994, 2008, 1998, 2011, 2012, 2008, 2006, 1997, 2008, 2005, 1978, 1998,
            1999, 2009, 2001, 1999, 2002, 2000, 2010, 2012, 2012, 2011, 2012, 2012, 2002, 2009, 2013, 2010,
            1977, 2009, 2011, 2008, 2006, 1998, 1989, 1987, 2002, 2008, 2009, 2008, 1992, 2008, 2002, 2012,
            2006, 1984, 1985, 2007, 2001, 1984, 2001, 2013, 2006, 2011, 2007, 2006, 2010, 1980, 2002, 2007,
            2008, 2011, 2002, 1994, 2010, 1983, 2001, 1987, 2002, 2007, 2012, 2006, 2010, 2006, 1984, 1997,
            2011, 2000, 2005, 2009, 2006, 2004, 2009, 1985, 2001, 2004, 2001, 2011, 2003, 1996, 1986, 2010,
            1994, 1999, 2006, 2007, 2010, 2012, 2012, 2006, 1998, 2010, 2002, 2004, 2005, 2006, 2011, 2012,
            1987, 2000, 1997, 2002, 2001, 2008, 1982, 1995, 2008, 1977, 2013, 1996, 1994, 2013, 2009, 1994,
            2011, 2005, 2012, 2009, 2013, 2006, 2000, 2007, 2009, 1995, 2012, 2005, 1987, 1996, 2004, 2013,
            2009, 2005, 2006, 2001, 2011, 1983, 1981, 1982, 2002, 2010, 2011, 2001, 2013, 2013, 2013, 1998,
            2006, 2010, 2007, 2009, 1996, 1999, 2007, 2009, 2013, 2012, 1998, 1997, 1999, 2009, 2000, 2001,
            2009, 2013]
    df['annee_veh'] = annees
    return df

def set_date_acci_column(df):
    dates = [
            "07/04/2013", "17/09/2013", "04/12/2013", "06/11/2013", "21/07/2013", "08/05/2013",
            "27/07/2013", "20/06/2013", "13/10/2013", "07/03/2013", "28/11/2013", "27/08/2013",
            "20/08/2013", "25/05/2013", "14/02/2013", "03/12/2013", "26/04/2013", "06/09/2013",
            "04/04/2013", "20/04/2013", "24/03/2013", "25/06/2013", "07/09/2013", "20/04/2013",
            "28/12/2013", "29/04/2013", "31/10/2013", "04/04/2013", "31/03/2013", "07/12/2013",
            "24/08/2013", "04/12/2013", "13/08/2013", "29/01/2013", "13/05/2013", "01/07/2013",
            "07/10/2013", "30/03/2013", "07/07/2013", "17/06/2013", "10/04/2013", "20/12/2013",
            "22/07/2013", "20/03/2013", "17/08/2013", "30/09/2013", "03/07/2013", "07/11/2013",
            "25/01/2013", "20/08/2013", "10/02/2013", "16/09/2013", "13/11/2013", "23/07/2013",
            "27/08/2013", "15/04/2013", "22/04/2013", "08/08/2013", "14/04/2013", "25/10/2013",
            "08/11/2013", "05/01/2013", "21/01/2013", "06/01/2013", "29/01/2013", "03/01/2013",
            "25/08/2013", "01/03/2013", "20/09/2013", "13/06/2013", "18/05/2013", "31/07/2013",
            "13/08/2013", "06/05/2013", "22/09/2013", "16/05/2013", "08/10/2013", "04/05/2013",
            "13/03/2013", "03/03/2013", "28/12/2013", "15/06/2013", "12/04/2013", "22/05/2013",
            "22/05/2013", "24/12/2013", "04/07/2013", "16/11/2013", "29/10/2013", "13/08/2013",
            "06/12/2013", "14/08/2013", "16/10/2013", "01/05/2013","07/06/2013", "09/05/2013",
            "28/11/2013", "01/10/2013", "20/05/2013",
            "28/09/2013", "28/07/2013", "13/01/2013", "28/12/2013", "19/06/2013", "07/01/2013",
            "24/09/2013", "24/06/2013", "10/12/2013", "15/08/2013", "30/03/2013", "28/06/2013",
            "09/08/2013", "04/04/2013", "30/03/2013", "23/10/2013", "25/07/2013", "30/07/2013",
            "02/07/2013", "08/09/2013", "25/10/2013", "29/08/2013", "29/08/2013", "08/11/2013",
            "25/07/2013", "01/05/2013", "15/08/2013", "30/01/2013", "06/06/2013", "26/03/2013",
            "26/10/2013", "17/05/2013", "30/07/2013", "24/03/2013", "19/04/2013", "16/08/2013",
            "08/01/2013", "27/10/2013", "15/07/2013", "11/03/2013", "26/05/2013", "14/07/2013",
            "20/09/2013", "09/06/2013", "24/08/2013", "04/03/2013", "30/09/2013", "25/07/2013",
            "31/10/2013", "09/01/2013", "17/02/2013", "22/11/2013", "24/05/2013", "31/03/2013",
            "04/03/2013", "01/10/2013", "28/05/2013", "30/07/2013", "02/12/2013", "21/06/2013",
            "05/08/2013", "08/06/2013", "11/09/2013", "04/12/2013", "04/12/2013", "12/05/2013",
            "08/06/2013", "26/08/2013", "05/08/2013", "07/09/2013", "25/10/2013", "13/06/2013",
            "21/06/2013", "25/02/2013", "15/03/2013", "07/04/2013", "19/03/2013", "25/06/2013",
            "22/04/2013", "04/12/2013", "28/04/2013", "06/03/2013", "23/09/2013", "03/07/2013",
            "07/12/2013", "20/03/2013", "25/07/2013", "05/10/2013", "27/07/2013", "31/01/2013",
            "12/03/2013", "05/01/2013", "01/01/2013", "13/01/2013", "22/06/2013", "26/11/2013",
            "26/05/2013", "28/07/2013", "03/11/2013", "12/03/2013", "24/04/2013",
            "04/08/2013", "16/09/2013", "15/10/2013", "18/04/2013", "30/06/2013", "16/10/2013",
            "31/08/2013", "26/10/2013", "08/10/2013", "28/05/2013", "15/08/2013", "09/09/2013",
            "30/04/2013", "17/09/2013", "25/06/2013", "29/04/2013", "15/10/2013", "09/07/2013",
            "13/10/2013", "08/06/2013", "11/07/2013", "04/10/2013", "21/07/2013", "06/04/2013",
            "06/08/2013", "28/07/2013", "15/07/2013", "06/04/2013", "14/01/2013", "31/07/2013",
            "23/07/2013", "17/06/2013", "13/06/2013", "08/01/2013", "18/07/2013", "11/03/2013",
            "07/01/2013", "31/05/2013", "16/08/2013", "30/08/2013", "20/05/2013", "13/07/2013",
            "06/10/2013", "16/12/2013", "07/02/2013", "05/09/2013", "04/03/2013", "20/06/2013",
            "23/06/2013", "06/07/2013", "12/05/2013", "30/06/2013", "10/11/2013", "21/08/2013",
            "05/09/2013", "05/11/2013", "06/09/2013", "06/06/2013", "05/05/2013", "02/02/2013",
            "26/10/2013", "10/01/2013", "30/05/2013", "21/08/2013", "06/05/2013", "10/04/2013",
            "05/01/2013", "05/04/2013", "20/08/2013", "06/12/2013", "09/09/2013", "08/10/2013",
            "19/10/2013", "10/10/2013", "06/06/2013", "24/11/2013", "24/08/2013", "10/01/2013",
            "17/07/2013", "11/09/2013", "01/02/2013", "01/10/2013", "11/03/2013", "13/08/2013",
            "15/06/2013", "31/10/2013", "05/09/2013", "28/03/2013", "23/05/2013", "24/01/2013",
            "22/08/2013", "30/09/2013", "12/09/2013", "07/09/2013", "03/09/2013", "19/03/2013",
            "16/09/2013", "17/10/2013", "27/06/2013", "17/11/2013", "14/05/2013", "20/05/2013",
            "24/05/2013", "17/04/2013", "30/04/2013", "01/03/2013", "19/02/2013", "04/05/2013",
            "15/07/2013", "30/06/2013", "25/09/2013", "29/03/2013", "07/01/2013", "07/06/2013",
            "26/06/2013", "14/11/2013", "16/07/2013", "31/05/2013", "08/11/2013", "18/08/2013",
            "06/10/2013", "21/06/2013", "01/06/2013", "13/02/2013", "10/08/2013", "23/08/2013",
            "08/06/2013", "14/09/2013", "10/01/2013", "06/06/2013", "07/11/2013", "24/12/2013",
            "09/02/2013", "19/05/2013", "14/07/2013", "26/01/2013", "08/01/2013", "20/02/2013",
            "25/12/2013", "13/07/2013", "30/03/2013", "07/04/2013", "30/08/2013", "31/01/2013",
            "27/10/2013", "08/11/2013", "06/05/2013", "09/02/2013", "06/11/2013", "28/06/2013",
            "06/12/2013", "09/01/2013", "02/02/2013", "20/03/2013", "23/04/2013", "08/10/2013",
            "15/05/2013", "01/10/2013", "06/11/2013", "29/03/2013", "16/08/2013", "06/03/2013",
            "27/03/2013", "14/08/2013", "07/05/2013", "05/10/2013", "17/07/2013", "08/10/2013",
            "27/11/2013", "13/06/2013", "06/11/2013", "16/10/2013", "14/07/2013", "05/08/2013",
            "11/10/2013", "09/07/2013", "13/10/2013", "05/10/2013", "17/01/2013", "06/10/2013",
            "28/06/2013", "22/09/2013", "25/12/2013", "23/07/2013", "10/08/2013", "31/05/2013",
            "09/01/2013", "09/01/2013", "20/07/2013", "06/11/2013", "20/05/2013", "05/07/2013",
            "29/07/2013", "25/04/2013", "09/05/2013", "02/10/2013", "02/06/2013", "14/07/2013",
            "24/12/2013", "11/11/2013", "14/08/2013", "08/08/2013", "10/01/2013", "08/12/2013",
            "06/09/2013", "17/04/2013", "02/06/2013", "14/04/2013", "17/07/2013", "08/07/2013",
            "12/05/2013", "06/07/2013", "14/02/2013", "11/02/2013", "26/05/2013", "29/08/2013",
            "22/08/2013", "16/01/2013", "06/12/2013", "08/07/2013", "19/11/2013", "25/09/2013",
            "22/11/2013", "07/04/2013", "16/11/2013", "20/03/2013", "27/02/2013", "24/05/2013",
            "17/06/2013", "20/04/2013", "18/04/2013", "09/08/2013", "26/12/2013", "14/08/2013",
            "12/01/2013", "21/11/2013", "07/02/2013", "18/04/2013", "01/04/2013", "01/11/2013",
            "08/07/2013", "18/10/2013", "15/06/2013", "06/03/2013", "30/04/2013", "20/06/2013",
            "07/08/2013", "03/04/2013", "26/07/2013", "06/12/2013", "15/05/2013", "07/11/2013",
            "16/05/2013", "03/12/2013", "14/08/2013", "27/09/2013", "05/11/2013", "28/08/2013",
            "16/04/2013", "14/05/2013", "22/06/2013", "05/06/2013", "17/08/2013", "20/02/2013",
            "20/01/2013", "29/06/2013", "29/01/2013", "08/05/2013", "05/05/2013", "01/07/2013",
            "22/04/2013", "10/12/2013", "06/01/2013", "19/11/2013", "05/02/2013", "29/08/2013",
            "04/09/2013", "03/12/2013", "26/12/2013", "21/06/2013", "23/03/2013", "23/08/2013",
            "12/08/2013", "17/05/2013", "06/12/2013", "15/08/2013", "11/07/2013", "04/01/2013",
            "04/01/2013", "19/03/2013", "16/06/2013", "10/07/2013", "05/08/2013", "26/03/2013",
            "01/08/2013", "25/01/2013", "24/04/2013", "06/09/2013", "06/11/2013", "25/07/2013",
            "06/04/2013", "06/04/2013", "01/09/2013", "22/02/2013", "06/05/2013", "17/09/2013",
            "13/04/2013", "27/07/2013", "02/08/2013", "14/12/2013", "29/08/2013", "14/06/2013",
            "17/08/2013", "24/03/2013", "08/12/2013", "12/05/2013", "14/07/2013", "28/10/2013",
            "07/09/2013", "05/04/2013", "11/05/2013", "05/04/2013", "01/09/2013", "02/12/2013",
            "07/08/2013", "01/04/2013", "21/12/2013", "02/11/2013", "25/01/2013", "02/02/2013",
            "18/03/2013", "23/10/2013", "08/10/2013", "05/11/2013", "13/09/2013", "21/01/2013",
            "15/03/2013", "06/07/2013", "13/05/2013", "16/10/2013", "03/08/2013", "21/06/2013",
            "06/11/2013", "01/08/2013", "22/02/2013", "21/06/2013", "17/08/2013", "26/09/2013",
            "14/06/2013", "21/08/2013", "16/08/2013", "19/09/2013", "22/09/2013", "27/07/2013",
            "08/01/2013", "16/10/2013", "06/04/2013", "25/09/2013", "12/07/2013", "18/01/2013",
            "29/08/2013", "13/12/2013", "31/07/2013", "30/06/2013", "14/03/2013", "22/06/2013",
            "30/11/2013", "24/08/2013", "08/02/2013", "16/06/2013", "09/06/2013", "25/06/2013",
            "01/08/2013", "08/11/2013", "24/09/2013", "28/09/2013", "08/09/2013", "07/06/2013",
            "09/06/2013", "06/09/2013", "09/04/2013", "26/03/2013", "04/04/2013", "08/05/2013",
            "16/04/2013", "14/11/2013", "27/04/2013", "01/05/2013", "25/07/2013", "15/10/2013",
            "04/12/2013", "12/04/2013", "26/12/2013", "17/02/2013", "22/09/2013", "19/05/2013",
            "01/06/2013", "20/04/2013", "23/06/2013", "28/03/2013", "30/03/2013", "05/10/2013",
            "17/05/2013", "24/03/2013", "25/09/2013", "05/06/2013", "22/08/2013", "26/06/2013",
            "21/03/2013", "25/07/2013", "27/08/2013", "16/06/2013", "21/11/2013", "15/08/2013",
            "10/03/2013", "08/08/2013", "25/07/2013", "26/12/2013", "13/01/2013", "25/12/2013",
            "28/04/2013", "30/12/2013", "13/08/2013", "03/09/2013", "11/05/2013", "03/04/2013",
            "06/09/2013", "04/04/2013", "28/01/2013", "15/08/2013", "19/04/2013", "24/05/2013",
            "10/03/2013", "18/07/2013", "01/08/2013", "29/04/2013", "26/08/2013", "22/04/2013",
            "06/11/2013", "15/08/2013", "09/01/2013", "09/03/2013", "22/08/2013", "04/03/2013",
            "28/04/2013", "01/09/2013", "03/09/2013", "15/12/2013", "17/04/2013", "08/06/2013",
            "08/10/2013", "19/10/2013", "06/02/2013", "01/05/2013", "08/11/2013", "31/10/2013",
            "12/11/2013", "28/07/2013", "14/03/2013", "24/08/2013", "22/09/2013", "23/10/2013",
            "05/04/2013", "22/02/2013", "02/03/2013", "09/12/2013", "17/10/2013", "31/07/2013",
            "09/06/2013", "17/06/2013", "03/12/2013", "30/08/2013", "16/08/2013", "18/04/2013",
            "15/09/2013", "08/11/2013", "21/03/2013", "11/08/2013", "09/04/2013", "07/06/2013",
            "16/02/2013", "28/09/2013", "23/10/2013", "20/04/2013", "07/09/2013", "19/10/2013",
            "13/06/2013", "18/08/2013", "08/07/2013", "27/08/2013", "30/07/2013", "08/11/2013",
            "25/06/2013", "17/10/2013", "29/09/2013", "06/08/2013", "16/02/2013", "23/06/2013",
            "22/04/2013", "05/03/2013", "30/10/2013", "08/10/2013", "28/05/2013", "16/01/2013",
            "10/08/2013", "10/02/2013", "13/09/2013", "10/08/2013", "18/06/2013", "27/01/2013",
            "09/04/2013", "16/06/2013", "12/02/2013", "07/06/2013", "07/08/2013", "08/09/2013",
            "07/07/2013", "07/07/2013", "22/12/2013", "29/08/2013", "06/11/2013", "29/07/2013",
            "16/07/2013", "31/01/2013", "24/03/2013", "10/04/2013", "27/04/2013", "31/12/2013",
            "24/08/2013", "20/06/2013", "07/09/2013", "28/07/2013", "27/04/2013", "23/08/2013",
            "09/02/2013", "12/12/2013", "11/03/2013", "30/08/2013"]
    df['Date_Acci'] = dates
    return df

def generate_random_dates2(df, start_date, end_date):
    random_dates = [start_date + (end_date - start_date) * random.random() for _ in range(df.shape[0])]
    random_dates_str = [date.strftime('%d/%m/%Y') for date in random_dates]
    df['annee_permis'] = random_dates_str
    return df

# Définir les intervalles de dates et leurs probabilités
date_ranges = [
    ((datetime(1981, 1, 1), datetime(1990, 12, 31)), 0.5),
    ((datetime(1971, 1, 1), datetime(1980, 12, 31)), 0.2),
    ((datetime(1991, 1, 1), datetime(2000, 12, 31)), 0.1),
    ((datetime(1961, 1, 1), datetime(1970, 12, 31)), 0.09),
    ((datetime(1951, 1, 1), datetime(1960, 12, 31)), 0.07),
    ((datetime(1940, 1, 1), datetime(1950, 12, 31)), 0.04),

]

# Fonction pour générer une date aléatoire dans un intervalle donné
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_days = random.randrange(days_between_dates)
    return start_date + timedelta(days=random_days)

# Générer des dates aléatoires selon les probabilités
random_dates = []
for date_range, probability in date_ranges:
    start_date, end_date = date_range
    num_dates = int(741 * probability)  # Générer 10000 dates en respectant la probabilité
    for _ in range(num_dates):
        random_date_obj = random_date(start_date, end_date)
        random_dates.append(random_date_obj.strftime("%d/%m/%Y"))

def calculate_age(df):
    # Convertir les colonnes de dates au format datetime
    df['date_naissance'] = pd.to_datetime(df['date_naissance'], format="%d/%m/%Y")
    df['Date_Acci'] = pd.to_datetime(df['Date_Acci'], format="%d/%m/%Y")

    # Calculer l'âge
    df['Age'] = (df['Date_Acci'].dt.year - df['date_naissance'].dt.year) - \
                ((df['Date_Acci'].dt.month < df['date_naissance'].dt.month) |
                 ((df['Date_Acci'].dt.month == df['date_naissance'].dt.month) &
                  (df['Date_Acci'].dt.day < df['date_naissance'].dt.day)))

    # Convertir la colonne 'Age' en type entier
    df['Age'] = df['Age'].astype(int)

    return df

def add_weekend_column(df, date_column):
    # S'assurer que la colonne de date est de type datetime
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Créer la colonne 'Weekend'
    df["Weekend"] = df[date_column].dt.strftime("%A")
    
    # Créer la colonne 'Week_non_week'
    df["Week_non_week"] = df["Weekend"].apply(lambda x: "Weekend" if x in ["Saturday", "Friday"] else "Non-Weekend")
    
    return df

def standardize_place_names(df, column_name):

    replacements = {'AIN ABESSA' : 'AIN ABESSA',
            'AIN ARNAT' : 'AIN ARNAT',
            'AIN AZEL' : 'AIN AZEL',
            'AIN EL KEBIRA' : 'AIN EL KEBIRA',
            'AIN LAGRADJ' : 'AIN-LEGRADJ',
            'AIN LAHDJAR' : 'AIN LAHDJAR',
            'AIN OULMENE' : 'AIN OULMENE',
            'AIN ROUA' : 'AIN-ROUA',
            'AIN SEBT' : 'AIN-SEBT',
            'AIT NOUAL M\'ZADA' : 'AIT NOUAL MZADA',
            'AIT TIZI' : 'AIT TIZI',
            'AMOUCHA' : 'AMOUCHA',
            'BABOR' : 'BABOR',
            'BAZER SAKRA' : 'BAZER-SAKRA',
            'BEIDA BORDJ' : 'BEIDHA BORDJ',
            'BELLAA' : 'BELLAA',
            'BENI AZIZ' : 'BENI-AZIZ',
            'BENI CHEBANA' : 'BENI CHEBANA',
            'BENI FOUDA' : 'BENI FOUDA',
            'BENI MOUHLI' : 'BENI-MOUHLI',
            'BENI OUARTILANE' : 'BENI OURTILANE',
            'BENI OUSSINE' : 'BENI HUSSINE',
            'BIR EL ARCHE' : 'BIR-EL-ARCH',
            'BIR HADDADA' : 'BIR HADDADA',
            'BOUANDAS' : 'BOUANDAS',
            'BOUGAA' : 'BOUGAA',
            'BOUSSELAM' : 'BOUSSELAM',
            'BOUTALEB' : 'BOUTALEB',
            'DEHAMCHA' : 'DEHAMCHA',
            'DJEMILA' : 'DJEMILA',
            'DRAA KEBILA' : 'DRAA KEBILA',
            'EL EULMA' : 'EL EULMA',
            'EL OUELDJA' : 'EL-OULDJA',
            'EL OURICIA' : 'EL OURICIA',
            'GUELLAL' : 'GUELLAL',
            'GUELT ZERGA' : 'GUELTA ZERKA',
            'GUENZET' : 'GUENZET',
            'GUIDJEL' : 'GUIDJEL',
            'HAMMA' : 'HAMMA',
            'HAMMAM ESOUKHNA' : 'HAMAM SOUKHNA',
            'HAMMAM GUERGOUR' : 'HAMMAM GUERGOUR',
            'HARBIL' : 'HARBIL',
            'KSAR EL ABTAL' : 'KASR EL ABTAL',
            'MAOKLANE' : 'MAOUAKLANE',
            'MAOUIA' : 'MAOUIA',
            'MEZLOUG' : 'MEZLOUG',
            'OUED  BARED' : 'OUED EL BARED',
            'OULED ADDOUANE' : 'OULED ADDOUANE',
            'OULED SABOR' : 'OULED SABOR',
            'OULED SI AHMED' : 'OULED SI AHMED',
            'OULED TEBBEN' : 'OULED TEBBEN',
            'RASFA' : 'ROSFA',
            'SALAH BEY' : 'SALAH BEY',
            'SERDJ EL GHOUL' : 'SERDJ EL GHOUL',
            'SETIF' : 'SETIF',
            'TACHOUDA' : 'TACHOUDA',
            'TALA IFACENE ' : 'TALAIFACENE',
            'TAYA' : 'TAYA',
            'TELLA' : 'TELLA',
            'TIZI N\'BECHAR' : 'TIZI BECHAR',}
    df[column_name] = df[column_name].replace(replacements)
    return df

def add_population_column(df, commune_column, population_dict):
    df['Population'] = df[commune_column].map(population_dict)
    return df

def add_Area_column(df, commune_column, communes_Area):
    df['Area'] = df[commune_column].map(communes_Area)
    return df


def calculate_population_density(df, population_column, area_column, density_column_name='density_pop'):
    df[density_column_name] = df[population_column] / df[area_column]
    return df

#df_non_acc= join_geodata(df_non_acc, df_com)
#df_non_acc.drop(['index_right'], axis=1, inplace=True)


df_non_acc = add_new_columns(df_non_acc)
df_non_acc = set_accident_columns(df_non_acc)
df_non_acc = set_random_columns(df_non_acc)
df_non_acc = set_meteo_column(df_non_acc)


# Generate random times for the given number of rows
num_rows = len(df_non_acc)
random_times = generate_random_time(num_rows)
# Add the random times to the DataFrame
df_non_acc['heure_acc'] = random_times

start_date = datetime(1988, 1, 1)
end_date = datetime(2013, 12, 31)
df_non_acc = generate_random_dates(df_non_acc, start_date, end_date)

df_non_acc = set_random_values(df_non_acc)
df_non_acc = set_annee_veh_column(df_non_acc)
df_non_acc = set_date_acci_column(df_non_acc)

start_date = datetime(1988, 1, 1)
end_date = datetime(2013, 12, 31)
df_non_acc = generate_random_dates2(df_non_acc, start_date, end_date)

df_non_acc['date_naissance'] =random_dates

df_non_acc = calculate_age(df_non_acc)

df_non_acc = add_weekend_column(df_non_acc, "Date_Acci")

df_non_acc = standardize_place_names(df_non_acc, "COMMUNE")


# Exemple d'utilisation de la fonction
commune_population = {
    'EL EULMA': 155038,
    'BOUGAA': 30987,
    'SETIF': 288461,
    'EL OURICIA': 18087,
    'AIN-ROUA': 11499,
    'BENI OURTILANE': 10591,
    'OULED SI AHMED': 10238,
    'BEIDHA BORDJ': 35276,
    'BIR-EL-ARCH': 24995,
    'TACHOUDA': 7578,
    'BENI-AZIZ': 19383,
    'AIN OULMENE': 73831,
    'BOUANDAS': 16966,
    'AIN ARNAT': 43551,
    'HAMMA': 13223,
    'BOUTALEB': 9456,
    'OULED SABOR': 12510,
    'GUIDJEL': 33685,
    'HAMAM SOUKHNA': 13439,
    'TAYA': 10302,
    'AIN AZEL': 48487,
    'KASR EL ABTAL': 23833,
    'EL-OULDJA': 8592,
    'BENI CHEBANA': 13174,
    'ROSFA': 16075,
    'AIN EL KEBIRA': 36295,
    'AIN ABESSA': 1677,
    'MEZLOUG': 16976,
    'BABOR': 15762,
    'TIZI BECHAR': 21086,
    'BIR HADDADA': 20860,
    'BENI FOUDA': 17667,
    'DJEMILA': 24145,
    'OULED ADDOUANE': 9613,
    'GUELLAL': 21385,
    'OULED TEBBEN': 10385,
    'BELLAA': 14666,
    'AMOUCHA': 22767,
    'AIN LAHDJAR': 34338,
    'AIN-SEBT': 14798,
    'OUED EL BARED': 2333,
    'AIN-LEGRADJ': 3675,
    'HARBIL': 3675,
    'BENI-MOUHLI': 8521,
    'HAMMAM GUERGOUR': 15853,
    'MAOUAKLANE': 15715,
    'GUELTA ZERKA': 15472,
    'BAZER-SAKRA': 27996,
    'GUELLAL':21385,
    'AIT NOUAL MZADA':5630,
    'AIT TIZI':6983,
    'BENI HUSSINE':11220,
    'BOUSSELAM':16059,
    'DEHAMCHA':9141,
    'DRAA KEBILA':14977,
    'GUENZET':3541,
    'MAOUIA':7005,
    'SALAH BEY':27175,
    'SERDJ EL GHOUL':9311,
    'TALA IFACENE':20337,
    'TELLA':7562,
}

# Supposons que data_non_acc1 soit déjà défini quelque part dans votre code
df_non_acc = add_population_column(df_non_acc, "COMMUNE", commune_population)

communes_Area = {
    'EL EULMA': 74,
    'BOUGAA': 61,
    'SETIF': 6504,
    'EL OURICIA': 120,
    'AIN-ROUA': 117,
    'BENI OURTILANE': 71,
    'OULED SI AHMED': 103,
    'BEIDHA BORDJ': 145,
    'BIR-EL-ARCH': 142,
    'TACHOUDA': 80,
    'BENI-AZIZ': 56,
    'AIN OULMENE': 162,
    'BOUANDAS': 38,
    'AIN ARNAT': 206,
    'HAMMA': 100,
    'BOUTALEB': 143,
    'OULED SABOR': 119,
    'GUIDJEL': 234,
    'HAMAM SOUKHNA': 184,
    'TAYA': 145,
    'AIN AZEL': 257,
    'KASR EL ABTAL': 114,
    'EL-OULDJA': 152,
    'BENI CHEBANA': 56,
    'ROSFA': 189,
    'AIN EL KEBIRA': 66,
    'AIN ABESSA': 164,
    'MEZLOUG': 136,
    'BABOR': 142,
    'TIZI BECHAR': 71,
    'BIR HADDADA': 116,
    'BENI FOUDA': 162,
    'DJEMILA': 157,
    'OULED ADDOUANE': 28,
    'GUELLAL': 126,
    'OULED TEBBEN': 176,
    'BELLAA': 143,
    'AMOUCHA': 88,
    'AIN LAHDJAR': 228,
    'AIN-SEBT': 74,
    'OUED EL BARED': 49,
    'AIN-LEGRADJ': 74,
    'HARBIL': 86,
    'BENI-MOUHLI': 27,
    'HAMMAM GUERGOUR': 76,
    'MAOUAKLANE': 87,
    'GUELTA ZERKA': 132,
    'BAZER-SAKRA': 160,
    'AIT NOUAL MZADA':26,
    'AIT TIZI':37,
    'BENI HUSSINE':55,
    'BOUSSELAM':60,
    'DEHAMCHA':104,
    'DRAA KEBILA':60,
    'GUENZET':60,
    'MAOUIA':85,
    'SALAH BEY':140,
    'SERDJ EL GHOUL':97,
    'TALA IFACENE':56,
    'TELLA':117,
}
# Supposons que data_non_acc1 soit déjà défini quelque part dans votre code
df_non_acc = add_Area_column(df_non_acc, "COMMUNE", communes_Area)

df_non_acc = calculate_population_density(df_non_acc, 'Population', 'Area')


df_non_acc.drop(columns=['index_right'], inplace=True)
df_non_acc.rename(columns={"COMMUNE": "Commune"}, inplace=True)
df_non_acc.rename(columns={"Type": "type_route"}, inplace=True)
print(df_non_acc.info())
df_non_acc[['Date_Acci','date_naissance']] = df_non_acc[['Date_Acci','date_naissance']].astype(str)
df_non_acc.to_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/data_non_acc/data_non_acc.gpkg")
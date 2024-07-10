import geopandas as gpd
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

data = gpd.read_file("C:/Users/hp/Desktop/test_mimoir/ariba/traduit/predection/data.gpkg")
data.rename(columns={'Type': 'type_route'}, inplace=True)
print(data.info())
#data.drop(['index_right'], axis=1, inplace=True)

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

def update_data3(data):
    # Prompt user for inputs
    date_input = '07/06/2024'
    heur_input = '14:15'
    meteo_input = 'LT'
    vision_input = 'M'
    etat_chauss_input = 'GL'
    etat_route_input = 'MG'

    # Update the data dictionary
    data['date'] = date_input
    data['heur'] = heur_input
    data['meteo'] = meteo_input
    data['vision'] = vision_input
    data['etat_chauss'] = etat_chauss_input
    data['etat_route'] = etat_route_input

    return data

def add_month_column(data):
    # Ensure the 'date' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')
    
    # Add the 'month' column
    data['month'] = data['date'].dt.month
    
    return data

# Define the reclassify function
def reclassify_month(row):
        if row['month'] in [12, 1, 2]:
            return 'H'  # Hiver (Winter)
        elif row['month'] in [3, 4, 5]:
            return 'P'  # Printemps (Spring)
        elif row['month'] in [6, 7, 8]:
            return 'E'  # Été (Summer)
        elif row['month'] in [9, 10, 11]:
            return 'A'  # Automne (Autumn)

def reclassify_hour(row):
    # Convert the string to datetime object
    time_obj = pd.to_datetime(row['heur'])

    # Extract the hour from the datetime object
    hour = time_obj.hour

    if 8 <= hour <= 12:
        return 'PMA'
    elif 13 <= hour <= 20:
        return 'PS'
    else:
        return 'PM'

def add_binary_columns(data):
    # Create binary columns for 'Periode_jour'
    data['Periode_jour_PMA'] = np.where(data['Periode_jour'] == 'PMA', 1, 0)
    data['Periode_jour_PS'] = np.where(data['Periode_jour'] == 'PS', 1, 0)

    # Create binary columns for 'Saison'
    data['Saison_E'] = np.where(data['Saison'] == 'E', 1, 0)
    data['Saison_P'] = np.where(data['Saison'] == 'P', 1, 0)

    # Create binary columns for 'meteo'
    data['meteo_LT'] = np.where(data['meteo'] == 'LT', 1, 0)
    data['meteo_PL'] = np.where(data['meteo'] == 'PL', 1, 0)
    data['meteo_SN'] = np.where(data['meteo'] == 'SN', 1, 0)
    data['meteo_N'] = np.where(data['meteo'] == 'N', 1, 0)

    # Create binary columns for 'vision'
    data['vision_M'] = np.where(data['vision'] == 'M', 1, 0)
    data['vision_F'] = np.where(data['vision'] == 'F', 1, 0)

    # Create binary columns for 'etat_chauss'
    data['etat_chauss_GL'] = np.where(data['etat_chauss'] == 'GL', 1, 0)
    data['etat_chauss_HM'] = np.where(data['etat_chauss'] == 'HM', 1, 0)

    # Replace values in 'type_route' and create binary columns
    data['type_route'] = data['type_route'].replace('RN', 'RNN')
    data['type_route'] = data['type_route'].replace('A', 'A1')
    data['type_route_A1'] = np.where(data['type_route'] == 'A1', 1, 0)
    data['type_route_RNN'] = np.where(data['type_route'] == 'RNN', 1, 0)
    data['type_route_RW'] = np.where(data['type_route'] == 'RW', 1, 0)

    # Create binary columns for 'etat_route'
    data['etat_route_MG'] = np.where(data['etat_route'] == 'MG', 1, 0)
    data['etat_route_NP'] = np.where(data['etat_route'] == 'NP', 1, 0)

    return data

def add_weekend_columns(data):
    # Ensure the 'date' column is in datetime format
    if not pd.api.types.is_datetime64_any_dtype(data['date']):
        data['date'] = pd.to_datetime(data['date'], format='%d/%m/%Y')
    
    # Create the "Weekend" column
    data["Weekend"] = data["date"].dt.strftime("%A")
    
    # Create the "Week_non_week_Weekend" column
    data["Week_non_week_Weekend"] = data["Weekend"].apply(lambda x: "Weekend" if x in ["Saturday", "Friday"] else "Non-Weekend")
    
    return data

def convert_week_non_week(df, column_name):
    df[column_name] = np.where(df[column_name] == "Non-Weekend", 0, 1)
    return df

data = standardize_place_names(data, "COMMUNE")
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
data = add_population_column(data, "COMMUNE", commune_population)
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
data = add_Area_column(data, "COMMUNE", communes_Area)
data = calculate_population_density(data, 'Population', 'Area', 'density_pop')

data = update_data3(data)
# Add the 'month' column
data = add_month_column(data)
# Apply the reclassification to each row
data['Saison'] = data.apply(reclassify_month, axis=1)
data['Periode_jour'] = data.apply(reclassify_hour, axis=1)
data = add_binary_columns(data)
# Add the weekend columns
data = add_weekend_columns(data)
print(data["Weekend"].head())
print(data["Week_non_week_Weekend"].head())
data = convert_week_non_week(data, "Week_non_week_Weekend")
data.drop(['type_route', 'COMMUNE', 'date', 'heur', 'meteo', 'vision', 'etat_chauss',
             'etat_route', 'month', 'Saison', 'Periode_jour','Weekend'], axis=1, inplace=True)
data['accident'] = None
data = data[['density_pop', 'accident', 'Week_non_week_Weekend', 'Periode_jour_PMA', 'Periode_jour_PS',
                'meteo_LT', 'meteo_N', 'meteo_PL', 'meteo_SN', 'Saison_E', 'Saison_P', 'etat_chauss_GL',
                  'etat_chauss_HM', 'etat_route_MG', 'etat_route_NP', 'type_route_A1', 'type_route_RNN',
                    'type_route_RW', 'vision_F', 'vision_M', 'geometry']]
print(data.info())
print(data.head())


# Load the model
model = joblib.load('C:/Users/hp/Desktop/test_mimoir/ariba/traduit/predection/dt_model_deploy3.joblib')
data1=data.copy()
data1.drop('geometry', axis=1, inplace=True)
data1 = data1.drop('accident', axis=1)
data1['accident'] = model.predict(data1)
print(data1.head())
print(data1['accident'].unique())
#plot les point acct et non acc
data['accident']=data1['accident']
data.plot(column='accident', legend=True)

# Plot the points with accidents in red
data[data['accident'] == 1].plot(color='red', marker='o', label='Accident')
# Add a legend
plt.legend()
# Show the plot
plt.show()

accident_data = data[data['accident'] == 1]

gdf = gpd.GeoDataFrame(accident_data, geometry='geometry')

gdf.to_file('accident_data.gpkg', driver='GPKG')
